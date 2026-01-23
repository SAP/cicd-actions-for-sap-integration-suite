# 📦 Deploy ZIP Package into CPI Designtime GitHub Action

Upload and deploy a ZIP package containing integration artifacts directly into SAP BTP Integration Suite Design Time.

---

## ✨ Overview

This action uploads a ZIP file containing integration package artifacts to SAP BTP Integration Suite via the REST API. It base64-encodes the ZIP file, creates a JSON payload with the encoded content, and sends it to the CPI Design Time API endpoint. The action validates the upload success through HTTP 201 response code and provides detailed error feedback if the deployment fails.

---

## ⚙️ Inputs

| Name        | Required | Description                                                   |
|------------|----------|---------------------------------------------------------------|
| bearer-token | ✅ Yes   | Bearer token with authorization to upload packages to Integration Suite. |
| btp-api-url  | ✅ Yes   | Base URL for the BTP Integration Suite API.                   |
| zip-location | ✅ Yes   | Path to the ZIP file containing the integration package artifacts. |

---

## 📝 Usage Example

```yaml
jobs:
  deploy-zip-package:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Create Package ZIP
        run: |
          cd btp-insuite/IntegrationPackages
          zip -r my-package.zip my-package~my-package-001/
      
      - name: Deploy ZIP to CPI
        uses: ./.github/actions/deploy-zip-to-cpi
        with:
          bearer-token: Bearer ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          zip-location: btp-insuite/IntegrationPackages/my-package.zip

  deploy-from-artifact:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Download Package Artifact
        uses: actions/download-artifact@v3
        with:
          name: integration-package
      
      - name: Deploy ZIP to CPI
        uses: ./.github/actions/deploy-zip-to-cpi
        with:
          bearer-token: Bearer ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          zip-location: integration-package.zip
```

---

## 📂 Outputs

This action has no outputs. It performs a package upload operation via BTP API and returns only exit status (success or failure).

**Side Effects:**
- Sends POST request to BTP Integration Suite API endpoint `/api/v1/IntegrationPackages`
- Creates temporary files: `encoded.txt` (base64-encoded ZIP) and `payload.json` (JSON payload)
- Uploads the package to CPI Design Time if successful

**Expected Response:**
- HTTP 201 Created: Package successfully uploaded to CPI Design Time

---

## 💡 Tips & Troubleshooting

- **Bearer Token Format**: Include the `Bearer` prefix in your token. Store as `Bearer xyz...` in GitHub secrets or format as `Bearer ${{ secrets.TOKEN }}` in the input.
- **ZIP File Location**: Provide the relative path from the workflow execution context to the ZIP file. Absolute paths may not work in all environments.
- **ZIP File Requirements**: Ensure the ZIP file is a valid package archive containing the required integration artifacts and metadata in the correct directory structure.
- **File Size Limits**: Large ZIP files may exceed API payload limits. Check your BTP environment's API limits if upload fails with 413 or 414 errors.
- **Base64 Encoding**: The action uses `base64 -w 0` to create a single-line base64 string, which is required for valid JSON formatting.
- **HTTP 201 Response**: Successful upload returns HTTP 201 (Created). Any other response code triggers an error and exits with code 1.
- **Authentication Failures**: If you receive HTTP 401, verify your bearer token is valid and not expired. Regenerate tokens in your BTP environment if needed.
- **Permission Issues**: If you receive HTTP 403, ensure your bearer token has permissions to upload integration packages.
- **Duplicate Packages**: If uploading a package with an ID that already exists in CPI, the API may return an error. Delete or rename the existing package first.
- **Temporary Files**: The action creates `encoded.txt` and `payload.json` in the working directory. These are not cleaned up automatically; delete manually if needed.
- **ZIP Structure**: Ensure your ZIP file follows the expected package structure. Incorrect directory layouts may cause upload acceptance but subsequent deployment failures.
- **Error Details**: Check the full API response body in logs for detailed error messages that indicate what went wrong with the upload.
- **Network Connectivity**: Ensure the runner has network access to the BTP API URL. Firewall or network restrictions may cause connectivity errors.

---

## 📄 License

This project is licensed under the Apache License 2.0.