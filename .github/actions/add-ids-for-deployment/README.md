# 🚀 Add IDs for Deployment GitHub Action

Passes a JSON file with artifact IDs to be added to a deployment task file for SAP BTP Integration Suite CI/CD pipelines.

---

## ✨ Overview

This action reads a JSON file containing artifact IDs and appends them to a deployment task file located at `.github/actions/perform-deployment/data/$STAGE/DeployTask.${PACKAGEID}`. The action automatically detects the artifact type from the input filename, creates the output file structure if it doesn't exist, and ensures only unique IDs are added to prevent duplicates.

---

## ⚙️ Inputs

| Name        | Required | Description                                                    |
|-------------|----------|----------------------------------------------------------------|
| PACKAGEID   | ✅ Yes   | The package ID for deployment.                                  |
| PACKAGENAME | ✅ Yes   | The package name for deployment.                                |
| FILE        | ✅ Yes   | Path to the JSON file containing artifact IDs to deploy.        |
| STAGE       | ✅ Yes   | The deployment stage (e.g., `dev`, `staging`, `prod`).          |

---

## 📝 Usage Example

```yaml
jobs:
  add-deployment-ids:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Add IDs for Deployment
        uses: ./.github/actions/add-ids-for-deployment
        with:
          PACKAGEID: my-package-001
          PACKAGENAME: my-integration-package
          FILE: artifacts/DesigntimeArtifactsIntegrationFlow.json
          STAGE: dev
```

---

## 📂 Outputs

- Creates/updates `.github/actions/perform-deployment/data/$STAGE/DeployTask.${PACKAGEID}` with deployment task entries
- Each entry includes: artifact ID, name, type (auto-detected from filename), action type (`Deploy`), package ID, and package name
- Output is structured as JSON with deployment task array

**Output Structure Example:**
```json
{
  "d": {
    "deploytasks": [
      {
        "id": "artifact-id-123",
        "name": "Artifact Display Name",
        "type": "IntegrationFlow",
        "action": "Deploy"
      }
    ],
    "packageid": "my-package-001",
    "packagename": "my-integration-package"
  }
}
```

---

## 💡 Tips & Troubleshooting

- **File Not Found**: Ensure the `FILE` path is correct and the file exists in your repository before calling this action.
- **No IDs Found**: If the JSON structure doesn't match `.d.results[]`, the action will exit gracefully without error. Verify your JSON format contains IDs under `d.results`.
- **Artifact Type Detection**: The action extracts the artifact type by removing `DesigntimeArtifacts` from the filename. Ensure your input filenames follow this convention (e.g., `DesigntimeArtifactsIntegrationFlow.json` → type: `IntegrationFlow`).
- **Duplicate Prevention**: The action automatically checks for duplicates before adding. If an entry with the same ID, name, type, and action already exists, it won't be added again.
- **Directory Creation**: Parent directories are automatically created if missing—no manual setup required.
- **jq Dependency**: This action uses `jq` for JSON parsing. Ensure your runner has `jq` installed (included by default on `ubuntu-latest`).

---

## 📄 License

This project is licensed under the Apache License 2.0.
