# 🚀 Download Package GitHub Action

Downloads an Integration Suite package from BTP to Git repository.

---

## ✨ Overview

This composite action orchestrates the complete process of downloading an Integration Suite package from BTP, extracting it, retrieving external parameters, and creating deployment files. It handles package preparation, ZIP extraction, IFlow parameter retrieval, and configuration merging.

---

## ⚙️ Inputs

| Name         | Required | Description                                      |
|--------------|----------|--------------------------------------------------|
| bearer-token | ✅        | BEARER Token to access Integration Suite Artifacts |
| package-id   | ✅        | Package ID                                       |
| btp-api-url  | ✅        | URL on BTP to access APIs                        |

---

## 📝 Usage Example

```yaml
jobs:
  download-package:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      - name: Download Integration Package
        uses: ./.github/actions/download-package
        with:
          bearer-token: ${{ secrets.BEARER_TOKEN }}
          btp-api-url: ${{ vars.BTP_API_URL }}
          package-id: 'DBF_PARTNER_INTEGRATION'
```

---

## 🪵 Example Logs

```
[INFO] Getting package name for DBF_PARTNER_INTEGRATION...
[INFO] Downloading package as ZIP...
[INFO] Preparing repository by deleting old package version...
[INFO] Extracting package into repository...
[INFO] Getting IFlow IDs from package...
[INFO] Retrieving external parameters for IFlows...
[INFO] Merging new parameters with existing configuration...
[INFO] Creating IFlow deployment file...
[INFO] Package download completed successfully.
```
_These are example logs you may encounter when running this action. Actual logs may vary depending on configuration and runtime conditions._

---

## 📂 Outputs

This action does not produce direct outputs. It creates the following in the repository:
- Extracted package files
- External parameters configuration JSON
- IFlow deployment configuration files

---

## 💡 Tips & Troubleshooting

- This is a composite action that orchestrates multiple sub-actions.
- The action automatically handles merging of old and new external parameters, preserving non-default values.
- Ensure the bearer token has read access to Integration Suite packages and artifacts.
- The package will be extracted into the IntegrationPackages directory in your repository.
- If a package already exists in the repository, the old version will be deleted before extracting the new one.
- External parameters are only retrieved for Integration Flows (IFlows), not other artifact types.

---

## 📚 References

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/CLOUD_INTEGRATION)
