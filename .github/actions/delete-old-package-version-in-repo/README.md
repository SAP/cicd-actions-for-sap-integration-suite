# 🧹 Prepare Repo GitHub Action

Delete old versions of a package and prepare the repository directory structure for fresh integration suite artifacts.

---

## ✨ Overview

This action cleans up and prepares a package directory in your repository for deployment of fresh artifacts from SAP BTP Integration Suite. It locates the package directory matching the pattern `*~{PACKAGE_ID}`, removes all outdated artifact files and subdirectories (except Configuration), and ensures the directory is correctly named. This cleanup step prevents conflicts and ensures only current artifacts are present before pulling new data from BTP.

---

## ⚙️ Inputs

| Name         | Required | Description                                                     |
|--------------|----------|----------------------------------------------------------------|
| bearer-token | ✅ Yes   | Bearer token to authenticate with SAP BTP APIs (may be unused). |
| btp-api-url  | ✅ Yes   | Base URL for SAP BTP Integration Suite APIs (may be unused).    |
| package-id   | ✅ Yes   | The package ID to identify the directory to clean.              |
| package-name | ✅ Yes   | The package name for correct directory naming.                  |

---

## 📝 Usage Example

```yaml
jobs:
  prepare-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Prepare Repository
        uses: ./.github/actions/prepare-repo
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          package-name: my-integration-package
      
      - name: Fetch Fresh Artifacts
        uses: ./.github/actions/get-iflow-ids
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
      
      - name: Commit Changes
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add btp-insuite/IntegrationPackages/
          git commit -m "Refresh package artifacts from BTP"
          git push
```

---

## 📂 Outputs

This action has no outputs. It performs repository cleanup operations in place within the `btp-insuite/IntegrationPackages` directory.

**Side Effects:**
- Deletes all subdirectories within the package except `Configuration/`
- Deletes all files directly in the package directory root
- Renames the package directory if needed to match `{PACKAGE_NAME}~{PACKAGE_ID}` format
- Preserves the `Configuration/` subdirectory and its contents

---

## 💡 Tips & Troubleshooting

- **Directory Matching**: The action searches for directories matching `*~{PACKAGE_ID}` pattern in `btp-insuite/IntegrationPackages`. If the directory doesn't exist, the action exits gracefully without error.
- **Single Match Validation**: Exactly one directory matching the pattern must be found. If multiple directories match, the action fails with an error to prevent accidental cleanup of wrong packages.
- **Configuration Preservation**: The `Configuration/` subdirectory is always preserved. This typically contains deployment settings like `Deployment_INTEGRATION_FLOW.json`.
- **File Cleanup**: All regular files in the package root are deleted. Only subdirectories and Configuration contents survive the cleanup.
- **Directory Renaming**: If the directory name doesn't match the expected format `{PACKAGE_NAME}~{PACKAGE_ID}`, it will be renamed automatically to ensure consistency.
- **Working Directory**: This action operates in `btp-insuite/IntegrationPackages`. Ensure your repository structure includes this path.
- **Unused Inputs**: The `bearer-token` and `btp-api-url` inputs are included for workflow consistency but are not actively used in this action. Future versions may leverage these for API-based cleanup.
- **Safe to Repeat**: Running this action multiple times is safe—if the directory doesn't match the expected pattern or doesn't exist, no action is taken.
- **Pre-deployment Step**: Use this action as a preparation step before fetching fresh artifacts from BTP to ensure a clean working state.

---

## 📄 License

This project is licensed under the Apache License 2.0.