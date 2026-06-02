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
| eic-location     | ❌        | Edge Integration Cell runtime identifier (e.g., 'eicruntime01'). When provided, entries are created in the specified EIC instead of Cloud Integration. |
| eic-url-template | ❌        | URL path template for EIC API access. Contains `{runtime}` as placeholder for the runtime identifier. **Not published — subject to change.** Required when `eic-location` is set. |

---

## 📝 Usage Example

### Standard (Cloud Integration)
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

### Edge Integration Cell
```yaml
jobs:
  create-pd-entries-eic:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      - name: Create String Parameters in EIC
        uses: ./.github/actions/create-pid-entry
        with:
          bearer-token: ${{ secrets.BEARER_TOKEN }}
          btp-api-url: ${{ vars.BTP_API_URL }}
          type: 'StringParameters'
          parameter-json: './partner-data/StringParameters.json'
          eic-location: 'eicruntime01'
          eic-url-template: ${{ vars.BTP_EIC_URL_TEMPLATE }}
```

---

## 🪵 Example Logs

### Cloud Integration
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

### Edge Integration Cell
```
=========================================
🚀 Creating Partner Directory: StringParameters (EIC: eicruntime01)
=========================================
📍 Target: Edge Integration Cell (eicruntime01)
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

### Edge Integration Cell (EIC) Support
- When `eic-location` is provided, entries are created using the EIC API endpoint, constructed from the `eic-url-template` and the `eic-location` value.
- The EIC API path is not yet published — subject to change. Configure `BTP_EIC_URL_TEMPLATE` in your GitHub environment.
- The same bearer token is used for both Cloud Integration and EIC APIs.
- EIC runtimes must be properly connected to your Cloud Integration tenant.

---

## 📚 References

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/CLOUD_INTEGRATION)