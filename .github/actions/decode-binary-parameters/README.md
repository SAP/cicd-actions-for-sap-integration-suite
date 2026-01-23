# 🚀 Decode Binary Parameters GitHub Action

Decodes base64 binary parameters and writes them to files, updating the JSON.

---

## ✨ Overview

This action processes BinaryParameters.json files by decoding base64-encoded binary values, writing them to separate files in a Binary subdirectory, and updating the JSON to reference the file names instead of the base64 content.

---

## ⚙️ Inputs

| Name       | Required | Description                              |
|------------|----------|------------------------------------------|
| partner-id | ✅        | Partner ID                               |
| output-dir | ✅        | Directory to write binary files          |

---

## 📝 Usage Example

```yaml
jobs:
  decode-binaries:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      - name: Decode Binary Parameters
        uses: ./.github/actions/decode-binary-parameters
        with:
          partner-id: 'PARTNER123'
          output-dir: './PartnerDirectory'
```

---

## 🪵 Example Logs

```
Processing BinaryParameters.json for Partner ID: PARTNER123
Decoding binary parameter: Certificate
Writing binary file: PARTNER123_Certificate.jks
Updating JSON with filename reference
```
_These are example logs you may encounter when running this action. Actual logs may vary depending on configuration and runtime conditions._

---

## 📂 Outputs

This action does not produce any outputs. It creates binary files in the Binary subdirectory and updates the BinaryParameters.json file.

---

## 💡 Tips & Troubleshooting

- The action expects a BinaryParameters.json file at: `{output-dir}/{partner-id}/BinaryParameters.json`
- Binary files are written to: `{output-dir}/{partner-id}/Binary/`
- File names are generated as: `{partner-id}_{Id}.{extension}`
- File extensions are derived from the ContentType field; defaults to 'bin' if not determinable.
- The original base64 Value in the JSON is replaced with the filename for easier version control.
- Ensure the BinaryParameters.json file contains valid base64-encoded data in the Value fields.

---

## 📚 References

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/CLOUD_INTEGRATION)
