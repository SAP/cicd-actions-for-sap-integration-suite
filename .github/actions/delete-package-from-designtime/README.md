# 🗑️ Delete Package from CPI Design Time GitHub Action

Delete an integration package from SAP Cloud Platform Integration (CPI) Design Time via API call.

---

## ✨ Overview

This action removes an integration package directly from SAP BTP Integration Suite using the REST API. It sends a DELETE request to the CPI Design Time API endpoint with the package ID and bearer token for authentication. The action accepts both successful deletion (HTTP 202) and already-deleted scenarios (HTTP 404) as valid outcomes, making it idempotent and safe for repeated execution.

---

## ⚙️ Inputs

| Name        | Required | Description                                      |
|------------|----------|--------------------------------------------------|
| bearer-token | ✅ Yes   | Bearer token with authorization to delete packages from Integration Suite. |
| btp-api-url  | ✅ Yes   | Base URL for the BTP Integration Suite API (e.g., `https://my-tenant.it-cpitrial01.cfapps.sap.hana.ondemand.com`). |
| package-id   | ✅ Yes   | The package ID to be deleted from CPI Design Time. |

---

## 📝 Usage Example

```yaml
jobs:
  delete-from-cpi:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Delete Package from CPI
        uses: ./.github/actions/delete-package-from-cpi
        with:
          bearer-token: Bearer ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001

  delete-with-conditional:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Delete Package on Demand
        if: github.event_name == 'workflow_dispatch' && github.event.inputs.action == 'delete'
        uses: ./.github/actions/delete-package-from-cpi
        with:
          bearer-token: Bearer ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: ${{ github.event.inputs.package-id }}
```

---

## 📂 Outputs

This action has no outputs. It performs a DELETE API operation and returns only exit status (success or failure).

**Side Effects:**
- Sends a DELETE request to the BTP Integration Suite API
- Removes the package from CPI Design Time (if it exists)
- No local file system changes

---

## 💡 Tips & Troubleshooting

- **Bearer Token Format**: Ensure the bearer token includes the `Bearer` prefix. If using a GitHub secret, include it in the input as `Bearer ${{ secrets.TOKEN }}` or store the full `Bearer xyz...` in the secret.
- **API URL Format**: Use the complete base URL of your BTP tenant (e.g., `https://my-tenant.it-cpitrial01.cfapps.sap.hana.ondemand.com`). Do not include trailing slashes.
- **HTTP 202 Response**: Indicates the deletion request was accepted and is being processed asynchronously. The package will be deleted shortly.
- **HTTP 404 Response**: Indicates the package doesn't exist (already deleted or never existed). The action treats this as success since the end result is the same.
- **Other HTTP Status Codes**: Any response code other than 202 or 404 is treated as an error. Common error codes include 401 (unauthorized), 403 (forbidden), 500 (server error).
- **Authentication Failures**: If you receive a 401 error, verify your bearer token is valid and has not expired. Regenerate tokens in your BTP environment if needed.
- **Permission Issues**: If you receive a 403 error, ensure your bearer token has the required permissions to delete integration packages.
- **Idempotent Operation**: This action is safe to run multiple times. If the package is already deleted, it returns 404, which is treated as success.
- **Package Deletion Delay**: After a successful 202 response, the actual deletion may take a few seconds. Subsequent operations on the package should wait briefly.
- **No Rollback**: Package deletion is permanent. Ensure you have backups or Git version control for recovery.

---

## 📄 License

This project is licensed under the Apache License 2.0.