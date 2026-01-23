# 📦 Prepare ZIP Package from GIT GitHub Action

Create a deployable ZIP package from integration package directory structure in the Git repository.

---

## ✨ Overview

This action packages an integration package from your Git repository into a ZIP file suitable for deployment to SAP BTP Integration Suite. It locates the package directory matching the pattern `*~{PACKAGE_ID}`, copies all contents while intelligently handling subdirectories (zipping them as embedded files without .zip extensions), skips the Configuration directory, and creates a final deployment-ready ZIP package. The resulting ZIP maintains the proper structure expected by CPI Design Time import operations.

---

## ⚙️ Inputs

| Name       | Required | Description                                  |
|-----------|----------|----------------------------------------------|
| package-id | ✅ Yes   | The package ID to identify the directory to package. |

---

## 📝 Usage Example

```yaml
jobs:
  package-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Prepare ZIP Package
        id: prepare
        uses: ./.github/actions/prepare-zip-from-git
        with:
          package-id: my-package-001
      
      - name: Deploy to CPI
        uses: ./.github/actions/deploy-zip-to-cpi
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          zip-location: ${{ steps.prepare.outputs.location }}

  package-and-backup:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Prepare ZIP
        id: package
        uses: ./.github/actions/prepare-zip-from-git
        with:
          package-id: my-package-001
      
      - name: Upload as Artifact
        uses: actions/upload-artifact@v3
        with:
          name: packaged-artifact
          path: ${{ steps.package.outputs.location }}
      
      - name: Store in S3 Backup
        run: |
          aws s3 cp ${{ steps.package.outputs.location }} \
            s3://my-backups/packages/$(date +%Y-%m-%d)_my-package-001.zip

  export-for-distribution:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Prepare Package
        id: prep
        uses: ./.github/actions/prepare-zip-from-git
        with:
          package-id: my-package-001
      
      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: v${{ github.run_number }}
          release_name: Package Release v${{ github.run_number }}
          draft: false
          prerelease: false
      
      - name: Upload Release Asset
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ${{ steps.prep.outputs.location }}
          asset_name: my-package-001.zip
          asset_content_type: application/zip
```

---

## 📂 Outputs

| Name     | Description                                    |
|----------|------------------------------------------------|
| location | File path to the created ZIP package file      |

**Output File Details:**
- **Filename Format**: `{PACKAGE_DIRECTORY_NAME}.zip` (e.g., `my-package~my-package-001.zip`)
- **Location**: Stored in `${{ runner.temp }}` directory
- **Content**: Complete package structure ready for CPI Design Time import

**ZIP Structure Example:**
```
my-package~my-package-001.zip
├── SRC/
│   ├── flow1
│   └── flow2
├── ValueMappings/
│   ├── mapping1
│   └── mapping2
├── MANIFEST.MF
├── package.xml
└── [other files from package root]
```

---

## 💡 Tips & Troubleshooting

- **Directory Matching**: The action searches for directories matching `*~{PACKAGE_ID}` pattern in `btp-insuite/IntegrationPackages`. Ensure your package directory follows this naming convention.

- **Single Match Validation**: Exactly one directory matching the pattern must be found. If multiple directories match, the action fails to prevent packaging the wrong package. If no match is found, the action exits with an error.

- **Configuration Skipping**: The `Configuration` directory is intentionally skipped during packaging. This directory typically contains deployment settings and environment-specific configurations that should not be included in the exportable package.

- **Subdirectory Handling**: Subdirectories (except Configuration) are zipped as individual files within the main ZIP:
  1. Contents of each subdirectory are zipped into a temporary file
  2. The temporary file is renamed without the `.zip` extension
  3. The renamed file is included in the final ZIP
  This maintains proper package structure for CPI import.

- **File Copying**: Regular files in the package root are copied directly into the ZIP as-is.

- **Hidden Files**: The action includes hidden files (those starting with `.`) when copying package contents. This ensures complete package replication.

- **ZIP Output Location**: The final ZIP is created in `${{ runner.temp }}` with the same directory name as the source package directory.

- **Temporary Directory**: A temporary directory is created during packaging to organize files before final ZIP creation. This is cleaned up after ZIP creation.

- **File Permissions**: Zipped files preserve their permissions from the source directory. When extracted, these permissions are restored.

- **Large Packages**: Large packages with many subdirectories may take additional time to process. Monitor workflow execution time for timeout concerns on self-hosted runners.

- **Disk Space**: Ensure sufficient temporary disk space for both the intermediate ZIP files and the final package. The action may temporarily require twice the package size in disk space.

- **Working Directory**: The action operates in `btp-insuite/IntegrationPackages`. Ensure this path exists in your repository structure.

- **Deployment-Ready**: The output ZIP is fully prepared for import into SAP BTP Integration Suite using the `deploy-zip-to-cpi` action.

- **Artifact Storage**: Use `upload-artifact` action to preserve the ZIP package across jobs or workflows.

- **Backup Strategy**: Combine with storage actions to automatically backup packages to cloud storage or artifact repositories.

- **Release Distribution**: Use with GitHub Releases to distribute packages as release artifacts for version tracking and download.

- **CI/CD Integration**: This action is typically the final step before deployment, converting repository-stored packages into deployable archives.

- **Error Handling**: Clear error messages indicate if the package directory is not found or multiple directories match the pattern.

- **Verification**: After packaging, use other tools to verify ZIP integrity before deployment if desired.

- **Re-packaging**: Running this action multiple times produces consistent ZIP files from the same source directory.

- **Cross-workflow Usage**: The output location can be stored as a workflow artifact and used in dependent workflows for multi-stage deployments.

---

## 📄 License

This project is licensed under the Apache License 2.0.