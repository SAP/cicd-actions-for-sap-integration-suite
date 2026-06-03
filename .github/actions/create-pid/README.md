# 🚀 Create Partner ID in BTP GitHub Action

Creates a complete Partner ID in BTP including all associated Partner Directory entries.

---

## ✨ Overview

This composite action orchestrates the creation of a Partner ID in BTP by checking out the repository, obtaining OAuth tokens, locating Partner Directory JSON files, validating their structure, and creating all necessary entries (AlternativePartners, AuthorizedUsers, StringParameters, BinaryParameters).

---

## ⚙️ Inputs

| Name             | Required | Description                                                      |
|------------------|----------|------------------------------------------------------------------|
| target-env       | ✅        | Environment                                                      |
| source-ref       | ✅        | GIT Source Reference                                             |
| partner-id       | ✅        | Partner ID to create                                             |
| btp-api-user     | ✅        | BTP Service Key (ClientID) to access Token Endpoint             |
| btp-tec-user     | ✅        | BTP technical User with Access Policy for Integration Suite     |
| btp-token-url    | ✅        | URL on BTP to request Token                                      |
| btp-api-url      | ✅        | URL on BTP to access APIs                                        |
| eic-runtimes     | ❌        | Comma-separated list of Edge Integration Cell runtime identifiers. When provided, Partner Directory entries are also synced to all specified EIC runtimes. |
| eic-url-template | ❌        | URL path template for EIC API access. Contains `{runtime}` as placeholder for the runtime identifier. **Not published — subject to change.** Required when `eic-runtimes` is set. |
| BTP_API_PASSWORD | ✅        | BTP API Password                                                 |
| BTP_TEC_PASSWORD | ✅        | BTP Technical User Password                                      |

---

## 📝 Usage Example

### Standard (Cloud Integration Only)
```yaml
jobs:
  create-partner:
    runs-on: ubuntu-latest
    steps:
      - name: Create Partner ID in BTP
        uses: ./.github/actions/create-pid
        with:
          target-env: 'production'
          source-ref: 'main'
          partner-id: 'PARTNER123'
          btp-api-user: ${{ secrets.BTP_API_USER }}
          btp-tec-user: ${{ secrets.BTP_TEC_USER }}
          btp-token-url: ${{ vars.BTP_TOKEN_URL }}
          btp-api-url: ${{ vars.BTP_API_URL }}
          BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
          BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}
```

### With Edge Integration Cell Sync
```yaml
jobs:
  create-partner-with-eic:
    runs-on: ubuntu-latest
    steps:
      - name: Create Partner ID in BTP and sync to EIC
        uses: ./.github/actions/create-pid
        with:
          target-env: 'production'
          source-ref: 'main'
          partner-id: 'PARTNER123'
          btp-api-user: ${{ secrets.BTP_API_USER }}
          btp-tec-user: ${{ secrets.BTP_TEC_USER }}
          btp-token-url: ${{ vars.BTP_TOKEN_URL }}
          btp-api-url: ${{ vars.BTP_API_URL }}
          eic-runtimes: 'eicruntime01,deveiceur'
          eic-url-template: ${{ vars.BTP_EIC_URL_TEMPLATE }}
          BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
          BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}
```

---

## 🪵 Example Logs

### Cloud Integration
```
🔍 Looking for Partner ID: PARTNER123
📂 Current directory: /home/runner/work/repo
✅ Found Partner ID directory: ./PartnerDirectory/PARTNER123
📄 Processing: ./PartnerDirectory/PARTNER123/AlternativePartners.json
📄 Processing: ./PartnerDirectory/PARTNER123/AuthorizedUsers.json
📄 Processing: ./PartnerDirectory/PARTNER123/StringParameters.json
📄 Processing: ./PartnerDirectory/PARTNER123/BinaryParameters.json
```

### With EIC Sync
```
🔍 Looking for Partner ID: PARTNER123
📂 Current directory: /home/runner/work/repo
✅ Found Partner ID directory: ./PartnerDirectory/PARTNER123
📄 Processing: ./PartnerDirectory/PARTNER123/AlternativePartners.json
📄 Processing: ./PartnerDirectory/PARTNER123/StringParameters.json
...
🔄 Syncing Partner Directory to Edge Integration Cells
📍 Processing EIC runtime: eicruntime01
   ✅ AlternativePartners: 3 entries synced
   ✅ StringParameters: 5 entries synced
📍 Processing EIC runtime: deveiceur
   ✅ AlternativePartners: 3 entries synced
   ✅ StringParameters: 5 entries synced
```
_These are example logs you may encounter when running this action. Actual logs may vary depending on configuration and runtime conditions._

---

## 📂 Outputs

This action does not produce any outputs. It creates the Partner ID and all associated entries in BTP.

---

## 💡 Tips & Troubleshooting

- Ensure the PartnerDirectory folder exists in your repository with the correct structure.
- Each Partner ID should have its own subdirectory under PartnerDirectory containing the JSON files:
  - AlternativePartners.json
  - AuthorizedUsers.json
  - StringParameters.json
  - BinaryParameters.json
- The action requires proper OAuth credentials and token endpoint access.
- If the Partner ID directory is not found, verify the directory name matches the partner-id input exactly.

### Edge Integration Cell (EIC) Support
- When `eic-runtimes` is provided, entries are first created in Cloud Integration, then synced to all specified EIC runtimes.
- EIC runtimes should be specified as a comma-separated list (e.g., `eicruntime01,deveiceur`).
- The same bearer token is used for both Cloud Integration and EIC APIs.
- Each EIC runtime receives the same Partner Directory entries created in Cloud Integration.
- The EIC API path is not yet published — subject to change. Configure `BTP_EIC_URL_TEMPLATE` in your GitHub environment.

---

## 📚 References

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/CLOUD_INTEGRATION)
