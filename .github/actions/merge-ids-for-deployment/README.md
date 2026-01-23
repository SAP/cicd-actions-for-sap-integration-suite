# 🔀 Pass JSON with IDs to be Merged for Deployment GitHub Action

Merge artifact IDs from a JSON file into a local deployment task file for deploy or undeploy operations.

---

## ✨ Overview

This action reads a JSON file containing artifact IDs (typically from the `get-object-ids-of-package` action) and merges them into a deployment task file. It automatically detects the artifact type from the filename, creates or updates a deployment task JSON structure, and prevents duplicate entries based on artifact ID, name, type, and action. The action supports both deployment and undeployment modes, making it suitable for bidirectional lifecycle management of integration artifacts.

---

## ⚙️ Inputs

| Name        | Required | Description                                                    |
|-------------|----------|----------------------------------------------------------------|
| package-id  | ✅ Yes   | The package ID for deployment.                                  |
| package-name | ✅ Yes   | The package name for deployment.                                |
| file        | ✅ Yes   | Path to JSON file from get-object-ids-of-package action.       |
| mode        | ✅ Yes   | Deployment mode: `Deploy` or `Undeploy`.                       |

---

## 📝 Usage Example

```yaml
jobs:
  merge-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Get OAuth Token
        id: auth
        uses: ./.github/actions/get-oauth-token
        with:
          btp-api-user: ${{ secrets.BTP_API_USER }}
          btp-tec-user: ${{ secrets.BTP_TEC_USER }}
          btp-token-url: ${{ secrets.BTP_TOKEN_URL }}
          BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
          BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}
      
      - name: Get Integration Flows
        id: iflows
        uses: ./.github/actions/get-object-ids-of-package
        with:
          bearer-token: ${{ steps.auth.outputs.token }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          object-type: Integration
      
      - name: Merge for Deployment
        id: merge
        uses: ./.github/actions/merge-ids-for-deployment
        with:
          package-id: my-package-001
          package-name: my-integration-package
          file: ${{ steps.iflows.outputs.file }}
          mode: Deploy
      
      - name: Deploy Artifacts
        uses: ./.github/actions/deploy-undeploy-artifacts
        with:
          bearer-token: ${{ steps.auth.outputs.token }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          file: ${{ runner.temp }}/DeployTask.my-package-001
          action: Deploy

  multi-artifact-merge:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Get Token
        id: token
        uses: ./.github/actions/get-oauth-token
        with:
          btp-api-user: ${{ secrets.BTP_API_USER }}
          btp-tec-user: ${{ secrets.BTP_TEC_USER }}
          btp-token-url: ${{ secrets.BTP_TOKEN_URL }}
          BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
          BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}
      
      - name: Get Integration Flows
        id: iflows
        uses: ./.github/actions/get-object-ids-of-package
        with:
          bearer-token: ${{ steps.token.outputs.token }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          object-type: Integration
      
      - name: Get Value Mappings
        id: valuemaps
        uses: ./.github/actions/get-object-ids-of-package
        with:
          bearer-token: ${{ steps.token.outputs.token }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          object-type: ValueMapping
      
      - name: Get Message Mappings
        id: msgmaps
        uses: ./.github/actions/get-object-ids-of-package
        with:
          bearer-token: ${{ steps.token.outputs.token }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          object-type: MessageMapping
      
      - name: Merge Integration Flows
        id: merge-iflows
        uses: ./.github/actions/merge-ids-for-deployment
        with:
          package-id: my-package-001
          package-name: my-integration-package
          file: ${{ steps.iflows.outputs.file }}
          mode: Deploy
      
      - name: Merge Value Mappings
        id: merge-valuemaps
        uses: ./.github/actions/merge-ids-for-deployment
        with:
          package-id: my-package-001
          package-name: my-integration-package
          file: ${{ steps.valuemaps.outputs.file }}
          mode: Deploy
      
      - name: Merge Message Mappings
        id: merge-msgmaps
        uses: ./.github/actions/merge-ids-for-deployment
        with:
          package-id: my-package-001
          package-name: my-integration-package
          file: ${{ steps.msgmaps.outputs.file }}
          mode: Deploy
      
      - name: Deploy All Artifacts
        uses: ./.github/actions/deploy-undeploy-artifacts
        with:
          bearer-token: ${{ steps.token.outputs.token }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          file: ${{ runner.temp }}/DeployTask.my-package-001
          action: Deploy

  undeploy-workflow:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Get Token
        id: token
        uses: ./.github/actions/get-oauth-token
        with:
          btp-api-user: ${{ secrets.BTP_API_USER }}
          btp-tec-user: ${{ secrets.BTP_TEC_USER }}
          btp-token-url: ${{ secrets.BTP_TOKEN_URL }}
          BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
          BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}
      
      - name: Get Integration Flows
        id: iflows
        uses: ./.github/actions/get-object-ids-of-package
        with:
          bearer-token: ${{ steps.token.outputs.token }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          object-type: Integration
      
      - name: Merge for Undeployment
        uses: ./.github/actions/merge-ids-for-deployment
        with:
          package-id: my-package-001
          package-name: my-integration-package
          file: ${{ steps.iflows.outputs.file }}
          mode: Undeploy
      
      - name: Undeploy Artifacts
        uses: ./.github/actions/deploy-undeploy-artifacts
        with:
          bearer-token: ${{ steps.token.outputs.token }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          file: ${{ runner.temp }}/DeployTask.my-package-001
          action: Undeploy
```

---

## 📂 Outputs

This action has no explicit outputs. It creates/updates a deployment task file in the temporary directory.

**Side Effects:**
- Creates or updates `${{ runner.temp }}/DeployTask.${PACKAGEID}` file
- File contains merged deployment tasks with all artifacts

**Output File Structure:**
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
        "id": "valuemap-id-456",
        "name": "My Value Mapping",
        "type": "ValueMapping",
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

- **Input File Format**: The input file must contain artifact IDs in the BTP API response format with `.d.results[]` array containing objects with `Id` and `Name` fields.

- **Artifact Type Detection**: The action automatically extracts artifact type from the input filename by removing the `DesigntimeArtifacts` prefix. Examples:
  - `IntegrationDesigntimeArtifacts.pkg-001` → type: `Integration`
  - `ValueMappingDesigntimeArtifacts.pkg-001` → type: `ValueMapping`
  - `MessageMappingDesigntimeArtifacts.pkg-001` → type: `MessageMapping`
  - `ScriptCollectionDesigntimeArtifacts.pkg-001` → type: `ScriptCollection`

- **File Not Found**: If the input file doesn't exist, the action exits with error code 1 and displays a clear error message.

- **Empty Results**: If the input file contains no artifact IDs (empty `.d.results[]` array), the action exits gracefully without creating a deployment task file.

- **Output Location**: The deployment task file is created in `${{ runner.temp }}` with filename `DeployTask.${PACKAGEID}`.

- **Duplicate Prevention**: The action checks for duplicates using all four fields:
  - `id`: Artifact ID
  - `name`: Artifact name
  - `type`: Artifact type
  - `action`: Deploy or Undeploy mode
  
  If all four match, the entry is skipped to prevent duplicates.

- **Mode Parameter**: Use exact casing - `Deploy` or `Undeploy` (capital first letter). This value is stored in the deployment task's `action` field.

- **Multi-Artifact Merging**: You can run this action multiple times with different artifact types, and they will all be merged into the same `DeployTask.${PACKAGEID}` file with preserved uniqueness.

- **Incremental Merging**: Each run of this action either creates a new deployment task file or appends to an existing one without duplicating entries.

- **Display Output**: The action displays the final deployment task file contents on stdout for verification and debugging.

- **Temporary File Cleanup**: The deployment task file is created in `${{ runner.temp }}`, which is cleaned up after the workflow run unless explicitly preserved.

- **Downstream Integration**: Use the output file path with the `deploy-undeploy-artifacts` action to execute the deployment tasks.

- **jq Dependency**: The action uses `jq` for JSON parsing and transformation. Ensure your runner has jq installed (included by default on ubuntu-latest).

- **Error Handling**: If jq parsing fails or the JSON structure is invalid, the action fails with a descriptive error message.

- **Package Context**: All artifacts are associated with the provided package ID and name in the deployment task file.

- **Artifact Naming**: The action preserves artifact names from the BTP API response, which may contain special characters or spaces.

- **Combined Workflows**: This action enables flexible workflows where you can:
  - Deploy different artifact types from the same package
  - Create separate deployment tasks for selective deployment
  - Combine multiple artifact collections before deployment

---

## 📄 License

This project is licensed under the Apache License 2.0.