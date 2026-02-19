# Deploying to Google Cloud

This project includes scripts to automate the deployment process to Google Cloud Run.

## Key Services Used

To deploy this application, you will use **both** Cloud Build and Cloud Run:

1.  **Cloud Build**: This service builds your application code into a Docker container image. It runs the build steps defined in the `Dockerfile` (or automatically detects languages).
    - _Usage_: The `scripts/deploy.sh` script runs `gcloud builds submit` to bundle your code and save the image to Artifact Registry.
2.  **Cloud Run**: This service takes the Docker image built by Cloud Build and runs it as a scalable web service.
    - _Usage_: The `scripts/deploy.sh` script runs `gcloud run deploy` to launch the container in a managed serverless environment.

## Prerequisites

1.  **GCP Credentials**: Ensure you have set up your GCP project and credentials. See [GCP Credentials Guide](gcp_credentials.md) for details.
2.  **Enabled APIs**: You must enable both the **Cloud Build API** and **Cloud Run API** (along with Artifact Registry and Secret Manager). The [GCP Credentials Guide](gcp_credentials.md) covers this.
3.  **gcloud CLI**: Make sure you have the `gcloud` CLI installed and authenticated.

## Deployment Steps

The deployment process is automated via the `scripts/deploy.sh` script.

### 1. Upload Secrets

Before deploying, ensure your local secrets in `.streamlit/secrets.toml` are uploaded to Google Secret Manager. The deployment script handles this calling `scripts/upload_secrets.sh`, but you can also run it manually:

```bash
./scripts/upload_secrets.sh
```

### 2. Run Deployment Script

Run the main deployment script:

```bash
./scripts/deploy.sh
```

This script will:

1.  Upload/Update secrets in Secret Manager.
2.  Grant necessary permissions to the Cloud Run service account to access secrets.
3.  Ensure the Artifact Registry repository exists.
4.  Build the Docker image using Cloud Build.
5.  Deploy the service to Cloud Run.

## Configuration

The deployment configuration variables are located at the top of `scripts/deploy.sh`:

- `SERVICE_NAME`: The name of the Cloud Run service (default: `time-track-dashboard`).
- `REGION`: The GCP region (default: `southamerica-west1`).

### 3. Continuous Deployment (CD) Setup

If you have set up Continuous Deployment (e.g., via Cloud Build triggers from GitHub):

1.  **Code Changes**: Pushing to your repository will automatically build and deploy the new image.
2.  **Secret Management**: Since `.streamlit/secrets.toml` is **not** in your repository, updating secrets requires a manual step.
    - Run the provided script to upload your local secrets and configure the running service to use them:
      ```bash
      ./scripts/update_cloud_run_secrets.sh
      ```
    - This script uploads the current state of your local `.streamlit/secrets.toml` to Secret Manager and updates the Cloud Run service to mount it.

- `SECRET_NAME`: The name of the secret in Secret Manager (default: `time-track-dashboard-secrets`).
