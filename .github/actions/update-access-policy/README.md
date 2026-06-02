# 🔄 Update Access Policy from GIT (Upload / Delete) GitHub Action

Composite action to upload or delete an access policy in SAP BTP Integration Suite from Git.

---

## ✨ Overview

This composite action orchestrates the full update cycle for an Access Policy:

- **Upload**: Checks out the source repository, requests an OAuth token, deletes the existing policy on BTP (if present), then uploads the policy and its Artifact References from Git.
- **Delete**: Checks out the source repository, requests an OAuth token, deletes the policy on BTP (if present).

The delete-before-upload pattern ensures a clean state and is consistent with how Integration Packages are handled.

---

## ⚙️ Inputs

| Name | Required | Description |
|------|----------|-------------|
| `source-ref` | ✅ Yes | Git reference (branch/tag) containing the Access Policy files. |
| `access-policy-name` | ✅ Yes | The `RoleName` of the Access Policy. |
| `case` | ✅ Yes | Operation to perform: `Upload` or `Delete`. |
| `btp-api-user` | ✅ Yes | BTP Service Key (ClientID) for OAuth token. |
| `btp-tec-user` | ✅ Yes | BTP technical user with Integration Suite access. |
| `btp-token-url` | ✅ Yes | BTP OAuth token endpoint URL. |
| `btp-api-url` | ✅ Yes | Base URL for the BTP Integration Suite API. |
| `BTP_API_PASSWORD` | ✅ Yes | Client Secret for the API user. |
| `BTP_TEC_PASSWORD` | ✅ Yes | Password for the technical user. |

---

## 📝 Usage Example

```yaml
- name: Upload Access Policy
  uses: ./.github/actions/update-access-policy
  with:
    source-ref: development
    access-policy-name: MyAccessPolicy
    case: Upload
    btp-api-user: ${{ vars.BTP_API_USER }}
    btp-tec-user: ${{ vars.BTP_TEC_USER }}
    btp-token-url: ${{ vars.BTP_TOKEN_URL }}
    btp-api-url: ${{ vars.BTP_API_URL }}
    BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
    BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}
```

---

## 📂 Outputs

This action has no outputs.

---

## 📄 License

This project is licensed under the Apache License 2.0.
