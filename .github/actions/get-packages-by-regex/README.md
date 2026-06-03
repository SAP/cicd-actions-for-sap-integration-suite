# Get Packages by Regex

Fetches all Integration Packages from BTP Integration Suite and filters them by a regex pattern applied to the Package ID.

## Usage

```yaml
- uses: ./cicd-actions/.github/actions/get-packages-by-regex
  with:
    bearer-token: ${{ steps.get-token.outputs.token }}
    btp-api-url: ${{ vars.BTP_API_URL }}
    package-regex: "^MyPrefix_.*"
```

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `bearer-token` | ✅ | — | Bearer token to access Integration Suite APIs |
| `btp-api-url` | ✅ | — | BTP Integration Suite API base URL |
| `package-regex` | ❌ | `.*` | Regex pattern to filter Package IDs |

## Outputs

| Output | Description |
|--------|-------------|
| `packages` | JSON array of matching packages: `[{Id, Name}]` |
| `count` | Number of matching packages |

## How it Works

1. Calls the BTP `IntegrationPackages` OData API to fetch all packages
2. Applies the `package-regex` filter on each Package ID using `jq`'s `test()` function
3. Returns only the matching packages with their ID and Name

## Example

With `package-regex` set to `^SAP_` and the following packages on BTP:

| Package ID | Package Name |
|-----------|-------------|
| `SAP_OrderMgmt` | SAP Order Management |
| `SAP_InvoiceMgmt` | SAP Invoice Management |
| `Custom_Analytics` | Custom Analytics |

The output `packages` will be:

```json
[
  {"Id": "SAP_OrderMgmt", "Name": "SAP Order Management"},
  {"Id": "SAP_InvoiceMgmt", "Name": "SAP Invoice Management"}
]