# 🚀 Pass iFlow JSON with IDs to be added for Deployment GitHub Action

Process deployment configuration file and add integration flows marked for deployment or undeployment in SAP BTP Integration Suite.

---

## ✨ Overview

This action manages the deployment and undeployment of integration flows for SAP BTP Integration Suite. It reads a package's deployment configuration file, processes integration flows based on stage-specific deployment settings for a target environment, and generates a deployment task file. The action supports both deployment and undeployment modes, with intelligent fallback logic for stage-specific environment configurations.

---

## ⚙️ Inputs

| Name           | Required | Description                                                                    |
|----------------|----------|--------------------------------------------------------------------------------|
| package-id     | ✅ Yes   | The package ID for deployment.                                                 |
| package-name   | ✅ Yes   | The package name for deployment.                                                |
| file           | ✅ Yes   | Input file containing artifact IDs (used in undeploy mode).                    |
| mode           | ✅ Yes   | Deployment mode: `deploy` or `undeploy`.                                       |
| target-env     | ✅ Yes   | Target environment (e.g., `DEV`, `TST`, `PRD`, `POC`).                        |

---

## 📝 Usage Example

```yaml
jobs:
  add-iflows-deployment:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Add iFlows for Deployment
        uses: ./.github/actions/add-iflows-for-deployment
        with:
          package-id: my-package-001
          package-name: my-integration-package
          file: artifacts/DesigntimeArtifactsIntegrationFlow.json
          mode: deploy
          target-env: DEV

  remove-iflows-deployment:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Remove iFlows from Deployment
        uses: ./.github/actions/add-iflows-for-deployment
        with:
          package-id: my-package-001
          package-name: my-integration-package
          file: artifacts/DesigntimeArtifactsIntegrationFlow.json
          mode: undeploy
          target-env: PRD
```

---

## 📂 Outputs

- Creates deployment task file at `${{ runner.temp }}/DeployTask.${PACKAGEID}` with integration flow deployment configurations
- **Deploy mode**: Processes flows from package's `Configuration/Deployment_INTEGRATION_FLOW.json` file based on target environment settings
- **Undeploy mode**: Processes flows from the provided input file for undeployment
- Each entry includes: artifact ID, name, type (`Integration`), action (`deploy` or `undeploy`), package ID, and package name

**Output Structure Example:**
```json
{
  "d": {
    "deploytasks": [
      {
        "id": "flow-id-001",
        "name": "My Integration Flow",
        "type": "Integration",
        "action": "deploy"
      }
    ],
    "packageid": "my-package-001",
    "packagename": "my-integration-package"
  }
}
```

---

## 💡 Tips & Troubleshooting

- **Deploy Mode Logic**: The action uses stage-specific settings if available for the target environment. If not found, it falls back to the default `Deploy` flag. This allows per-environment control of integration flow deployments.
- **Package Directory Format**: Ensure your package directory follows the naming convention `*~${PACKAGE_ID}` in the `btp-insuite/IntegrationPackages` directory.
- **Configuration File Required**: For deploy mode, the package must contain `Configuration/Deployment_INTEGRATION_FLOW.json`. If missing, the action exits gracefully.
- **Environment Variables**: Target environment names are case-sensitive. Use uppercase values (e.g., `DEV`, `TST`, `PRD`, `POC`) to match your configuration file keys.
- **Undeploy Mode**: Requires the input file to contain artifact IDs under the `.d.results[]` path.
- **Duplicate Prevention**: The action automatically checks for duplicates before adding. Identical entries are skipped.
- **Working Directory**: The action executes in `btp-insuite/IntegrationPackages` directory. Ensure relative paths are adjusted accordingly.
- **Error Handling**: The action uses `set +e` to continue processing even if individual steps encounter errors. Check the logs for detailed error messages.
- **Summary Output**: The action provides deployment/undeployment summaries showing total processed and skipped artifacts.

---

## 📄 License

This project is licensed under the Apache License 2.0.