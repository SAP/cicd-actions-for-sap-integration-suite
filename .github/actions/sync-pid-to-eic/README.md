# 🚀 Sync Partner Directory to EIC GitHub Action

Synchronizes Partner Directory entries from Cloud Integration to Edge Integration Cell runtimes.

---

## ✨ Overview

This composite action syncs Partner Directory entries from Cloud Integration (the source of truth) to one or more Edge Integration Cell (EIC) runtimes. It first downloads the entries using `download-pid`, then pushes them to each specified EIC runtime using the Partner Directory REST API for EIC.

This action is designed for CI/CD scenarios where you need to keep EIC runtimes in sync with Cloud Integration Partner Directory entries.

---

## ⚙️ Inputs

| Name             | Required | Description                                                    |
|------------------|----------|----------------------------------------------------------------|
| bearer-token     | ✅        | OAuth Bearer Token for API authentication                      |
| btp-api-url      | ✅        | URL on BTP to access APIs                                      |
| partner-id       | ✅        | Partner ID to sync                                             |
| eic-runtimes     | ✅        | Comma-separated list of Edge Integration Cell runtime identifiers |
| eic-url-template | ❌        | URL path template for EIC API access. Contains `{runtime}` as placeholder for the runtime identifier. **Not published — subject to change.** Required when `eic-runtimes` is set. |

---

## 📝 Usage Example

### Sync to Single EIC

```yaml
jobs:
  sync-partner-directory:
    runs-on: ubuntu-latest
    steps:
      - name: Sync Partner Directory to EIC
        uses: ./.github/actions/sync-pid-to-eic
        with:
          bearer-token: ${{ secrets.BEARER_TOKEN }}
          btp-api-url: ${{ vars.BTP_API_URL }}
          partner-id: 'PARTNER123'
          eic-runtimes: 'deveicmbag'
          eic-url-template: ${{ vars.BTP_EIC_URL_TEMPLATE }}
```

### Sync to Multiple EICs

```yaml
jobs:
  sync-partner-directory:
    runs-on: ubuntu-latest
    steps:
      - name: Sync Partner Directory to EICs
        uses: ./.github/actions/sync-pid-to-eic
        with:
          bearer-token: ${{ secrets.BEARER_TOKEN }}
          btp-api-url: ${{ vars.BTP_API_URL }}
          partner-id: 'PARTNER123'
          eic-runtimes: 'deveicmbag, testeicmbag, prodeicmbag'
          eic-url-template: ${{ vars.BTP_EIC_URL_TEMPLATE }}
```

---

## 🔄 How It Works

1. **Download**: The action downloads Partner Directory entries from Cloud Integration using `download-pid`
2. **Parse EICs**: The comma-separated EIC runtimes list is parsed
3. **Sync Each EIC**: For each EIC runtime:
   - Builds the EIC-specific API endpoint using the `eic-url-template` and the runtime identifier
   - Posts each Partner Directory entry (StringParameters, AlternativePartners, AuthorizedUsers, BinaryParameters) to the EIC
   - Handles HTTP 409 (conflict/already exists) as success

---

## 🪵 Example Logs

```
========================================
🔄 Syncing Partner Directory to Edge Integration Cells
========================================
Partner ID: PARTNER123
EIC Runtimes: deveicmbag, testeicmbag
Input Directory: /tmp/pd-sync
----------------------------------------

📍 Syncing to EIC: deveicmbag
-----------------------------------------
   📤 StringParameters: Syncing 5 entries...
      ✅ StringParameters: 5/5 entries synced
   📤 AlternativePartners: Syncing 2 entries...
      ✅ AlternativePartners: 2/2 entries synced
   📤 AuthorizedUsers: Syncing 3 entries...
      ✅ AuthorizedUsers: 3/3 entries synced
   📤 BinaryParameters: Syncing 1 entries...
      ✅ BinaryParameters: 1/1 entries synced
   ✅ EIC deveicmbag: Sync completed successfully

📍 Syncing to EIC: testeicmbag
-----------------------------------------
   ...

========================================
📊 EIC Sync Summary
========================================
Partner ID: PARTNER123
✅ Successful EICs: 2
⚠️ EICs with errors: 0
========================================
```

---

## 🔗 EIC API Endpoint

The action builds the EIC-specific API endpoint using the `eic-url-template` input and the runtime identifier. The URL path template is not yet published — subject to change. Configure `BTP_EIC_URL_TEMPLATE` in your GitHub environment.

---

## 💡 Tips & Troubleshooting

- **Source of Truth**: Cloud Integration is always the source of truth for Partner Directory entries. This action syncs FROM Cloud Integration TO EIC.
- **Multiple EICs**: Separate multiple EIC runtime identifiers with commas. Spaces are trimmed automatically.
- **Conflict Handling**: HTTP 409 responses (entry already exists) are treated as success.
- **Authentication**: Ensure the bearer token has access to both Cloud Integration and the target EIC runtimes.
- **EIC Runtime Names**: Find your EIC runtime identifiers in your BTP cockpit or Integration Suite setup.
- **EIC URL Template**: The EIC API path is not yet published — pre-work to support EIC, subject to change. Configure `BTP_EIC_URL_TEMPLATE` in your GitHub environment variables.

---

## 📚 References

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/CLOUD_INTEGRATION)
- [Edge Integration Cell Documentation](https://help.sap.com/docs/integration-suite/sap-integration-suite/edge-integration-cell)
- [download-pid Action](../download-pid/README.md)