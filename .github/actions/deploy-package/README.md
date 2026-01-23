# 🚀 Deploy/Undeploy Package Artifacts GitHub Action

Deploy or undeploy all artifacts in a package from a JSON deployment task file to SAP BTP Integration Suite.

---

## ✨ Overview

This action orchestrates the deployment and undeployment of integration artifacts to SAP BTP Integration Suite. It reads a JSON file containing deployment tasks with artifact details, sends deployment or undeployment requests to the BTP APIs, and polls for completion status. The action supports exponential backoff polling with a maximum wait time of 2 hours, handles both deployment success (STARTED status) and undeployment verification (404 response), and provides detailed logging throughout the process.

---

## ⚙️ Inputs

| Name        | Required | Description                                                          |
|------------|----------|----------------------------------------------------------------------|
| bearer-token | ✅ Yes   | Bearer token with authorization to deploy/undeploy artifacts.        |
| btp-api-url  | ✅ Yes   | Base URL for the BTP Integration Suite API.                          |
| file        | ✅ Yes   | Path to JSON file containing deploytasks (from Create CSV action).   |
| action      | ✅ Yes   | Deployment action: `Deploy` or `Undeploy`.                           |

---

## 📝 Usage Example

```yaml
jobs:
  deploy-artifacts:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Deploy Package Artifacts
        uses: ./.github/actions/deploy-undeploy-artifacts
        with:
          bearer-token: Bearer ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          file: deployment-tasks.json
          action: Deploy

  undeploy-artifacts:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Undeploy Package Artifacts
        uses: ./.github/actions/deploy-undeploy-artifacts
        with:
          bearer-token: Bearer ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          file: deployment-tasks.json
          action: Undeploy
```

---

## 📂 Outputs

This action has no outputs. It performs deployment/undeployment operations via BTP APIs and returns only exit status.

**Expected Input File Format:**
```json
{
  "d": {
    "deploytasks": [
      {
        "id": "artifact-id-123",
        "name": "My Integration Flow",
        "type": "Integration",
        "action": "Deploy"
      },
      {
        "id": "artifact-id-456",
        "name": "My REST Endpoint",
        "type": "RestEndpoint",
        "action": "Deploy"
      }
    ]
  }
}
```

**Side Effects:**
- Sends POST requests to `Deploy{Type}DesigntimeArtifact` API for deployment
- Sends DELETE requests to `IntegrationRuntimeArtifacts` API for undeployment
- Polls artifact status until completion (STARTED/ERROR for deploy, 404 for undeploy)
- Creates temporary body.json file for JSON parsing during polling

---

## 💡 Tips & Troubleshooting

- **Bearer Token Format**: Include the `Bearer` prefix in your token. Store full `Bearer xyz...` in GitHub secrets or format as `Bearer ${{ secrets.TOKEN }}` in the input.
- **Action Parameter**: Use exact casing - `Deploy` or `Undeploy` (capital first letter). The action is case-insensitive internally but input validation expects these values.
- **Artifact Types**: The `type` field in deploytasks determines the API endpoint. Common types include `Integration`, `RestEndpoint`, `SOAP`. The action constructs `Deploy{Type}DesigntimeArtifact` endpoint.
- **Deployment Status**: For deployment, the action waits until the artifact status is either `STARTED` (success) or `ERROR` (treated as success—continue processing).
- **Undeployment Status**: For undeployment, the action waits until the artifact returns a 404 response, indicating successful removal from runtime.
- **Maximum Wait Time**: The action polls for up to 2 hours (7200 seconds) before timing out. Large deployments may require this full duration.
- **Exponential Backoff**: Wait times start at 1 second and double with each poll, maxing out at 60 seconds between checks. This reduces API load during long waits.
- **jq Dependency**: The action requires `jq` for JSON parsing. If not available, it installs via apt-get automatically.
- **JSON Validation**: Input file is validated for JSON syntax before processing. Invalid JSON causes immediate failure.
- **Error Handling**: HTTP status codes other than 202 (for deployment request) or 202/404 (for polling) trigger immediate failure.
- **Empty Deployment Lists**: If the deploytasks array is empty, the action exits gracefully with code 0.
- **Concurrent Artifacts**: Each artifact is processed sequentially within a single workflow run. For parallel deployments, use multiple workflow runs.
- **Deployment Logs**: Detailed logging includes API endpoints, HTTP status codes, response bodies on errors, and elapsed time for status polling.

---

## 📄 License

This project is licensed under the Apache License 2.0.