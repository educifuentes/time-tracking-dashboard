#!/bin/bash

# Configuration
SERVICE_NAME="time-track-dashboard"
REGION="southamerica-west1"
SECRET_NAME="time-track-dashboard-secrets"
REPO_NAME="cloud-run-source-deploy" # Standard repo name
PROJECT_ID="personal-dashboards-487913"
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
IMAGE_NAME="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}:latest"
SERVICE_ACCOUNT="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

echo "🚀 Starting Deployment Process..."

# 1. Upload Secrets
echo "--- Step 1: Uploading Secrets to Secret Manager ---"
./scripts/upload_secrets.sh

# 2. Grant Permissions (New Step)
echo "--- Step 2: Granting Secret Access to Cloud Run Service Account ---"
echo "Granting roles/secretmanager.secretAccessor to $SERVICE_ACCOUNT on $SECRET_NAME..."
gcloud secrets add-iam-policy-binding $SECRET_NAME \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/secretmanager.secretAccessor" \
    --project=$PROJECT_ID >/dev/null 2>&1 || echo "Warning: Could not grant permissions automatically. Ensure your user has IAM permission management rights."

# 3. Ensure Artifact Registry Repository exists
echo "--- Step 3: Ensuring Artifact Registry Repository exists ---"
gcloud artifacts repositories describe $REPO_NAME --location=$REGION >/dev/null 2>&1 || \
gcloud artifacts repositories create $REPO_NAME \
    --repository-format=docker \
    --location=$REGION \
    --description="Repository for Cloud Run images"

# 4. Build the Image using Cloud Build
echo "--- Step 4: Building Image with Cloud Build ---"
gcloud builds submit --tag $IMAGE_NAME .

# 5. Deploy to Cloud Run
echo "--- Step 5: Deploying to Cloud Run ---"
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --region $REGION \
    --allow-unauthenticated \
    --set-secrets="/app/.streamlit/secrets.toml=${SECRET_NAME}:latest" \
    --port 8080

echo "✅ Deployment complete!"
