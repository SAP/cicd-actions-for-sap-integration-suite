# 🔍 Get CPI Package ID for IFlow GitHub Action

Retrieve the package ID for a specific integration flow from SAP BTP Integration Suite Design Time.

---

## ✨ Overview

This action queries the SAP BTP Integration Suite API to fetch metadata about a specific integration flow and extracts its associated package ID. It's useful for discovering which package contains a particular IFLOW or for dynamically determining package context during multi-package workflows. The action validates that the IFLOW exists and has a valid package association before returning the result.

---

## ⚙️ Inputs

| Name         | Required | Description                                           |
|--------------|----------|-------------------------------------------------------|
| bearer-token | ✅ Yes   | Bearer token to authenticate with SAP BTP APIs.       |
| btp-api-url  | ✅ Yes   | Base URL for the SAP BTP Integration Suite APIs.      |
| iflow-id     | ✅ Yes   | The integration flow ID to query for its package.     |

---

## 📝 Usage Example

```yaml
jobs:
  discover-package-context:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Get Package ID for IFlow
        id: get-pkg
        uses: ./.github/actions/get-package-id-for-iflow
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          iflow-id: my-iflow-123
      
      - name: Use Package ID in Workflow
        run: |
          echo "IFlow belongs to package: ${{ steps.get-pkg.outputs.packageID }}"
          echo "Proceeding with package-specific operations..."

  dynamic-package-operations:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Get Package for IFlow
        id: discover
        uses: ./.github/actions/get-package-id-for-iflow
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          iflow-id: iflow-to-deploy
      
      - name: Export Parameters
        uses: ./.github/actions/get-external-parameters
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: ${{ steps.discover.outputs.packageID }}
          package-name: discovered-package
          file: iflow-list.json
      
      - name: Get Package as ZIP
        uses: ./.github/actions/get-cpi-package-as-zip
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: ${{ steps.discover.outputs.packageID }}
          package-name: discovered-package

  multi-iflow-discovery:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Discover IFlow 1 Package
        id: iflow1
        uses: ./.github/actions/get-package-id-for-iflow
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          iflow-id: iflow-1
      
      - name: Discover IFlow 2 Package
        id: iflow2
        uses: ./.github/actions/get-package-id-for-iflow
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          iflow-id: iflow-2
      
      - name: Report Package Associations
        run: |
          echo "IFlow-1 belongs to: ${{ steps.iflow1.outputs.packageID }}"
          echo "IFlow-2 belongs to: ${{ steps.iflow2.outputs.packageID }}"
          if [ "${{ steps.iflow1.outputs.packageID }}" == "${{ steps.iflow2.outputs.packageID }}" ]; then
            echo "Both IFlows are in the same package"
          else
            echo "IFlows are in different packages"
          fi
```

---

## 📂 Outputs

| Name      | Description                                      |
|-----------|--------------------------------------------------|
| packageID | The package ID containing the specified IFLOW    |

**Output Format:**
The packageID is a simple string containing the package identifier. Example: `my-package-001`

**API Response Structure:**
The action extracts the PackageId from the BTP API response:
```json
{
  "d": {
    "Id": "iflow-id-123",
    "Name": "My Integration Flow",
    "PackageId": "my-package-001",
    "Version": "active"
  }
}
```

---

## 💡 Tips & Troubleshooting

- **Bearer Token**: Ensure your bearer token has read permissions for integration flow metadata. Store as a GitHub secret and pass as `Bearer ${{ secrets.BTP_BEARER_TOKEN }}`.
- **IFLOW ID Format**: Use the exact IFLOW ID from your BTP environment. IDs are typically alphanumeric strings without spaces.
- **HTTP 200 Response**: The action expects HTTP 200 for successful metadata retrieval. Any other status code triggers an error.
- **Authentication Failures**: If you receive HTTP 401, verify your bearer token is valid and not expired. Regenerate tokens in your BTP environment if needed.
- **Permission Issues**: If you receive HTTP 403, ensure your bearer token has read permissions for integration flows.
- **IFLOW Not Found**: If you receive HTTP 404, verify the IFLOW ID is correct and the IFLOW exists in your BTP environment.
- **Null Package ID**: If the IFLOW exists but has no associated PackageId, the action fails with a clear error message. This indicates a data inconsistency in BTP.
- **Dynamic Workflow Configuration**: Use this action to conditionally configure subsequent actions based on discovered package context.
- **Multi-IFLOW Workflows**: Chain multiple instances of this action to discover which packages contain multiple IFLOWs, useful for impact analysis.
- **Error Handling**: The action validates both HTTP response status and the presence of a valid PackageId before returning results, preventing downstream errors.
- **API Endpoint**: The action queries the `IntegrationDesigntimeArtifacts` endpoint with `Version='active'` to get the current active version metadata.
- **Idempotent Operation**: Running this action multiple times returns the same package ID, making it safe for repeated calls and conditional workflows.
- **Use with Other Actions**: The discovered packageID can be passed to downstream actions like `get-external-parameters` or `get-cpi-package-as-zip` for package-level operations.
- **Package Context Discovery**: Useful when you know an IFLOW ID but need to determine its package for subsequent operations.
- **Debugging**: Check the GitHub Actions log group output for detailed API response information to troubleshoot failures.

---

## 📄 License

This project is licensed under the Apache License 2.0.