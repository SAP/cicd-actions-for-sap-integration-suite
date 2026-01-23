# 🚀 Get Parameter from Partner Directory GitHub Action

Retrieves parameters from the BTP Partner Directory for a specific Partner ID.

---

## ✨ Overview

This action fetches parameters from the BTP Partner Directory API for a given Partner ID and parameter type. It supports retrieving StringParameters, AuthorizedUsers, AlternativePartners, and BinaryParameters, and saves the results to a temporary file.

---

## ⚙️ Inputs

| Name           | Required | Description                                                                                      |
|----------------|----------|--------------------------------------------------------------------------------------------------|
| bearer-token   | ✅        | BEARER Token to access Partner Directory                                                        |
| btp-api-url    | ✅        | URL on BTP to access APIs                                                                        |
| partner-id     | ✅        | Partner ID                                                                                       |
| parameter-type | ✅        | Partner Type (StringParameters, AuthorizedUsers, AlternativePartners, BinaryParameters)         |

---

## 📝 Usage Example

```yaml
jobs:
  get-parameters:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      - name: Get String Parameters
        id: get-params
        uses: ./.github/actions/get-parameter-pd
        with:
          bearer-token: ${{ secrets.BEARER_TOKEN }}
          btp-api-url: ${{ vars.BTP_API_URL }}
          partner-id: 'PARTNER123'
          parameter-type: 'StringParameters'
      - name: Display output file
        run: echo "Parameters saved to ${{ steps.get-params.outputs.file }}"
```

---

## 🪵 Example Logs

```
Get StringParameters for Partner ID PARTNER123 from https://api.btp.example.com/api/v1/StringParameters?$filter=Pid%20eq%20'PARTNER123'
Writing StringParameters Parameters of Partner ID PARTNER123 to file /tmp/tmp.abc123xyz
```
_These are example logs you may encounter when running this action. Actual logs may vary depending on configuration and runtime conditions._

---

## 📂 Outputs

| Name | Description                              |
|------|------------------------------------------|
| file | File path containing the list of parameters |

---

## 💡 Tips & Troubleshooting

- The action retrieves parameters filtered by Partner ID from the BTP Partner Directory API.
- Valid parameter types are: StringParameters, AuthorizedUsers, AlternativePartners, BinaryParameters.
- The output is written to a temporary file whose path is returned in the `file` output.
- HTTP status code must be 200 for successful retrieval.
- Ensure the bearer token has read permissions to the Partner Directory API.
- The response is in JSON format containing the Partner Directory data structure.

---

## 📚 References

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/CLOUD_INTEGRATION)
