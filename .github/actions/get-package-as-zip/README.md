# 📥 Get CPI Package as ZIP GitHub Action

Download an integration package from SAP BTP Integration Suite Design Time as a ZIP file for backup, version control, or redistribution.

---

## ✨ Overview

This action exports a complete integration package from SAP BTP Integration Suite as a compressed ZIP file. It sends a GET request to the CPI Design Time API's `$value` endpoint to retrieve the package binary content and saves it to a temporary location. The action is ideal for creating backups, downloading packages for local analysis, or obtaining packages for deployment to other environments via the `deploy-zip-to-cpi` action.

---

## ⚙️ Inputs

| Name         | Required | Description                                              |
|--------------|----------|----------------------------------------------------------|
| bearer-token | ✅ Yes   | Bearer token to authenticate with SAP BTP APIs.          |
| btp-api-url  | ✅ Yes   | Base URL for the SAP BTP Integration Suite APIs.         |
| package-id   | ✅ Yes   | The package ID to download from CPI Design Time.         |
| package-name | ✅ Yes   | The package name (used for output filename).             |

---

## 📝 Usage Example

```yaml
jobs:
  download-and-backup:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Download Package from CPI
        id: download
        uses: ./.github/actions/get-cpi-package-as-zip
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          package-name: my-integration-package
      
      - name: Store as Artifact
        uses: actions/upload-artifact@v3
        with:
          name: package-backup
          path: ${{ steps.download.outputs.location }}

  download-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Download from Dev
        id: download-dev
        uses: ./.github/actions/get-cpi-package-as-zip
        with:
          bearer-token: ${{ secrets.BTP_DEV_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_DEV_API_URL }}
          package-id: my-package-001
          package-name: my-integration-package
      
      - name: Deploy to Prod
        uses: ./.github/actions/deploy-zip-to-cpi
        with:
          bearer-token: ${{ secrets.BTP_PROD_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_PROD_API_URL }}
          zip-location: ${{ steps.download-dev.outputs.location }}

  version-control-backup:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Download Current Package
        id: download
        uses: ./.github/actions/get-cpi-package-as-zip
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          package-name: my-integration-package
      
      - name: Store in Backups Directory
        run: |
          mkdir -p backups
          cp ${{ steps.download.outputs.location }} backups/my-integration-package-$(date +%Y%m%d-%H%M%S).zip
      
      - name: Commit Backup
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add backups/
          git commit -m "Add package backup"
          git push
```

---

## 📂 Outputs

| Name     | Description                                    |
|----------|------------------------------------------------|
| location | File path to the downloaded ZIP package file   |

**Output File Details:**
- **Filename Format**: `{PACKAGE_NAME}~{PACKAGE_ID}.zip`
- **Location**: Stored in `${{ runner.temp }}` directory
- **Content**: Complete package archive with all artifacts, configurations, and metadata from CPI Design Time
- **ZIP Structure**: Matches the format expected by the `deploy-zip-to-cpi` action for re-deployment

---

## 💡 Tips & Troubleshooting

- **Bearer Token**: Ensure your bearer token has read permissions for integration packages. Store as a GitHub secret and pass as `Bearer ${{ secrets.BTP_BEARER_TOKEN }}`.
- **Package ID**: Use the exact package ID from your BTP environment. This can be found in the package URL or management interface.
- **HTTP 200 Response**: The action expects HTTP 200 for successful download. Any other status code triggers an error.
- **Authentication Failures**: If you receive HTTP 401, verify your bearer token is valid and not expired. Regenerate tokens in your BTP environment if needed.
- **Permission Issues**: If you receive HTTP 403, ensure your bearer token has read permissions for the specified package.
- **Package Not Found**: If you receive HTTP 404, verify the package ID is correct and the package exists in your BTP environment.
- **File Size**: Downloaded ZIP files are stored in `${{ runner.temp }}`, which has limited disk space. Very large packages may fail if they exceed available space.
- **Temporary Storage**: The downloaded ZIP file is created in the workflow's temporary directory. Move or archive it if you need to preserve it beyond the workflow run.
- **Filename Format**: The output filename combines package name and ID with a tilde separator (`~`), making it easy to identify and preventing naming conflicts.
- **API Endpoint**: The action uses the `$value` endpoint which returns the binary ZIP content directly, not JSON metadata.
- **Network Requirements**: Ensure the runner has network access to the BTP API URL. Firewall or network restrictions may cause connectivity errors.
- **Environment-to-Environment Transfers**: Combine this action with `deploy-zip-to-cpi` to move packages between development, testing, and production environments.
- **Artifact Storage**: Use `upload-artifact` and `download-artifact` actions to preserve packages across jobs or workflows.
- **Version Control**: Consider storing periodically downloaded packages in version control with timestamps for change tracking and audit trails.
- **Backup Strategy**: Run this action on a schedule to automatically backup packages from production or important environments.
- **Error Diagnostics**: If download fails, the action displays the response body in logs, which may contain API error messages for troubleshooting.

---

## 📄 License

This project is licensed under the Apache License 2.0.