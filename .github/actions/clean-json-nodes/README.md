# 🚀 Clean JSON Nodes GitHub Action

Cleans a JSON file, keeping only specified nodes.

---

## ✨ Overview

This action filters a JSON file to retain only specified node paths, removing all other metadata and unnecessary fields. This is particularly useful for cleaning Partner Directory API responses to keep only the essential data for version control.

---

## ⚙️ Inputs

| Name       | Required | Description                                                                              |
|------------|----------|------------------------------------------------------------------------------------------|
| filename   | ✅        | Path to the JSON file to clean                                                           |
| keep_nodes | ✅        | Comma-separated list of JSON node paths to keep (e.g., d.results.Id,d.results.Value)    |

---

## 📝 Usage Example

```yaml
jobs:
  clean-json:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v7
      - name: Clean JSON StringParameters
        uses: ./.github/actions/clean-json-nodes
        with:
          filename: './partner-data/StringParameters.json'
          keep_nodes: 'd.results.Pid,d.results.Id,d.results.Value'
```

---

## 🪵 Example Logs

```
Cleaning JSON file: ./partner-data/StringParameters.json
Keeping nodes: Pid, Id, Value
✅ JSON file cleaned successfully
```
_These are example logs you may encounter when running this action. Actual logs may vary depending on configuration and runtime conditions._

---

## 📂 Outputs

This action does not produce any outputs. It modifies the input JSON file in-place.

---

## 💡 Tips & Troubleshooting

- The action expects node paths in the format `d.results.PropertyName`.
- Multiple properties are separated by commas.
- The JSON structure is preserved with `{d: {results: [...]}}` format.
- The original file is overwritten with the cleaned version.
- Common keep_nodes patterns:
  - **StringParameters**: `d.results.Pid,d.results.Id,d.results.Value`
  - **AlternativePartners**: `d.results.Pid,d.results.Agency,d.results.Id,d.results.Scheme`
  - **AuthorizedUsers**: `d.results.Pid,d.results.User`
  - **BinaryParameters**: `d.results.Pid,d.results.ContentType,d.results.Id,d.results.Value`

---

## 📚 References

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/CLOUD_INTEGRATION)