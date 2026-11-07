# 🚀 Create Partner Directory GitHub Action

Creates a partner directory structure and copies provided JSON files.

---

## ✨ Overview

This action creates a Partner Directory folder structure in the repository and copies the four required JSON files (StringParameters, AlternativePartners, AuthorizedUsers, BinaryParameters) into the partner-specific directory. If the directory already exists, it is deleted and recreated.

---

## ⚙️ Inputs

| Name                | Required | Description                              |
|---------------------|----------|------------------------------------------|
| partner-id          | ✅        | Partner ID for directory creation        |
| StringParameters    | ✅        | Path to StringParameters file            |
| AlternativePartners | ✅        | Path to AlternativePartners file         |
| AuthorizedUsers     | ✅        | Path to AuthorizedUsers file             |
| BinaryParameters    | ✅        | Path to BinaryParameters file            |

---

## 📝 Usage Example

```yaml
jobs:
  create-pd:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v7
      - name: Create Partner Directory
        uses: ./.github/actions/create-partner-directory
        with:
          partner-id: 'PARTNER123'
          StringParameters: '/tmp/StringParameters.json'
          AlternativePartners: '/tmp/AlternativePartners.json'
          AuthorizedUsers: '/tmp/AuthorizedUsers.json'
          BinaryParameters: '/tmp/BinaryParameters.json'
```

---

## 🪵 Example Logs

```
Creating directory: PartnerDirectory/PARTNER123
Copying StringParameters.json...
Copying AlternativePartners.json...
Copying AuthorizedUsers.json...
Copying BinaryParameters.json...
✅ Partner Directory created successfully
```
_These are example logs you may encounter when running this action. Actual logs may vary depending on configuration and runtime conditions._

---

## 📂 Outputs

This action does not produce any outputs. It creates the directory structure in the repository.

---

## 💡 Tips & Troubleshooting

- The action creates the directory at: `btp-insuite/PartnerDirectory/{partner-id}/`
- If the directory already exists, it is completely removed and recreated.
- All four JSON files are required inputs.
- The JSON files are renamed during copy to match the standard naming convention.
- This action is typically used after downloading Partner Directory data from BTP.
- Ensure the working directory is set correctly (the action uses `btp-insuite` as the working directory).

---

## 📚 References

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/CLOUD_INTEGRATION)