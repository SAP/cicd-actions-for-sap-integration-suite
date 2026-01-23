# 📦 Get Object IDs of Package GitHub Action

Retrieve a list of artifact IDs for a specific object type from an SAP BTP Integration Suite package.

---

## ✨ Overview

This action queries the SAP BTP Integration Suite API to fetch a list of specific artifact types (Integration Flows, Value Mappings, Message Mappings, or Script Collections) from a designated package. It gracefully handles both successful retrievals and missing packages, returning an appropriately formatted JSON file with either the artifact list or an empty results array. The action is ideal for discovering what artifacts exist within a package before deployment or configuration operations.

---

## ⚙️ Inputs

| Name        | Required | Description                                                  |
|------------|----------|--------------------------------------------------------------|
| bearer-token | ✅ Yes   | Bearer token to authenticate with SAP BTP APIs.              |
| btp-api-url  | ✅ Yes   | Base URL for the SAP BTP Integration Suite APIs.             |
| package-id   | ✅ Yes   | The package ID to query for artifacts.                       |
| object-type  | ✅ Yes   | Artifact type to retrieve: `Integration`, `ValueMapping`, `MessageMapping`, or `ScriptCollection` |

---

## 📝 Usage Example

```yaml
jobs:
  get-package-artifacts:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Get Integration Flow IDs
        id: get-iflows
        uses: ./.github/actions/get-object-ids-of-package
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          object-type: Integration
      
      - name: Display Integration Flows
        run: |
          echo "Found Integration Flows:"
          jq '.d.results[] | {Id, Name}' ${{ steps.get-iflows.outputs.file }}

  multi-artifact-discovery:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Get All Artifact Types
        id: get-all
        run: |
          declare -a types=("Integration" "ValueMapping" "MessageMapping" "ScriptCollection")
          for type in "${types[@]}"; do
            echo "Querying $type artifacts..."
          done
      
      - name: Get Integration Flows
        id: iflows
        uses: ./.github/actions/get-object-ids-of-package
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          object-type: Integration
      
      - name: Get Value Mappings
        id: valuemaps
        uses: ./.github/actions/get-object-ids-of-package
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          object-type: ValueMapping
      
      - name: Get Script Collections
        id: scripts
        uses: ./.github/actions/get-object-ids-of-package
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          object-type: ScriptCollection
      
      - name: Inventory Report
        run: |
          echo "=== Package Artifact Inventory ==="
          echo "Integration Flows: $(jq '.d.results | length' ${{ steps.iflows.outputs.file }})"
          echo "Value Mappings: $(jq '.d.results | length' ${{ steps.valuemaps.outputs.file }})"
          echo "Script Collections: $(jq '.d.results | length' ${{ steps.scripts.outputs.file }})"
```

---

## 📂 Outputs

| Name | Description                                       |
|------|---------------------------------------------------|
| file | Path to JSON file containing artifact IDs and details |

**Output File Format (200 - Artifacts Found):**
```json
{
  "d": {
    "results": [
      {
        "Id": "artifact-id-123",
        "Name": "My Integration Flow",
        "Version": "active",
        "CreatedDate": "/Date(1640000000000)/",
        "ModifiedDate": "/Date(1640000000000)/"
      },
      {
        "Id": "artifact-id-456",
        "Name": "Another Integration Flow",
        "Version": "active",
        "CreatedDate": "/Date(1640000000000)/",
        "ModifiedDate": "/Date(1640000000000)/"
      }
    ]
  }
}
```

**Output File Format (404 - Package Not Found):**
```json
{
  "d": {
    "results": []
  }
}
```

---

## 💡 Tips & Troubleshooting

- **Bearer Token**: Ensure your bearer token has permissions to query integration artifacts. Store as a GitHub secret and pass as `Bearer ${{ secrets.BTP_BEARER_TOKEN }}`.
- **Object Types**: The action supports four artifact types. Use exact casing: `Integration`, `ValueMapping`, `MessageMapping`, `ScriptCollection`. These map to BTP API endpoints like `IntegrationDesigntimeArtifacts`.
- **Package IDs**: Use the exact package ID from your BTP environment. The ID is typically found in the package URL or management interface.
- **HTTP 200 Response**: Indicates the package was found and its artifacts are being returned. The response may include zero or more artifacts.
- **HTTP 404 Response**: Indicates the package doesn't exist in the BTP environment. The action gracefully creates an empty JSON file with zero results instead of failing.
- **Other HTTP Status Codes**: Any response code other than 200 or 404 triggers an error. Common error codes include 401 (unauthorized), 403 (forbidden), 500 (server error).
- **Authentication Failures**: If you receive HTTP 401, verify your bearer token is valid and not expired. Regenerate tokens in your BTP environment if needed.
- **Empty Results**: If a package exists but has no artifacts of the requested type, the results array will be empty but the file will still be valid JSON.
- **Output File Location**: The file is created in `${{ runner.temp }}` with the naming pattern `{OBJECTTYPE}DesigntimeArtifacts.{PACKAGEID}`.
- **Artifact Details**: Returned artifacts include ID, Name, Version, and creation/modification timestamps. Use downstream actions or jq to extract specific fields.
- **API Endpoint Construction**: The action constructs the API URL as `/api/v1/IntegrationPackages('{PACKAGEID}')/{OBJECTTYPE}DesigntimeArtifacts`.
- **Downstream Processing**: Use the output file with other actions like `create-iflow-deployment-file` or `get-external-parameters` that expect artifact ID lists.
- **Multiple Artifact Types**: Run multiple instances of this action (one per artifact type) to get a complete inventory of all artifacts in a package.
- **Idempotent Operation**: Running this action multiple times returns the current state of artifacts from BTP, making it safe for repeated calls.

---

## 📄 License

This project is licensed under the Apache License 2.0.