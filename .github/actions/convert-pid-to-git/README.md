# 🚀 Convert Partner Directory to Git GitHub Action

Converts downloaded Partner Directory JSON files to Git repository structure.

---

## ✨ Overview

This composite action takes Partner Directory JSON files (downloaded by `download-pid`) and converts them into a structured Git repository format. It cleans the JSON (removes unnecessary metadata), creates the Partner Directory folder structure, and decodes binary parameters.

This action is designed to be used after `download-pid` when you want to store Partner Directory entries in Git.

---

## ⚙️ Inputs

| Name         | Required | Default                        | Description                                      |
|--------------|----------|--------------------------------|--------------------------------------------------|
| partner-id   | ✅        | -                              | Partner ID                                       |
| input-dir    | ✅        | -                              | Directory containing downloaded JSON files       |
| output-dir   | ❌        | `btp-insuite/PartnerDirectory` | Directory for Git repository structure           |

---

## 📝 Usage Example

### Typical Usage (with download-pid)

```yaml
jobs:
  download-partner:
    runs-on: ubuntu-latest
    steps:
      - name: Download Partner Directory
        uses: ./.github/actions/download-pid
        with:
          bearer-token: ${{ secrets.BEARER_TOKEN }}
          btp-api-url: ${{ vars.BTP_API_URL }}
          partner-id: 'PARTNER123'
          output-dir: /tmp/pd-download

      - name: Convert to Git Structure
        uses: ./.github/actions/convert-pid-to-git
        with:
          partner-id: 'PARTNER123'
          input-dir: /tmp/pd-download
          output-dir: btp-insuite/PartnerDirectory
```

---

## 📂 Output Structure

The action creates the following structure in the output directory:

```
btp-insuite/PartnerDirectory/
└── PARTNER123/
    ├── StringParameters.json      (cleaned JSON)
    ├── AlternativePartners.json   (cleaned JSON)
    ├── AuthorizedUsers.json       (cleaned JSON)
    ├── BinaryParameters.json      (cleaned JSON with file references)
    └── binaries/                  (decoded binary files)
        └── cert.pem
```

---

## 🧹 JSON Cleaning

The action removes unnecessary metadata fields, keeping only essential data for version control:

| Type                | Retained Fields           |
|---------------------|---------------------------|
| StringParameters    | Pid, Id, Value            |
| AlternativePartners | Pid, Agency, Id, Scheme   |
| AuthorizedUsers     | Pid, User                 |
| BinaryParameters    | Pid, ContentType, Id, Value |

---

## 💡 Tips & Troubleshooting

- Always use this action after `download-pid` to convert raw downloaded JSON to Git-friendly format.
- The action uses existing helper actions: `clean-json-nodes`, `create-partner-directory`, and `decode-binary-parameters`.
- Binary parameter values are decoded from base64 and stored as separate files in a `binaries/` subdirectory.
- The cleaned JSON files are suitable for version control and diff comparison.

---

## 📚 References

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/CLOUD_INTEGRATION)
- [download-pid Action](../download-pid/README.md)