# ⚙️ Update iFlow Configuration Parameters GitHub Action

Update integration flow configuration parameters in SAP BTP Integration Suite using local JSON configuration as the source of truth.

---

## ✨ Overview

This action updates integration flow configuration parameters in SAP BTP Integration Suite by reading parameter values from a local JSON configuration file and pushing them to the runtime via the BTP API. It locates the package directory, reads the `ConfigParams_INTEGRATION_FLOW.json` file, and updates each parameter with stage-specific values (falling back to default if stage value is not available). The action supports updating all iFlows in a package or a specific iFlow, provides detailed logging, and gracefully handles missing values with warnings instead of failures.

---

## ⚙️ Inputs

| Name          | Required | Description                                                                  |
|---------------|----------|------------------------------------------------------------------------------|
| package-id    | ✅ Yes   | The package ID to locate the configuration file.                             |
| bearer-token  | ✅ Yes   | Bearer token to authenticate with SAP BTP APIs.                              |
| btp-api-url   | ✅ Yes   | Base URL for the SAP BTP Integration Suite APIs.                             |
| target-env    | ✅ Yes   | Target environment/stage name (e.g., `DEV`, `TST`, `PRD`).                  |
| iflow-id      | ❌ No    | Optional: Specific iFlow ID to update. If omitted, updates all iFlows.      |

---

## 📝 Usage Example

```yaml
jobs:
  update-all-parameters:
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
      
      - name: Update All Parameters
        uses: ./.github/actions/update-iflow-parameters
        with:
          package-id: my-package-001
          bearer-token: ${{ steps.auth.outputs.token }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          target-env: TST

  update-specific-iflow:
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
      
      - name: Update Specific iFlow
        uses: ./.github/actions/update-iflow-parameters
        with:
          package-id: my-package-001
          bearer-token: ${{ steps.token.outputs.token }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          target-env: PRD
          iflow-id: my-critical-flow

  multi-environment-deployment:
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
      
      - name: Update DEV Parameters
        uses: ./.github/actions/update-iflow-parameters
        with:
          package-id: my-package-001
          bearer-token: ${{ steps.token.outputs.token }}
          btp-api-url: https://dev-tenant.it-cpitrial01.cfapps.sap.hana.ondemand.com
          target-env: DEV
      
      - name: Update TST Parameters
        uses: ./.github/actions/update-iflow-parameters
        with:
          package-id: my-package-001
          bearer-token: ${{ steps.token.outputs.token }}
          btp-api-url: https://tst-tenant.it-cpitrial01.cfapps.sap.hana.ondemand.com
          target-env: TST
      
      - name: Update PRD Parameters
        uses: ./.github/actions/update-iflow-parameters
        with:
          package-id: my-package-001
          bearer-token: ${{ steps.token.outputs.token }}
          btp-api-url: https://prod-tenant.it-cpitrial01.cfapps.sap.hana.ondemand.com
          target-env: PRD

  deployment-with-error-handling:
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
      
      - name: Update Parameters
        id: update
        uses: ./.github/actions/update-iflow-parameters
        with:
          package-id: my-package-001
          bearer-token: ${{ steps.token.outputs.token }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          target-env: TST
      
      - name: Generate Report
        if: always()
        run: |
          echo "Update operation completed"
          echo "Check logs above for success/failure details"
```

---

## 📂 Outputs

This action has no explicit outputs. It performs updates via BTP API and returns only exit status (always 0 for success/partial success).

**Side Effects:**
- Updates integration flow configuration parameters in the running BTP environment
- Writes detailed logs showing each parameter update attempt
- Provides summary of successful updates, failures, and skipped parameters

**Parameter Value Resolution:**
The action uses intelligent fallback logic to determine parameter values:
1. First tries to use the stage-specific value from JSON (e.g., `ParameterValues.TST`)
2. If not found, falls back to `ParameterValues.Default`
3. If neither exists, skips the parameter with a warning

---

## 💡 Tips & Troubleshooting

- **Configuration File Location**: The action expects the configuration file at `{PACKAGE_NAME}~{PACKAGE_ID}/Configuration/ConfigParams_INTEGRATION_FLOW.json` in the `btp-insuite/IntegrationPackages` directory.

- **Configuration File Format**: The JSON must follow the structure produced by `get-external-parameters` or `merge-package-configuration-json` actions with `PackageIntegrationFlowParameters.Artifacts` array.

- **Package Directory Matching**: Exactly one directory matching `*~{PACKAGE_ID}` must be found. Multiple matches cause failure to prevent updating the wrong package.

- **Stage Parameter Values**: The `target-env` parameter (e.g., `TST`, `PRD`) must match the stage keys in your JSON configuration. If a stage-specific value doesn't exist, the action falls back to `Default`.

- **All iFlows vs Specific iFlow**:
  - Leave `iflow-id` empty to update all iFlows in the package
  - Provide `iflow-id` to update only that specific iFlow
  - If `iflow-id` is provided but not found, the action exits with error

- **Bearer Token**: Ensure your bearer token has permissions to update integration flow configurations. Include the `Bearer ` prefix.

- **Parameter Key Encoding**: Parameter keys are URI-encoded for the API request. Special characters are handled automatically.

- **API Rate Limiting**: The action sleeps for 1 second between each parameter update to avoid API rate limiting issues. For packages with many parameters, this may take time.

- **Empty Parameter Values**: If a parameter has no stage-specific value and no default, the action logs a warning and skips it without failure. This allows partial updates without blocking.

- **HTTP Status Codes**: The action considers all 2xx HTTP status codes as success. Other codes are treated as failures but don't stop processing.

- **Exit Code**: The action always exits with code 0, even if some parameters fail to update. Check the summary logs for failure details.

- **Error Resilience**: Partial failures are tolerated. If 50 parameters update successfully but 5 fail, the action completes successfully with a summary showing both counts.

- **jq Installation**: The action automatically checks for and installs jq if needed using apt-get.

- **Detailed Logging**: Each parameter update attempt logs:
  - Parameter key name
  - Selected value (stage-specific or default)
  - HTTP status code
  - Success or failure indication

- **Summary Report**: At the end, the action provides a summary including:
  - Total parameters processed
  - Successfully updated count
  - Failed count (API errors)
  - Skipped count (missing values)

- **Target Environment Flexibility**: Use environment-specific naming (DEV, TST, STAGING, PRD, PROD) matching your configuration structure.

- **Workflow Integration**: Typically use this action after pulling packages from CPI and merging configurations to push updated parameters back to the environment.

- **Multi-Environment Workflows**: Can be called multiple times in the same workflow with different API URLs and environments for multi-tenancy deployments.

- **No Validation**: The action does not validate parameter values against business rules. Invalid values will be rejected by the BTP API.

- **Network Requirements**: Ensure the runner has network access to the BTP API URL.

- **Timeout Handling**: For packages with many parameters, ensure sufficient workflow timeout. The action processes one parameter at a time with 1-second delays.

- **Parameter Dependencies**: If parameters have interdependencies, ensure they're ordered correctly in your configuration JSON before running this action.

---

## 📄 License

This project is licensed under the Apache License 2.0.