# 🚀 Update Designtime from GIT (Upload / Delete) GitHub Action

Orchestrate the complete package lifecycle - checkout, prepare, authenticate, upload/delete packages, and configure parameters in SAP BTP Integration Suite from a Git reference.

---

## ✨ Overview

This is a composite orchestration action that manages the entire package deployment and deletion workflow. It handles Git checkout from a specified reference, OAuth authentication, package preparation from the Git repository, deletion of old package versions from CPI Design Time, optional package upload, and automatic parameter configuration for the target environment. The action simplifies complex multi-step workflows by combining package management, authentication, and configuration into a single operation, supporting both upload (refresh) and delete-only scenarios.

---

## ⚙️ Inputs

| Name             | Required | Description                                                         |
|------------------|----------|---------------------------------------------------------------------|
| target-env       | ✅ Yes   | Target environment for parameter configuration (e.g., DEV, TST, PRD) |
| source-ref       | ✅ Yes   | Git reference to checkout (branch name or tag).                     |
| package-id       | ✅ Yes   | The package ID to upload or delete.                                 |
| case             | ✅ Yes   | Operation mode: `Upload` or `Delete`.                               |
| btp-api-user     | ✅ Yes   | BTP Service Key Client ID for OAuth authentication.                 |
| btp-tec-user     | ✅ Yes   | BTP technical user username with Integration Suite permissions.    |
| btp-token-url    | ✅ Yes   | OAuth token endpoint URL.                                           |
| btp-api-url      | ✅ Yes   | Base URL for the SAP BTP Integration Suite APIs.                    |
| BTP_API_PASSWORD | ✅ Yes   | Client Secret for the API user/service account.                     |
| BTP_TEC_PASSWORD | ✅ Yes   | Password for the technical user.                                    |

---

## 📝 Usage Example

```yaml
jobs:
  upload-package-to-dev:
    runs-on: ubuntu-latest
    steps:
      - name: Update Designtime - Upload to DEV
        uses: ./.github/actions/update-designtime-from-git
        with:
          target-env: DEV
          source-ref: develop
          package-id: my-package-001
          case: Upload
          btp-api-user: ${{ secrets.BTP_API_USER }}
          btp-tec-user: ${{ secrets.BTP_TEC_USER }}
          btp-token-url: ${{ secrets.BTP_TOKEN_URL }}
          btp-api-url: ${{ secrets.BTP_DEV_API_URL }}
          BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
          BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}

  delete-package-cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Update Designtime - Delete Package
        uses: ./.github/actions/update-designtime-from-git
        with:
          target-env: TST
          source-ref: main
          package-id: old-package-001
          case: Delete
          btp-api-user: ${{ secrets.BTP_API_USER }}
          btp-tec-user: ${{ secrets.BTP_TEC_USER }}
          btp-token-url: ${{ secrets.BTP_TOKEN_URL }}
          btp-api-url: ${{ secrets.BTP_TST_API_URL }}
          BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
          BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}

  multi-env-promotion:
    runs-on: ubuntu-latest
    steps:
      - name: Upload to DEV
        uses: ./.github/actions/update-designtime-from-git
        with:
          target-env: DEV
          source-ref: develop
          package-id: my-package-001
          case: Upload
          btp-api-user: ${{ secrets.BTP_API_USER }}
          btp-tec-user: ${{ secrets.BTP_TEC_USER }}
          btp-token-url: ${{ secrets.BTP_TOKEN_URL }}
          btp-api-url: https://dev-tenant.it-cpitrial01.cfapps.sap.hana.ondemand.com
          BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
          BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}
      
      - name: Upload to TST
        uses: ./.github/actions/update-designtime-from-git
        with:
          target-env: TST
          source-ref: main
          package-id: my-package-001
          case: Upload
          btp-api-user: ${{ secrets.BTP_API_USER }}
          btp-tec-user: ${{ secrets.BTP_TEC_USER }}
          btp-token-url: ${{ secrets.BTP_TOKEN_URL }}
          btp-api-url: https://tst-tenant.it-cpitrial01.cfapps.sap.hana.ondemand.com
          BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
          BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}
      
      - name: Upload to PRD
        uses: ./.github/actions/update-designtime-from-git
        with:
          target-env: PRD
          source-ref: main
          package-id: my-package-001
          case: Upload
          btp-api-user: ${{ secrets.BTP_API_USER }}
          btp-tec-user: ${{ secrets.BTP_TEC_USER }}
          btp-token-url: ${{ secrets.BTP_TOKEN_URL }}
          btp-api-url: https://prod-tenant.it-cpitrial01.cfapps.sap.hana.ondemand.com
          BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
          BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}

  tag-based-release:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy Release Version to Production
        uses: ./.github/actions/update-designtime-from-git
        with:
          target-env: PRD
          source-ref: v1.2.3
          package-id: my-package-001
          case: Upload
          btp-api-user: ${{ secrets.BTP_API_USER }}
          btp-tec-user: ${{ secrets.BTP_TEC_USER }}
          btp-token-url: ${{ secrets.BTP_TOKEN_URL }}
          btp-api-url: ${{ secrets.BTP_PROD_API_URL }}
          BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
          BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}
```

---

## 📂 Outputs

This action has no explicit outputs. It orchestrates multiple sub-actions that perform the actual operations.

**Operation Summary:**

**Upload Case:**
1. Checks out repository from specified Git reference
2. Authenticates with BTP OAuth
3. Prepares ZIP package from Git repository
4. Deletes existing package from CPI Design Time
5. Uploads new package to CPI Design Time
6. Configures parameters for target environment

**Delete Case:**
1. Checks out repository from specified Git reference
2. Authenticates with BTP OAuth
3. Deletes package from CPI Design Time
4. (No upload or parameter configuration)

---

## 💡 Tips & Troubleshooting

- **Operation Modes**: Choose between `Upload` or `Delete`:
  - `Upload`: Complete refresh cycle (delete old → upload new → configure)
  - `Delete`: Remove package from CPI Design Time only

- **Git Reference**: The `source-ref` can be:
  - Branch name (e.g., `main`, `develop`)
  - Tag name (e.g., `v1.0.0`)
  - Commit SHA (full or abbreviated)
  - Use for version-based deployments or branch-based automatic updates

- **Package Directory**: The action expects the package at `btp-insuite/IntegrationPackages/{PACKAGE_NAME}~{PACKAGE_ID}/` in the Git reference.

- **Authentication**: All BTP credentials are required even though only the relevant operations are performed. Store all credentials as GitHub secrets for security.

- **Orchestration Flow**: This action calls sub-actions in sequence:
  1. `actions/checkout@v4` - Git checkout
  2. `get-oauth-token` - OAuth authentication
  3. `prepare-zip-from-git` - (if Upload)
  4. `delete-package-from-cpi` - Always
  5. `deploy-zip-to-cpi` - (if Upload)
  6. `update-iflow-parameters` - (if Upload)

- **Always-Delete Behavior**: Note that the `Delete Package from CPI Designtime` step always runs, regardless of case. This ensures clean replacement before upload and complete removal for delete operations.

- **Environment-Specific Parameters**: The `target-env` is used for parameter configuration during upload. Ensure your JSON configuration file contains values for this environment.

- **Target Environment Names**: Use consistent naming (DEV, TST, STAGING, PRD, PROD) matching your configuration structure and BTP environment setup.

- **Multi-Tenancy Support**: Supports multiple BTP tenants via different API URLs. Deploy the same package to different environments by calling this action multiple times.

- **Error Propagation**: If any sub-action fails, the orchestration stops and reports the failure. Check logs to identify which step failed.

- **Token Expiration**: For long-running workflows with multiple environments, ensure the OAuth token doesn't expire between operations (typically valid for 1-2 hours).

- **Network Requirements**: Ensure the runner has network access to:
  - The Git repository (for checkout)
  - The BTP token endpoint (for authentication)
  - The BTP API URL (for package operations)

- **Package Consistency**: Ensure the package in the specified Git reference is valid and complete. Missing or corrupted package directories will cause upload failures.

- **Parameter Configuration**: For Upload case, ensure the `ConfigParams_INTEGRATION_FLOW.json` file exists in the package's Configuration directory and contains valid parameter definitions for the target environment.

- **Concurrent Operations**: Deploying the same package to multiple environments is safe, but concurrent operations to the same BTP environment/package may cause conflicts. Use sequential environment promotion.

- **Zero-Downtime Replacement**: The delete-then-upload pattern allows updating running packages, though there may be a brief moment when the package is unavailable.

- **Backup Before Delete**: For production environments, consider manually backing up packages before running delete operations. Git provides version history, but additional backups offer extra safety.

- **Credential Rotation**: Regularly rotate API and technical user passwords, updating GitHub secrets accordingly.

- **Selective Updates**: To update only a specific iFlow's parameters (if supported), modify the sub-action `update-iflow-parameters` with an iFlow ID if needed.

- **Dry-Run Pattern**: To test without deploying, fork the workflow and modify the `case` parameter logic, or temporarily comment out steps.

- **Idempotent Upload**: Running this action multiple times with the same inputs produces consistent results. The delete-then-upload pattern ensures fresh deployment.

- **Monitoring and Logging**: The action provides detailed logs from each sub-action. Monitor logs for:
  - Git checkout success
  - OAuth token acquisition
  - Package preparation completion
  - Delete operation result
  - Upload operation result
  - Parameter configuration status

- **Failure Recovery**: If a step fails:
  - Fix the underlying issue (credentials, package structure, configuration, etc.)
  - Re-run the action (it will retry from the beginning)
  - Check logs for specific error messages

- **Cross-Reference Navigation**: This composite action calls several other documented actions:
  - `get-oauth-token` - For authentication details
  - `prepare-zip-from-git` - For packaging details
  - `delete-package-from-cpi` - For deletion details
  - `deploy-zip-to-cpi` - For upload details
  - `update-iflow-parameters` - For parameter configuration details

---

## 📄 License

This project is licensed under the Apache License 2.0.