# 📂 Unzip Package into REPO GitHub Action

Extract a ZIP package containing integration artifacts into the repository directory structure, including recursive extraction of nested ZIPs.

---

## ✨ Overview

This action extracts a ZIP file containing integration package artifacts into the `btp-insuite/IntegrationPackages` directory structure. It performs intelligent nested ZIP extraction—after extracting the main ZIP, it scans for any contained ZIP files and extracts those as well, replacing the nested ZIPs with their extracted folder contents. This ensures a fully unpacked, ready-to-use package structure suitable for version control and further processing.

---

## ⚙️ Inputs

| Name        | Required | Description                                                    |
|------------|----------|----------------------------------------------------------------|
| location-zip | ✅ Yes   | Full path to the ZIP file (including filename) to extract.     |

---

## 📝 Usage Example

```yaml
jobs:
  extract-package:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Download Package ZIP
        uses: actions/download-artifact@v3
        with:
          name: integration-package-zip
      
      - name: Unzip Package into Repo
        uses: ./.github/actions/unzip-package-into-repo
        with:
          location-zip: integration-package.zip
      
      - name: Commit Extracted Package
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add btp-insuite/IntegrationPackages/
          git commit -m "Extract and add integration package artifacts"
          git push

  deploy-after-extraction:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Download and Extract Package
        uses: ./.github/actions/unzip-package-into-repo
        with:
          location-zip: ${{ github.workspace }}/artifacts/my-package.zip
      
      - name: Create Deployment File
        uses: ./.github/actions/create-iflow-deployment-file
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          package-name: my-package
          file: deployment-config.json
```

---

## 📂 Outputs

This action has no outputs. It performs directory extraction operations in the repository.

**Side Effects:**
- Extracts main ZIP to `btp-insuite/IntegrationPackages/{ZIP_NAME}/`
- Recursively extracts nested ZIP files found in the extracted directory
- Removes original nested ZIP files after successful extraction
- Replaces nested ZIP files with folders containing their extracted contents
- Directory structure is ready for Git version control

**Expected Directory Structure After Extraction:**
```
btp-insuite/IntegrationPackages/
├── my-package~my-package-001/
│   ├── Configuration/
│   │   ├── Deployment_INTEGRATION_FLOW.json
│   │   └── ...
│   ├── artifacts/
│   │   ├── flow1/
│   │   ├── flow2/
│   │   └── ...
│   ├── resources/
│   │   └── ...
│   └── ...
```

---

## 💡 Tips & Troubleshooting

- **Full Path Required**: Provide the complete path to the ZIP file including filename. Relative paths work from the GitHub workspace context.
- **Empty Destination Assumption**: The action assumes the destination directory doesn't exist or is empty. Pre-existing files in the target directory may be overwritten by extraction.
- **Nested ZIP Extraction**: The action intelligently detects and extracts nested ZIPs, replacing the original ZIP files with their extracted contents. This flattens the structure for easier repository management.
- **Non-ZIP Files**: Files that are not valid ZIPs are left unchanged. The action logs failed extraction attempts but continues processing remaining files.
- **Cleanup**: Original nested ZIP files are automatically deleted after successful extraction. The main ZIP file is not deleted—remove it manually if needed.
- **Directory Naming**: The extracted directory is named after the ZIP filename without the `.zip` extension. For example, `my-package.zip` extracts to `my-package/`.
- **Working Directory**: The action performs extraction within `btp-insuite/IntegrationPackages`. Nested extractions happen in temporary folders created dynamically.
- **Recursive Extraction**: Only one level of nesting is processed per run. If there are multiple levels of nested ZIPs, the action will unzip one level, and a subsequent run would process the next level.
- **File Permissions**: After extraction, file permissions are inherited from the ZIP archive. Ensure scripts or executables have correct permissions if needed.
- **Special Characters**: ZIP filenames with special characters may cause issues. Use alphanumeric names with hyphens or underscores.
- **Large Packages**: Large ZIP files may take time to extract. Monitor workflow execution time for timeout issues on self-hosted runners.
- **Disk Space**: Ensure sufficient disk space for extraction. ZIP extraction requires space for both the compressed and uncompressed files temporarily.
- **Error Handling**: Invalid ZIP files or extraction failures don't stop the action—it logs warnings and continues. Check logs for details on any failed extractions.

---

## 📄 License

This project is licensed under the Apache License 2.0.