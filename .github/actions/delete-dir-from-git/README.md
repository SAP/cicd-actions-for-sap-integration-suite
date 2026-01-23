# 🚀 Delete Directory from GIT GitHub Action

Deletes a directory from the Git repository based on ID.

---

## ✨ Overview

This action searches for and deletes a directory matching a specific ID pattern from either the IntegrationPackages or PartnerDirectory folder. It validates that exactly one matching directory exists before deletion to prevent accidental removal of multiple directories.

---

## ⚙️ Inputs

| Name | Required | Description                                      |
|------|----------|--------------------------------------------------|
| id   | ✅        | ID of the directory to delete                    |
| mode | ✅        | Mode IntegrationPackages/PartnerDirectory        |

---

## 📝 Usage Example

```yaml
jobs:
  delete-directory:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      - name: Delete Integration Package
        uses: ./.github/actions/delete-dir-from-git
        with:
          id: 'DBF_PARTNER_INTEGRATION'
          mode: 'IntegrationPackages'
```

---

## 🪵 Example Logs

```
Looking for top-level directories ending in DBF_PARTNER_INTEGRATION in root...
✅ Found only one matching directory: Partner_Integration~DBF_PARTNER_INTEGRATION
Deleting directory: ./Partner_Integration~DBF_PARTNER_INTEGRATION
✅ Successfully deleted Partner_Integration~DBF_PARTNER_INTEGRATION
```
_These are example logs you may encounter when running this action. Actual logs may vary depending on configuration and runtime conditions._

---

## 📂 Outputs

This action does not produce any outputs. It deletes the matching directory from the repository.

---

## 💡 Tips & Troubleshooting

- The action searches for directories with names ending in the specified ID (pattern: `*{ID}`).
- If multiple directories match, the action fails to prevent accidental deletion.
- If no directory matches, the action exits gracefully with a warning (exit code 0).
- The mode parameter determines the search location:
  - `IntegrationPackages`: searches in `btp-insuite/IntegrationPackages/`
  - `PartnerDirectory`: searches in `btp-insuite/PartnerDirectory/`
- Directory names typically follow the pattern: `{Name}~{ID}`
- Use this action carefully as deletion is permanent within the Git workflow.
- Ensure you commit and push the changes after running the action to persist the deletion.

---

## 📚 References

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/CLOUD_INTEGRATION)