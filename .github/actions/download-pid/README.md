# 🚀 Download Partner Directory GitHub Action

Downloads Partner Directory entries from BTP Cloud Integration to a specified folder.

---

## ✨ Overview

This composite action downloads all Partner Directory entries (StringParameters, AlternativePartners, AuthorizedUsers, BinaryParameters) from Cloud Integration to a configurable output directory. The downloaded files are raw JSON that can be used by other actions.

> **Note:** This action downloads from **Cloud Integration only**, not from Edge Integration Cell (EIC). Cloud Integration is the source of truth for Partner Directory entries.

---

## ⚙️ Inputs

| Name         | Required | Default    | Description                                      |
|--------------|----------|------------|--------------------------------------------------|
| bearer-token | ✅        | -          | BEARER Token to access Integration Suite Artifacts |
| partner-id   | ✅        | -          | Partner ID                                       |
| btp-api-url  | ✅        | -          | URL on BTP to access APIs                        |
| output-dir   | ❌        | `/tmp/pd`  | Directory to save downloaded JSON files          |

---

## 📤 Outputs

| Name                     | Description                                        |
|--------------------------|---------------------------------------------------|
| output-dir               | Path to the directory containing downloaded files  |
| string-parameters-file   | Path to downloaded StringParameters JSON file      |
| alternative-partners-file| Path to downloaded AlternativePartners JSON file   |
| authorized-users-file    | Path to downloaded AuthorizedUsers JSON file       |
| binary-parameters-file   | Path to downloaded BinaryParameters JSON file      |

---

## 📝 Usage Example

### Basic Usage (download to temp folder)

```yaml
jobs:
  download-partner:
    runs-on: ubuntu-latest
    steps:
      - name: Download Partner Directory Entry
        uses: ./.github/actions/download-pid
        with:
          bearer-token: ${{ secrets.BEARER_TOKEN }}
          btp-api-url: ${{ vars.BTP_API_URL }}
          partner-id: 'PARTNER123'
```

### Download to Git Repository (with convert-pid-to-git)

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

## 🪵 Example Logs

```
========================================
📥 Downloading Partner Directory
========================================
Partner ID: PARTNER123
Output Directory: /tmp/pd
----------------------------------------
🔍 Checking Partner ID existence...
✅ Partner ID PARTNER123 exists

📄 Downloading StringParameters...
   ✅ Downloaded 5 entries → /tmp/pd/StringParameters.json

📄 Downloading AlternativePartners...
   ✅ Downloaded 2 entries → /tmp/pd/AlternativePartners.json

📄 Downloading AuthorizedUsers...
   ✅ Downloaded 3 entries → /tmp/pd/AuthorizedUsers.json

📄 Downloading BinaryParameters...
   ✅ Downloaded 1 entries → /tmp/pd/BinaryParameters.json

========================================
✅ Download completed successfully
========================================
```
_These are example logs you may encounter when running this action._

---

## 📂 Output Files

The action creates JSON files in the output directory:
- `StringParameters.json` - Array of string parameter entries
- `AlternativePartners.json` - Array of alternative partner entries
- `AuthorizedUsers.json` - Array of authorized user entries
- `BinaryParameters.json` - Array of binary parameter entries

Each file contains the raw `.d.results` array from the OData API response.

---

## 💡 Tips & Troubleshooting

- Use this action with `convert-pid-to-git` to save Partner Directory to Git with cleaned JSON and decoded binary files.
- Use this action with `sync-pid-to-eic` to sync Partner Directory to Edge Integration Cell runtimes.
- The action validates that the Partner ID exists before attempting to download.
- Ensure the bearer token has read access to the Partner Directory API.

---

## 📚 References

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/CLOUD_INTEGRATION)
- [convert-pid-to-git Action](../convert-pid-to-git/README.md)
- [sync-pid-to-eic Action](../sync-pid-to-eic/README.md)