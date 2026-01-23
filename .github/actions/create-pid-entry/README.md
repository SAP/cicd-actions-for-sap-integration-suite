# 🚀 Create Partner ID Entry GitHub Action

Creates Partner Directory entries in BTP for various entity types.

---

## ✨ Overview

This action creates entries in the BTP Partner Directory for different entity types including AlternativePartners, AuthorizedUsers, StringParameters, and BinaryParameters. It validates JSON structure, processes single or multiple entries, and provides detailed logging of the creation process.

---

## ⚙️ Inputs

| Name           | Required | Description                                                                                      |
|----------------|----------|--------------------------------------------------------------------------------------------------|
| bearer-token   | ✅        | OAuth Bearer Token for API authentication                                                        |
| parameter-json | ✅        | Path to JSON file or JSON content for creation                                                   |
| type           | ✅        | Type of Partner Directory entity (AlternativePartners, AuthorizedUsers, StringParameters, BinaryParameters) |
| btp-api-url    | ✅        | URL on BTP to access APIs                                                                        |

---

## 📝 Usage Example

```yaml
jobs:
  create-pd-entries:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      - name: Create String Parameters
        uses: ./.github/actions/create-pid-entry
        with:
          bearer-token: ${{ secrets.BEARER_TOKEN }}
          btp-api-url: ${{ vars.BTP_API_URL }}
          type: 'StringParameters'
          parameter-json: './partner-data/StringParameters.json'
```

---

## 🪵 Example Logs

```
=========================================
🚀 Creating Partner Directory: StringParameters
=========================================
📄 Reading JSON from file: ./partner-data/StringParameters.json
📊 Processing 3 entries for StringParameters
-----------------------------------------
✅ Entry 1/3 created successfully
✅ Entry 2/3 created successfully
✅ Entry 3/3 created successfully
```
_These are example logs you may encounter when running this action. Actual logs may vary depending on configuration and runtime conditions._

---

## 📂 Outputs

This action does not produce any outputs. It creates entries in the Partner Directory and exits with an error if creation fails.

---

## 💡 Tips & Troubleshooting

- The action accepts either a file path or direct JSON content via the `parameter-json` input.
- JSON can be a single object or an array of objects.
- Each entity type has specific required fields that are validated before creation:
  - **AlternativePartners**: Agency, Scheme, Id, Pid
  - **AuthorizedUsers**: User, Pid
  - **StringParameters**: Pid, Id, Value
  - **BinaryParameters**: Pid, Id, ContentType, Value
- Ensure the bearer token has write permissions to the Partner Directory API.

---

## 📚 References

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/CLOUD_INTEGRATION)
