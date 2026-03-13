# 🚀 Pass iFlow JSON with IDs to be added for Deployment GitHub Action

Process deployment configuration file and add integration flows marked for deployment or undeployment in SAP BTP Integration Suite.

---

## ✨ Overview

This action manages the deployment and undeployment of integration flows for SAP BTP Integration Suite. It reads a package's deployment configuration file, processes integration flows based on stage-specific deployment settings for a target environment, and generates a deployment task file. The action supports both deployment and undeployment modes, with an enhanced **Default vs. Override** pattern: top-level fields (`Deploy`, `LogLevel`, `Runtimes`) serve as defaults, while an optional `Environments` block can override these per target environment. `Rank` is a package-global setting and is only defined at the top level (not overridable per environment). The old flat-key format (e.g., `"DEV": "true"`) is still fully supported for backward compatibility.

---

## ⚙️ Inputs

| Name              | Required | Description                                                                    |
|-------------------|----------|--------------------------------------------------------------------------------|
| package-id        | ✅ Yes   | The package ID for deployment.                                                 |
| package-name      | ✅ Yes   | The package name for deployment.                                               |
| file              | ✅ Yes   | Input file containing artifact IDs (used in undeploy mode).                    |
| mode              | ✅ Yes   | Deployment mode: `deploy` or `undeploy`.                                       |
| target-env        | ✅ Yes   | Target environment (e.g., `DEV`, `TST`, `PRD`, `POC`).                        |
| exclude-iflow-ids | ❌ No    | Comma-separated list of IFLOW IDs to exclude from deployment (default: "").   |

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
          exclude-iflow-ids: "IFLOW_TO_SKIP_1,IFLOW_TO_SKIP_2"  # Optional: exclude specific IFLOWs

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
- Each iFlow entry includes: artifact ID, name, type (`Integration`), action (`deploy` or `undeploy`), effective `loglevel`, and effective `runtimes`. Non-iFlow entries (from `merge-ids-for-deployment`) contain only ID, name, type, and action.
- `loglevel` and `runtimes` are resolved using the same priority chain as Deploy: `Environments[$TARGET_ENV].LogLevel` → top-level `LogLevel` → `"INFO"` (and similarly for Runtimes → `"iflmap"`)

**Output Structure Example:**
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

---

## 💡 Tips & Troubleshooting

- **Deploy Mode Logic (Priority Chain)**: The deploy decision follows a three-level priority chain:
  1. **`Environments[$TARGET_ENV].Deploy`** — Enhanced format override (highest priority)
  2. **`$TARGET_ENV` flat key** — Old format (e.g., `"DEV": "true"`) for backward compatibility
  3. **`Deploy`** — Default fallback
  
  This means you can use the new `Environments` block for fine-grained control, or continue using the old flat-key format — both work.
- **Rank Sorting**: Integration flows are sorted by effective Rank before processing. Rank is a package-global setting defined at the top level of each iFlow entry (not overridable per environment). Unranked flows are deployed first (alphabetically), then ranked flows in ascending order.
- **Enhanced JSON Format Example**:
  ```json
  {
    "ArtifactID": "my-iflow-001",
    "ArtifactName": "My Integration Flow",
    "Deploy": "true",
    "Rank": "100",
    "LogLevel": "INFO",
    "Runtimes": "iflmap",
    "Environments": {
      "DEV": { "Deploy": "true", "LogLevel": "INFO" },
      "TST": { "Deploy": "true" },
      "PRD": { "Deploy": "false", "LogLevel": "ERROR" }
    }
  }
  ```
  In this example, deploying to `DEV` uses `Deploy=true` with `Rank=100` (from top level) and `LogLevel=INFO`, while `PRD` uses `Deploy=false` and would be skipped. Note that `Rank` is only defined at the top level and applies globally across all environments.
- **LogLevel & Runtimes Resolution**: The effective `LogLevel` and `Runtimes` for each iFlow are resolved using the same priority chain: `Environments[$TARGET_ENV].LogLevel` → top-level `LogLevel` → `"INFO"` (and `Environments[$TARGET_ENV].Runtimes` → top-level `Runtimes` → `"iflmap"`). These values are included in the deploytask output for downstream consumption.
- **Package Directory Format**: Ensure your package directory follows the naming convention `*~${PACKAGE_ID}` in the `btp-insuite/IntegrationPackages` directory.
- **Backward Compatibility**: Both old format (flat keys like `"DEV": "true"`) and new format (`Environments` block) are supported. You can even mix both in the same file — each iFlow is resolved independently.
- **Configuration File Required**: For deploy mode, the package must contain `Configuration/Deployment_INTEGRATION_FLOW.json`. If missing, the action exits gracefully.
- **Environment Variables**: Target environment names are case-sensitive. Use uppercase values (e.g., `DEV`, `TST`, `PRD`, `POC`) to match your configuration file keys.
- **Undeploy Mode**: Requires the input file to contain artifact IDs under the `.d.results[]` path.
- **Duplicate Prevention**: The action automatically checks for duplicates before adding. Identical entries are skipped.
- **Exclude IFLOW IDs**: Use the `exclude-iflow-ids` parameter to skip specific integration flows from deployment, even if they are marked for deployment in the configuration file. This is useful for temporarily excluding problematic flows during releases.
- **Working Directory**: The action executes in `btp-insuite/IntegrationPackages` directory. Ensure relative paths are adjusted accordingly.
- **Error Handling**: The action uses `set +e` to continue processing even if individual steps encounter errors. Check the logs for detailed error messages.
- **Summary Output**: The action provides deployment/undeployment summaries showing total processed and skipped artifacts.

---

## 📄 License

This project is licensed under the Apache License 2.0.