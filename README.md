# Time Tracking App

## Application

The dashboard is deployed on Google Cloud Run:
[**Open App**](https://time-track-dashboard-246254753086.southamerica-west1.run.app)

## Management

Access the Google Cloud Console to manage revisions and billing:
[**Manage Cloud Run**](https://console.cloud.google.com/run/detail/southamerica-west1/time-track-dashboard/revisions?project=personal-dashboards-487913)

## Release Process

The project uses CalVer format (`YY.MM.DD`) via Git tags to automatically trigger Cloud Build deployments to Cloud Run.

To easily tag and release a new version based on today's date, run the following script from the root of the repository:

```bash
./scripts/release.sh
```

See the full [**Release Process Guide**](guides/release_process.md) for deeper step-by-step instructions.
