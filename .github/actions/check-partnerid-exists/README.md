# 🚀 Check Partner ID Exists GitHub Action

Validates that a Partner ID exists in the BTP Partner Directory.

---

## ✨ Overview

This action checks whether a specific Partner ID exists in the BTP Partner Directory by querying the API and validating that exactly one unique entry is returned for the given Partner ID.

---

## ⚙️ Inputs

| Name         | Required | Description                                      |
|--------------|----------|--------------------------------------------------|
| bearer-token | ✅        | BEARER Token to access Partner Directory        |
| btp-api-url  | ✅        | URL on BTP to access APIs                        |
| partner-id   | ✅        | Partner ID to check for existence                |

---

## 📝 Usage Example

```yaml
jobs:
  check-partner:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v7
      - name: Check if Partner ID exists
        uses: ./.github/actions/check-partnerid-exists
        with:
          bearer-token: ${{ secrets.BEARER_TOKEN }}
          btp-api-url: ${{ vars.BTP_API_URL }}
          partner-id: 'PARTNER123'
```

---

## 🪵 Example Logs

```
Check whether Partner ID PARTNER123 exists via https://api.btp.example.com/api/v1/Partners?$format=json&$filter=Pid%20eq%20'PARTNER123'
Partner ID PARTNER123 exists and is unique in response.
```
_These are example logs you may encounter when running this action. Actual logs may vary depending on configuration and runtime conditions._

---

## 📂 Outputs

This action does not produce any outputs. It exits with an error if the Partner ID does not exist or is not unique.

---

## 💡 Tips & Troubleshooting

- Ensure the bearer token has sufficient permissions to access the Partner Directory API.
- The action validates that exactly one result is returned to ensure uniqueness.
- HTTP status code must be 200 for successful validation.
- If the Partner ID doesn't exist, the action will fail with exit code 1.

---

## 📚 References

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/CLOUD_INTEGRATION)
