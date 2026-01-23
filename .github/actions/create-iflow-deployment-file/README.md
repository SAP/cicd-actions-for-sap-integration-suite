# 📄 Create IFlow Deployment File GitHub Action

Create and merge integration flow deployment configuration files for SAP BTP Integration Suite packages.

---

## ✨ Overview

This action creates or updates a deployment configuration file for integration flows within a package directory structure. It reads a JSON file containing integration flow IDs from BTP APIs, intelligently merges with existing deployment configurations to preserve stage-specific settings, and generates a structured `Deployment_INTEGRATION_FLOW.json` file. New iFlows default to `Deploy: false`, requiring explicit configuration before deployment, while existing entries retain all their original settings and stage flags.

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

**Output File Structure:**
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
        "DEV": "true",
        "TST": "false",
        "PRD": "false"
      }
    ]
  }
}
```

---

## 💡 Tips & Troubleshooting

- **Merge Logic**: The action intelligently preserves existing deployment entries. If an iFlow already exists in the deployment file, all its settings (including stage-specific flags like DEV, TST, PRD) are retained. Only the `ArtifactName` is updated if it changed in the source.
- **New Entries Default**: New iFlows are created with `Deploy: "false"` by default. This prevents accidental deployments. Edit the deployment file to set `Deploy: "true"` and configure stage-specific flags as needed.
- **Directory Structure**: The action creates the directory structure `{PackageName}~{PackageID}/Configuration/` in the `btp-insuite/IntegrationPackages` directory. Ensure this path exists or the action will create it.
- **Bearer Token**: The bearer token must have sufficient permissions to query BTP Integration Suite APIs. Typically stored as a GitHub secret.
- **Input File Format**: The input file must contain iFlows data in the BTP API response format with `d.results[]` array containing objects with `Id` and `Name` fields.
- **Idempotent Operation**: Running this action multiple times with the same input is safe—existing entries are preserved unchanged, and only new iFlows are added.
- **Stage Flags**: If you need environment-specific deployments (DEV, TST, PRD, etc.), manually add these keys to the JSON after initial creation. They will be preserved on subsequent runs.
- **Working Directory**: This action runs in the `btp-insuite/IntegrationPackages` directory. Ensure your repository structure matches this path.
- **Processing Summary**: The action logs processing statistics showing total iFlows processed, preserved entries, and new entries with defaults for audit purposes.

---

## 📄 License

This project is licensed under the Apache License 2.0.