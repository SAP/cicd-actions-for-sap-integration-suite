# 🚀 Delete Partner Directory Entry GitHub Action

Deletes a Partner Directory entry from BTP.

---

## ✨ Overview

This action deletes a Partner ID and all its associated entries from the BTP Partner Directory by making a DELETE request to the Partners API endpoint.

---

## ⚙️ Inputs

| Name         | Required | Description                                      |
|--------------|----------|--------------------------------------------------|
| bearer-token | ✅        | BEARER Token to access Partner Directory        |
| btp-api-url  | ✅        | URL on BTP to access APIs                        |
| partner-id   | ✅        | Partner ID to delete                             |

---

## 📝 Usage Example

```yaml
jobs:
  delete-partner:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      - name: Delete Partner Directory Entry
        uses: ./.github/actions/delete-partner-directory-entry
        with:
          bearer-token: ${{ secrets.BEARER_TOKEN }}
          btp-api-url: ${{ vars.BTP_API_URL }}
          partner-id: 'PARTNER123'
```

---

## 🪵 Example Logs

```
DELETE Partner ID PARTNER123 from https://api.btp.example.com/api/v1/Partners('PARTNER123')
HTTP status 204 received. Deletion of PARTNER123 successfully!
```
_These are example logs you may encounter when running this action. Actual logs may vary depending on configuration and runtime conditions._

---

## 📂 Outputs

This action does not produce any outputs. It deletes the Partner ID and exits with an error if deletion fails.

---

## 💡 Tips & Troubleshooting

- The action expects HTTP status code 204 (No Content) for successful deletion.
- Ensure the bearer token has sufficient permissions to delete Partner Directory entries.
- This action will delete the Partner ID and all associated entries (AlternativePartners, AuthorizedUsers, StringParameters, BinaryParameters).
- If the Partner ID doesn't exist, the deletion will fail with an error.
- Use this action with caution as deletion is permanent.

---

## 📚 References

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/CLOUD_INTEGRATION)
