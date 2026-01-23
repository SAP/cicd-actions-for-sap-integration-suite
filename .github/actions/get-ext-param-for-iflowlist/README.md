# 📋 Get External Parameter for a List of IFLOW IDs GitHub Action

Retrieve and export external parameters for integration flows from SAP BTP Integration Suite and generate a structured configuration file.

---

## ✨ Overview

This action queries the SAP BTP Integration Suite API to retrieve external parameters for each integration flow in a provided list. It makes individual API calls to fetch configuration details for each IFLOW, transforms and cleans the response data, and generates a consolidated JSON file containing all parameters organized by artifact. The resulting configuration file is structured for easy parameter management and can be used to sync parameters across environments or for documentation purposes.

---

## ⚙️ Inputs

| Name         | Required | Description                                                  |
|--------------|----------|--------------------------------------------------------------|
| bearer-token | ✅ Yes   | Bearer token to authenticate with SAP BTP APIs.              |
| btp-api-url  | ✅ Yes   | Base URL for the SAP BTP Integration Suite APIs.             |
| package-id   | ✅ Yes   | The package ID for the integration flows.                    |
| package-name | ✅ Yes   | The package name for the integration flows.                  |
| file         | ✅ Yes   | Path to JSON file containing IFLOW IDs and names.            |

---

## 📝 Usage Example

```yaml
jobs:
  export-parameters:
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
      
      - name: Export Parameters
        id: export-params
        uses: ./.github/actions/get-external-parameters
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          package-name: my-integration-package
          file: ${{ steps.get-iflows.outputs.iflows-file }}
      
      - name: Rename and Commit
        run: |
          mv ${{ steps.export-params.outputs.path }} \
             btp-insuite/IntegrationPackages/my-package~my-package-001/Configuration/ConfigParams_INTEGRATION_FLOW.json
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add btp-insuite/IntegrationPackages/
          git commit -m "Export IFLOW parameters from BTP"
          git push

  sync-parameters-across-envs:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Export Parameters from Dev
        id: dev-params
        uses: ./.github/actions/get-external-parameters
        with:
          bearer-token: ${{ secrets.BTP_DEV_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_DEV_API_URL }}
          package-id: my-package-001
          package-name: my-integration-package
          file: iflow-list.json
      
      - name: Export Parameters from Prod
        id: prod-params
        uses: ./.github/actions/get-external-parameters
        with:
          bearer-token: ${{ secrets.BTP_PROD_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_PROD_API_URL }}
          package-id: my-package-001
          package-name: my-integration-package
          file: iflow-list.json
      
      - name: Compare Parameters
        run: |
          echo "Dev Parameters:"
          jq . ${{ steps.dev-params.outputs.path }}
          echo ""
          echo "Prod Parameters:"
          jq . ${{ steps.prod-params.outputs.path }}
```

---

## 📂 Outputs

| Name | Description                                          |
|------|------------------------------------------------------|
| path | Path to the generated `ConfigParams_INTEGRATION_FLOW.json.tmp` file |

**Output File Structure:**
```json
{
  "PackageIntegrationFlowParameters": {
    "PackageName": "my-integration-package",
    "PackageID": "my-package-001",
    "Artifacts": [
      {
        "ArtifactID": "iflow-id-123",
        "ArtifactName": "My Integration Flow",
        "ArtifactType": "INTEGRATION_FLOW",
        "Parameters": [
          {
            "DataType": "string",
            "Description": "API Endpoint URL",
            "ParameterKey": "API_ENDPOINT",
            "ParameterValues": {
              "Default": "https://api.example.com"
            }
          },
          {
            "DataType": "integer",
            "Description": "Timeout in seconds",
            "ParameterKey": "TIMEOUT",
            "ParameterValues": {
              "Default": "30"
            }
          }
        ]
      }
    ]
  }
}
```

---

## 💡 Tips & Troubleshooting

- **Bearer Token**: Ensure your bearer token has sufficient permissions to query integration flow configurations. Store as a GitHub secret and pass as `Bearer ${{ secrets.BTP_BEARER_TOKEN }}`.
- **Input File Format**: The input file must contain IFLOWs in the BTP API response format with `.d.results[]` array containing objects with `Id` and `Name` fields.
- **API Calls**: The action makes individual API calls for each IFLOW. Large numbers of IFLOWs may result in longer execution times and potential rate limiting issues.
- **Parameter Transformation**: The action transforms BTP API response data:
  - Removes `__metadata` fields from the raw API response
  - Converts `ParameterValue` to nested `ParameterValues.Default` structure
  - Normalizes field order for consistency
- **Output File Location**: The temporary file is created at `{PACKAGENAME}~{PACKAGEID}/Configuration/ConfigParams_INTEGRATION_FLOW.json.tmp`. The `.tmp` suffix indicates it should be renamed or processed further.
- **Directory Creation**: The action automatically creates the `Configuration` directory if it doesn't exist.
- **Data Types**: Parameters include DataType information (string, integer, etc.) from the BTP configuration.
- **HTTP 200 Response**: The action expects HTTP 200 from the configuration API. Any other status code triggers an error and shows the response body for debugging.
- **Artifact Type**: All artifacts are classified as `INTEGRATION_FLOW` in the output. Modify the action if you need to support other artifact types.
- **Parameter Values Structure**: The output structure uses `ParameterValues.Default` to accommodate potential future support for environment-specific overrides.
- **Idempotent Operation**: Running this action multiple times generates fresh parameter exports from the current BTP environment state.
- **Environment-Specific Parameters**: Use separate action calls with different `bearer-token` and `btp-api-url` inputs to export parameters from different environments.
- **File Naming Convention**: The `.tmp` extension allows distinguishing temporary parameter exports from finalized configuration files. Rename appropriately in subsequent steps.
- **Empty Parameter Lists**: If an IFLOW has no external parameters, the `Parameters` array will be empty but the artifact entry will still be created.

---

## 📄 License

This project is licensed under the Apache License 2.0.