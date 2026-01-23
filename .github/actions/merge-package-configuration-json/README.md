# 🔗 Merge Package Configuration JSON GitHub Action

Intelligently merge new JSON configuration files with existing package configurations while preserving stage-specific parameter values.

---

## ✨ Overview

This action merges two JSON configuration files containing integration flow parameters, intelligently preserving environment-specific stage values (TST, PRD, etc.) from the existing configuration. If no existing configuration exists, it copies the new configuration as the baseline. The action matches artifacts by `ArtifactID` and parameters by `ParameterKey`, then merges parameter values by combining the new `Default` values with preserved stage-specific values from the existing configuration. Useful for synchronizing parameter updates from BTP while maintaining environment-specific customizations.

---

## ⚙️ Inputs

| Name                | Required | Description                                                      |
|---------------------|----------|------------------------------------------------------------------|
| new-config-file-path | ✅ Yes   | Path to the new JSON configuration file to merge.                |
| package-id          | ✅ Yes   | The package ID for locating the target configuration directory.  |
| package-name        | ✅ Yes   | The package name for constructing the configuration path.        |

---

## 📝 Usage Example

```yaml
jobs:
  merge-and-sync-config:
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
      
      - name: Get Package IDs
        id: get-ids
        uses: ./.github/actions/get-object-ids-of-package
        with:
          bearer-token: ${{ steps.auth.outputs.token }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          object-type: Integration
      
      - name: Export Parameters
        id: export
        uses: ./.github/actions/get-external-parameters
        with:
          bearer-token: ${{ steps.auth.outputs.token }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          package-name: my-package
          file: ${{ steps.get-ids.outputs.file }}
      
      - name: Merge Configuration
        uses: ./.github/actions/merge-package-configuration-json
        with:
          new-config-file-path: ${{ steps.export.outputs.path }}
          package-id: my-package-001
          package-name: my-package
      
      - name: Commit Changes
        uses: ./.github/actions/git-commit
        with:
          comment: "Sync parameters and preserve stage configurations"

  sync-with-xml-backup:
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
      
      - name: Export Parameters
        id: export
        uses: ./.github/actions/get-external-parameters
        with:
          bearer-token: ${{ steps.token.outputs.token }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          package-name: my-package
          file: ${{ steps.iflows.outputs.file }}
      
      - name: Merge JSON Configuration
        uses: ./.github/actions/merge-package-configuration-json
        with:
          new-config-file-path: ${{ steps.export.outputs.path }}
          package-id: my-package-001
          package-name: my-package
      
      - name: Merge XML Backup
        uses: ./.github/actions/xml-configuration-merger
        with:
          temp_xml_path: ${{ steps.export.outputs.path }}.xml.tmp
      
      - name: Commit Configuration Update
        uses: ./.github/actions/git-commit
        with:
          comment: "Update JSON and XML configurations with preserved stage values"

  first-time-setup:
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
      
      - name: Get Package IDs
        id: get-ids
        uses: ./.github/actions/get-object-ids-of-package
        with:
          bearer-token: ${{ steps.token.outputs.token }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: new-package-001
          object-type: Integration
      
      - name: Export Initial Configuration
        id: export
        uses: ./.github/actions/get-external-parameters
        with:
          bearer-token: ${{ steps.token.outputs.token }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: new-package-001
          package-name: new-package
          file: ${{ steps.get-ids.outputs.file }}
      
      - name: Initialize Configuration (First Run)
        uses: ./.github/actions/merge-package-configuration-json
        with:
          new-config-file-path: ${{ steps.export.outputs.path }}
          package-id: new-package-001
          package-name: new-package
      
      - name: Commit Initial Configuration
        uses: ./.github/actions/git-commit
        with:
          comment: "Initialize package configuration from BTP"
```

---

## 📂 Outputs

This action has no explicit outputs. It modifies the configuration file in place within the repository structure.

**Side Effects:**
- Creates target directory if it doesn't exist: `{PACKAGE_NAME}~{PACKAGE_ID}/Configuration/`
- Copies or merges configuration to: `{PACKAGE_NAME}~{PACKAGE_ID}/Configuration/ConfigParams_INTEGRATION_FLOW.json`
- Removes temporary input files after processing
- Preserves stage-specific parameter values from existing configuration

**Merge Behavior:**
The action intelligently merges JSON files by:
1. **First Run**: If no existing configuration exists, copies new file as-is
2. **Subsequent Runs**: Merges new configuration with existing while preserving:
   - `Default` values from new configuration (always updated)
   - `TST`, `PRD`, and other stage-specific values from existing configuration
   - Matches artifacts by `ArtifactID` and parameters by `ParameterKey`

**Example Merge Result:**
```json
{
  "PackageIntegrationFlowParameters": {
    "PackageName": "my-package",
    "PackageID": "my-package-001",
    "Artifacts": [
      {
        "ArtifactID": "flow-1",
        "ArtifactName": "My Flow",
        "Parameters": [
          {
            "ParameterKey": "API_ENDPOINT",
            "ParameterValues": {
              "Default": "https://api.dev.example.com",
              "TST": "https://api.tst.example.com",
              "PRD": "https://api.prod.example.com"
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

- **Directory Structure**: The action expects and creates the directory structure `{PACKAGE_NAME}~{PACKAGE_ID}/Configuration/` within `btp-insuite/IntegrationPackages`. Ensure your repository follows this convention.

- **Target File**: The target configuration file is always named `ConfigParams_INTEGRATION_FLOW.json` within the Configuration directory.

- **First Run Behavior**: On first run (no existing configuration), the action simply copies the new configuration file to the target location. No merging is performed.

- **Subsequent Runs**: On subsequent runs with an existing configuration file, the action performs intelligent merging:
  - New `Default` parameter values always come from the new configuration
  - Stage-specific values (`TST`, `PRD`, etc.) are preserved from the existing configuration
  - New parameters not in existing configuration are added as-is
  - Artifacts are matched by `ArtifactID` for reliable association

- **Parameter Matching**: Parameters are matched by their `ParameterKey` field. Ensure parameter keys remain consistent between exports for reliable merging.

- **Artifact Matching**: Artifacts are matched by `ArtifactID`. If an artifact ID changes between exports, it's treated as a new artifact and added without merging with previous versions.

- **Stage Value Preservation**: All non-`Default` values in `ParameterValues` are preserved from the existing configuration. Common stage names include `TST`, `PRD`, `DEV`, `POC`, but the action preserves any custom stage names.

- **New Stages**: If you add new stage-specific values manually (e.g., `STAGING`), they will be preserved in subsequent merges as long as the parameter key matches.

- **Validation**: The action validates the merged JSON before replacing the target file. If validation fails, the merge is aborted and the existing file is left unchanged.

- **Cleanup**: The action automatically removes the input file after successful processing to keep the repository clean.

- **Error Handling**: If files are missing, merge fails, or resulting JSON is invalid, the action exits with a descriptive error message and doesn't modify the target file.

- **Working Directory**: The action operates in `btp-insuite/IntegrationPackages` directory. Ensure your repository structure matches this path.

- **jq Dependency**: The action uses jq for JSON merging with a custom helper function. Ensure your runner has jq installed (included by default on ubuntu-latest).

- **Merge Logic**: The merge uses a sophisticated jq filter that:
  - Maintains new JSON structure as the baseline
  - Overlays preserved stage values from old configuration
  - Handles both single objects and arrays transparently
  - Uses `merge_parameter_values` helper function for combining values

- **Null Handling**: If either file lacks `ParameterValues` or the stage-specific values don't exist, the action gracefully handles these cases without errors.

- **File Size**: Large configuration files should be processed efficiently, but extremely large files may require additional processing time.

- **Idempotent Operation**: Running this action multiple times with the same input produces consistent results, making it safe for repeated or automated executions.

- **Version Control**: After merging, use `git-commit` action to commit the updated configuration to maintain version history.

- **Configuration Export Format**: The input JSON must follow the format produced by `get-external-parameters` action with proper `PackageIntegrationFlowParameters` structure.

- **Combining with XML Merge**: You can run both `merge-package-configuration-json` and `xml-configuration-merger` in the same workflow to maintain both JSON and XML configurations in sync.

---

## 📄 License

This project is licensed under the Apache License 2.0.