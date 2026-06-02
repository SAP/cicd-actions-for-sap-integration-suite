# 🗑️ Delete Partner Directory Entry GitHub Action

Deletes a Partner Directory entry from BTP Cloud Integration and/or Edge Integration Cell runtimes.

---

## ✨ Overview

This composite action deletes a Partner Directory entry (Partner ID) from Cloud Integration and/or EIC runtimes. You can control whether to delete from Cloud Integration, EIC runtimes, or both.

---

## ⚙️ Inputs

| Name           | Required | Default  | Description                                                                |
|----------------|----------|----------|----------------------------------------------------------------------------|
| bearer-token   | ✅        | -        | OAuth Bearer Token for API authentication                                  |
| btp-api-url    | ✅        | -        | URL on BTP to access APIs                                                  |
| partner-id     | ✅        | -        | Partner ID to delete                                                       |
| delete-from-ci   | ❌        | `"true"` | Whether to delete from Cloud Integration. Set to `"false"` to skip CI.     |
| eic-runtimes     | ❌        | `""`     | Comma-separated list of EIC runtime identifiers to delete from             |
| eic-url-template | ❌        | `""`     | URL path template for EIC API access. Contains `{runtime}` as placeholder. **Not published — subject to change.** Required when `eic-runtimes` is set. |

---

## 📝 Usage Examples

### Delete from Cloud Integration Only (Default)

```yaml
jobs:
  delete-partner:
    runs-on: ubuntu-latest
    steps:
      - name: Delete Partner Directory Entry
        uses: ./.github/actions/delete-partner-directory-entry
        with:
          bearer-token: ${{ secrets.BEARER_TOKEN }}
          btp-api-url: ${{ vars.BTP_API_URL }}
          partner-id: 'PARTNER123'
```

### Delete from Cloud Integration and EIC Runtimes

```yaml
jobs:
  delete-partner:
    runs-on: ubuntu-latest
    steps:
      - name: Delete Partner Directory Entry
        uses: ./.github/actions/delete-partner-directory-entry
        with:
          bearer-token: ${{ secrets.BEARER_TOKEN }}
          btp-api-url: ${{ vars.BTP_API_URL }}
          partner-id: 'PARTNER123'
          eic-runtimes: 'deveicmbag, testeicmbag'
          eic-url-template: ${{ vars.BTP_EIC_URL_TEMPLATE }}
```

### Delete from EIC Runtimes Only (Skip Cloud Integration)

```yaml
jobs:
  delete-partner:
    runs-on: ubuntu-latest
    steps:
      - name: Delete Partner Directory Entry from EIC only
        uses: ./.github/actions/delete-partner-directory-entry
        with:
          bearer-token: ${{ secrets.BEARER_TOKEN }}
          btp-api-url: ${{ vars.BTP_API_URL }}
          partner-id: 'PARTNER123'
          delete-from-ci: 'false'
          eic-runtimes: 'deveicmbag, testeicmbag'
          eic-url-template: ${{ vars.BTP_EIC_URL_TEMPLATE }}
```

---

## 🔄 How It Works

1. **If `delete-from-ci` is `"true"` (default)**: Deletes from Cloud Integration
2. **If `delete-from-ci` is `"false"`**: Skips Cloud Integration deletion
3. **If `eic-runtimes` is provided**: Deletes from each specified EIC runtime
4. **Handles 404 gracefully**: If a Partner ID doesn't exist in a target, it's logged but not treated as an error
5. **Continues on errors**: Deletion continues for remaining targets even if one fails
6. **Fails if no targets**: If both CI deletion is disabled and no EIC runtimes are provided, the action fails

---

## 🪵 Example Logs

### Delete from Both CI and EIC
```
=========================================
🗑️ Deleting Partner Directory Entry
=========================================
📦 Partner ID: PARTNER123
📍 Delete from CI: true
📍 EIC Runtimes: deveicmbag, testeicmbag

🗑️ Deleting Partner ID PARTNER123 from Cloud Integration
   🔗 API Endpoint: https://xxx.integrationsuite.cfapps.eu10.hana.ondemand.com/api/v1/Partners('PARTNER123')
   ✅ Successfully deleted (HTTP 204)

🗑️ Deleting Partner ID PARTNER123 from EIC (deveicmbag)
   ✅ Successfully deleted (HTTP 204)

=========================================
✅ Deletion completed successfully
=========================================
```

### Delete from EIC Only
```
=========================================
🗑️ Deleting Partner Directory Entry
=========================================
📦 Partner ID: PARTNER123
📍 Delete from CI: false
📍 EIC Runtimes: deveicmbag

ℹ️ Skipping Cloud Integration deletion (delete-from-ci=false)

🗑️ Deleting Partner ID PARTNER123 from EIC (deveicmbag)
   ✅ Successfully deleted (HTTP 204)

=========================================
✅ Deletion completed successfully
=========================================
```

---

## 💡 Tips & Troubleshooting

- **Default behavior**: Deletes from Cloud Integration only (for backward compatibility)
- **Multiple EICs**: Separate EIC runtime identifiers with commas. Spaces are trimmed automatically.
- **404 responses** (Partner ID not found) are treated as success and logged with ℹ️.
- **Authentication**: Ensure the bearer token has permissions to delete from both Cloud Integration and the specified EIC runtimes.
- **At least one target required**: Either `delete-from-ci` must be `"true"` or `eic-runtimes` must be provided.
- **EIC URL Template**: The EIC API path is not yet published — pre-work to support EIC, subject to change. Configure `BTP_EIC_URL_TEMPLATE` in your GitHub environment.

---

## 📚 References

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/CLOUD_INTEGRATION)
- [Edge Integration Cell Documentation](https://help.sap.com/docs/integration-suite/sap-integration-suite/edge-integration-cell)