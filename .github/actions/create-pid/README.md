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
| BTP_API_PASSWORD | ✅        | BTP API Password                                                 |
| BTP_TEC_PASSWORD | ✅        | BTP Technical User Password                                      |

---

## 📝 Usage Example

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

---

## 🪵 Example Logs

```
🔍 Looking for Partner ID: PARTNER123
📂 Current directory: /home/runner/work/repo
✅ Found Partner ID directory: ./PartnerDirectory/PARTNER123
📄 Processing: ./PartnerDirectory/PARTNER123/AlternativePartners.json
📄 Processing: ./PartnerDirectory/PARTNER123/AuthorizedUsers.json
📄 Processing: ./PartnerDirectory/PARTNER123/StringParameters.json
📄 Processing: ./PartnerDirectory/PARTNER123/BinaryParameters.json
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

---

## 📚 References

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/CLOUD_INTEGRATION)
