# 🚀 Download Partner ID GitHub Action

Downloads a Partner Directory entry from BTP to Git repository.

---

## ✨ Overview

This composite action orchestrates the complete process of downloading a Partner Directory entry from BTP, including all parameter types (StringParameters, AlternativePartners, AuthorizedUsers, BinaryParameters), cleaning the JSON data, and creating the Partner Directory structure in the repository.

---

## ⚙️ Inputs

| Name         | Required | Description                                      |
|--------------|----------|--------------------------------------------------|
| bearer-token | ✅        | BEARER Token to access Integration Suite Artifacts |
| partner-id   | ✅        | Partner ID                                       |
| btp-api-url  | ✅        | URL on BTP to access APIs                        |

---

## 📝 Usage Example

```yaml
jobs:
  download-partner:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      - name: Download Partner Directory Entry
        uses: ./.github/actions/download-pid
        with:
          bearer-token: ${{ secrets.BEARER_TOKEN }}
          btp-api-url: ${{ vars.BTP_API_URL }}
          partner-id: 'PARTNER123'
```

---

## 🪵 Example Logs

```
[INFO] Checking Partner ID existence...
[INFO] Getting StringParameters for PARTNER123...
[INFO] Cleaning JSON StringParameters...
[INFO] Getting AlternativePartners for PARTNER123...
[INFO] Cleaning JSON AlternativePartners...
[INFO] Getting AuthorizedUsers for PARTNER123...
[INFO] Cleaning JSON AuthorizedUsers...
[INFO] Getting BinaryParameters for PARTNER123...
[INFO] Cleaning JSON BinaryParameters...
[INFO] Creating Partner Directory structure...
[INFO] Partner Directory download completed successfully.
```
_These are example logs you may encounter when running this action. Actual logs may vary depending on configuration and runtime conditions._

---

## 📂 Outputs

This action does not produce direct outputs. It creates the following:
- Partner Directory folder structure in the repository
- JSON files for all parameter types (StringParameters, AlternativePartners, AuthorizedUsers, BinaryParameters)

---

## 💡 Tips & Troubleshooting

- This is a composite action that orchestrates multiple sub-actions.
- The action first validates that the Partner ID exists before attempting to download.
- JSON cleaning removes unnecessary metadata fields, keeping only essential data for version control.
- Retained fields per type:
  - **StringParameters**: Pid, Id, Value
  - **AlternativePartners**: Pid, Agency, Id, Scheme
  - **AuthorizedUsers**: Pid, User
  - **BinaryParameters**: Pid, ContentType, Id, Value
- Ensure the bearer token has read access to the Partner Directory API.
- The Partner Directory structure is created in the PartnerDirectory folder in your repository.

---

## 📚 References

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/CLOUD_INTEGRATION)