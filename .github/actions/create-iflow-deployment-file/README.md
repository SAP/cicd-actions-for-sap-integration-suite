# 📄 Create IFlow Deployment File GitHub Action

Create and merge integration flow deployment configuration files for SAP BTP Integration Suite packages.

---

## ✨ Overview

This action creates or updates a deployment configuration file for integration flows within a package directory structure. It reads a JSON file containing integration flow IDs from BTP APIs, intelligently merges with existing deployment configurations to preserve stage-specific settings, and generates a structured `Deployment_INTEGRATION_FLOW.json` file. New iFlows are created with sensible defaults (`Deploy: false`, `Rank: 100`, `LogLevel: INFO`, `Runtimes: iflmap`), requiring explicit configuration before deployment. Existing entries retain all their original settings and stage flags, while missing fields are backfilled with defaults.

---

## ⚙️ Inputs

| Name         | Required | Description                                          |
|--------------|----------|------------------------------------------------------|
| bearer-token | ✅ Yes   | Bearer token to authenticate with SAP BTP APIs.      |
| btp-api-url  | ✅ Yes   | Base URL for SAP BTP Integration Suite APIs.         |
| package-id   | ✅ Yes   | The package ID for the integration flows.            |
| package-name | ✅ Yes   | The package name for the integration flows.          |
| file         | ✅ Yes   | Path to JSON file containing iFlow IDs from BTP API. |

---

## 📝 Usage Example

```yaml
jobs:
  create-deployment-config:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Get IFlow IDs from BTP
        id: get-iflows
        uses: ./.github/actions/get-iflow-ids
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
      
      - name: Create IFlow Deployment File
        id: create-deployment
        uses: ./.github/actions/create-iflow-deployment-file
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          package-name: my-integration-package
          file: ${{ steps.get-iflows.outputs.iflows-file }}
      
      - name: Commit Deployment File
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add ${{ steps.create-deployment.outputs.path }}
          git commit -m "Update deployment configuration"
          git push
```

---

## 📂 Outputs

| Name | Description                                    |
|------|------------------------------------------------|
| path | Path to the generated `Deployment_INTEGRATION_FLOW.json` file |

**Output File Structure (defaults created by this action):**
```json
{
  "PackageIntegrationFlowDeployments": {
    "PackageName": "my-integration-package",
    "PackageID": "my-package-001",
    "IntegrationFlows": [
      {
        "ArtifactID": "iflow-id-123",
        "ArtifactName": "My Integration Flow",
        "Deploy": "false",
        "Rank": "100",
        "LogLevel": "INFO",
        "Runtimes": "iflmap"
      }
    ]
  }
}
```

**Enhanced Format (manually configured after initial creation):**

The deployment file supports an optional `Environments` block per iFlow for environment-specific overrides. Top-level fields serve as **defaults**, while values inside `Environments` **override** them for the target environment:

```json
{
  "ArtifactID": "iflow-id-123",
  "ArtifactName": "My Integration Flow",
  "Deploy": "true",
  "Rank": "100",
  "LogLevel": "INFO",
  "Runtimes": "iflmap",
  "Environments": {
    "DEV": { "Deploy": "true", "LogLevel": "DEBUG", "Runtimes": "iflmap" },
    "TST": { "Deploy": "true", "LogLevel": "INFO", "Runtimes": "iflmap" },
    "PRD": { "Deploy": "false", "LogLevel": "ERROR", "Runtimes": "iflmap" }
  }
}
```

> **Note:** This action only creates the default top-level fields. The `Environments` sub-structures must be added manually after initial creation. The old flat-key format (e.g., `"DEV": "true"`) is still supported for backward compatibility.

---

## 💡 Tips & Troubleshooting

- **Merge Logic**: The action intelligently preserves existing deployment entries. If an iFlow already exists in the deployment file, all its settings (including stage-specific flags like DEV, TST, PRD) are retained. Only the `ArtifactName` is updated if it changed in the source.
- **New Entries Default**: New iFlows are created with the following defaults: `Deploy: "false"`, `Rank: "100"`, `LogLevel: "INFO"`, `Runtimes: "iflmap"`. This prevents accidental deployments. Edit the deployment file to adjust these values and configure stage-specific flags as needed.
- **Rank**: Controls the deployment order of integration flows. Flows are sorted by rank (lower values deploy first). Unranked flows are deployed before ranked ones.
- **LogLevel**: Sets the default log level for the integration flow (e.g., `INFO`, `DEBUG`, `ERROR`, `TRACE`).
- **Runtimes**: Specifies the runtime environment for the integration flow (default: `iflmap`).
- **Directory Structure**: The action creates the directory structure `{PackageName}~{PackageID}/Configuration/` in the `btp-insuite/IntegrationPackages` directory. Ensure this path exists or the action will create it.
- **Bearer Token**: The bearer token must have sufficient permissions to query BTP Integration Suite APIs. Typically stored as a GitHub secret.
- **Input File Format**: The input file must contain iFlows data in the BTP API response format with `d.results[]` array containing objects with `Id` and `Name` fields.
- **Idempotent Operation**: Running this action multiple times with the same input is safe—existing entries are preserved unchanged, and only new iFlows are added.
- **Backfill Logic**: Existing entries from older deployment files that lack `Rank`, `LogLevel`, or `Runtimes` fields will automatically have these fields added with their default values on the next run, without overwriting any existing values.
- **Stage Flags (Legacy)**: The old flat-key format (e.g., `"DEV": "true"`) is still supported for backward compatibility and will be preserved on subsequent runs.
- **Environments Block (Enhanced)**: For fine-grained per-environment control of Deploy, LogLevel, and Runtimes, manually add an `Environments` sub-object to each iFlow entry. Note that `Rank` is a package-global setting and cannot be overridden per environment. This block is not created automatically — it must be configured manually. Existing `Environments` blocks are preserved on subsequent runs.
- **Working Directory**: This action runs in the `btp-insuite/IntegrationPackages` directory. Ensure your repository structure matches this path.
- **Processing Summary**: The action logs processing statistics showing total iFlows processed, preserved entries, and new entries with defaults for audit purposes.

---

## 📄 License

This project is licensed under the Apache License 2.0.