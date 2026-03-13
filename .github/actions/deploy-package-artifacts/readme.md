# 🚀 Deploy/Undeploy Package Artifacts GitHub Action

Deploy or undeploy all artifacts in a package from a JSON deploytask file in SAP BTP Integration Suite.

---

## ✨ Overview

This action processes a deployment task JSON file and sequentially deploys or undeploys each artifact using the SAP BTP Integration Suite REST API. It supports multiple artifact types (Integration Flows, Message Mappings, Script Collections, Value Mappings) and waits for each deployment/undeployment to complete before proceeding to the next artifact. The action reads an enhanced deploytask format that may include `loglevel` and `runtimes` metadata per entry (currently logged but not yet acted upon).

---

## ⚙️ Inputs

| Name         | Required | Description                                                     |
|--------------|----------|-----------------------------------------------------------------|
| bearer-token | ✅ Yes   | Bearer token to authenticate with SAP BTP APIs.                |
| btp-api-url  | ✅ Yes   | Base URL for SAP BTP Integration Suite APIs.                   |
| file         | ✅ Yes   | Path to JSON file containing deploytasks.                      |
| action       | ✅ Yes   | Deployment action: `Deploy` or `Undeploy`.                     |

---

## 📝 Usage Example

```yaml
jobs:
  deploy-artifacts:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy Package Artifacts
        uses: ./.github/actions/deploy-package-artifacts
        with:
          bearer-token: Bearer ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          file: ${{ runner.temp }}/DeployTask.my-package-001
          action: Deploy
```

---

## 📂 Input File Format

The action reads a deploytask JSON file. Integration flow entries may include optional `loglevel` and `runtimes` fields (resolved from the deployment configuration). Non-iFlow entries (mappings, script collections, etc.) contain only the base fields.

**DeployTask JSON Structure:**
```json
{
  "d": {
    "deploytasks": [
      {
        "id": "flow-id-001",
        "name": "My Integration Flow",
        "type": "Integration",
        "action": "deploy",
        "loglevel": "INFO",
        "runtimes": "iflmap"
      },
      {
        "id": "mapping-001",
        "name": "My Mapping",
        "type": "MessageMapping",
        "action": "deploy"
      }
    ],
    "packageid": "my-package-001",
    "packagename": "my-integration-package"
  }
}
```

| Field      | Required | Description                                                    |
|------------|----------|----------------------------------------------------------------|
| id         | ✅ Yes   | Artifact ID                                                    |
| name       | ✅ Yes   | Artifact name (for logging)                                    |
| type       | ✅ Yes   | Artifact type: `Integration`, `MessageMapping`, `ScriptCollection`, `ValueMapping` |
| action     | ✅ Yes   | Action: `deploy` or `undeploy`                                 |
| loglevel   | ❌ No    | Effective log level for the artifact (e.g., `INFO`, `ERROR`, `NONE`). Currently logged only. |
| runtimes   | ❌ No    | Effective runtimes for the artifact (e.g., `iflmap`, `eicmbag`). Currently logged only. |

---

## 📂 Outputs

This action has no formal outputs. It deploys/undeploys artifacts via BTP API and reports success/failure per artifact in the logs.

**Behavior:**
- **Deploy**: Sends POST to `Deploy${type}DesigntimeArtifact` API, then polls status until `STARTED` or `ERROR`
- **Undeploy**: Sends DELETE to `IntegrationRuntimeArtifacts`, then polls until 404 (undeployed)
- Waits up to 2 hours per artifact with exponential backoff polling

---

## 💡 Tips & Troubleshooting

- **Enhanced DeployTask Format**: The action now reads optional `loglevel` and `runtimes` fields from deploytask entries. These are logged during processing but not yet used for deployment logic (future enhancement).
- **Backward Compatibility**: Deploytask entries without `loglevel`/`runtimes` fields are fully supported. The action gracefully handles both old and new formats.
- **Sequential Processing**: Artifacts are deployed one at a time in the order they appear in the deploytask array. The order is determined by the upstream action (`add-iflows-for-deployment`) which sorts by effective Rank.
- **Exponential Backoff**: Status polling uses exponential backoff (1s, 2s, 4s, ... up to 60s max) with a total timeout of 2 hours per artifact.
- **Error Handling**: If an artifact deploys but enters `ERROR` state, the action logs it and continues with the next artifact rather than failing the entire workflow.
- **HTTP Status Codes**: Deploy expects 202 (Accepted); Undeploy expects 202 or 404. Other codes trigger an error exit.
- **Bearer Token**: Must include the `Bearer` prefix. Store as a GitHub secret.
- **jq Dependency**: The action checks for `jq` and installs it automatically if missing.

---

## 📄 License

This project is licensed under the Apache License 2.0.