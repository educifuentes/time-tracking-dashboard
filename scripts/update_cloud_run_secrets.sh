#!/bin/bash

# Configuration
SERVICE_NAME="time-track-dashboard"
REGION="southamerica-west1"
SECRET_NAME="time-track-dashboard-secrets"
PROJECT_ID="personal-dashboards-487913"
SECRETS_FILE=".streamlit/secrets.toml"

echo "🚀 Starting Secrets Update for $SERVICE_NAME..."

# 1. Upload Secrets to Secret Manager
echo "--- Step 1: Uploading Secrets to Secret Manager ---"
if [ ! -f "$SECRETS_FILE" ]; then
    echo "Error: $SECRETS_FILE not found."
    exit 1
fi

echo "Checking if secret $SECRET_NAME exists..."
if gcloud secrets describe "$SECRET_NAME" --project="$PROJECT_ID" >/dev/null 2>&1; then
    echo "Secret exists. Adding new version..."
else
    echo "Creating new secret $SECRET_NAME..."
    gcloud secrets create "$SECRET_NAME" --replication-policy="automatic" --project="$PROJECT_ID"
fi

echo "Uploading contents of $SECRETS_FILE to $SECRET_NAME..."
gcloud secrets versions add "$SECRET_NAME" --data-file="$SECRETS_FILE" --project="$PROJECT_ID"

# 2. Grant Access (Crucial for CD where the service identity might change or lose permission)
echo "--- Step 2: Granting Access to Cloud Run Service Account ---"
# Get the service account used by the Cloud Run service
SERVICE_ACCOUNT=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(spec.template.spec.serviceAccountName)")

if [ -z "$SERVICE_ACCOUNT" ]; then
    # Fallback to default compute service account if not explicitly set
    PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
    SERVICE_ACCOUNT="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
    echo "Service account not found in service definition, assuming default: $SERVICE_ACCOUNT"
else
    echo "Target Service Account: $SERVICE_ACCOUNT"
fi

echo "Granting roles/secretmanager.secretAccessor to $SERVICE_ACCOUNT on $SECRET_NAME..."
gcloud secrets add-iam-policy-binding $SECRET_NAME \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/secretmanager.secretAccessor" \
    --project=$PROJECT_ID >/dev/null 2>&1 || echo "Warning: Could not grant permissions automatically."

# 3. Update Cloud Run Service to use the new Secret
echo "--- Step 3: Updating Cloud Run Service to Mount Secret ---"
# This command updates the service to mount the latest version of the secret at the expected path
gcloud run services update $SERVICE_NAME \
    --region=$REGION \
    --set-secrets="/app/.streamlit/secrets.toml=${SECRET_NAME}:latest"

echo "✅ Secrets updated and service re-deployed!"
