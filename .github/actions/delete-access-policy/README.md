# 🗑️ Delete Access Policy GitHub Action

Delete an access policy from SAP BTP Integration Suite via API call.

---

## ✨ Overview

This action removes an access policy directly from SAP BTP Integration Suite using the REST API. It looks up the policy by its `RoleName`, then sends a DELETE request to the API. The action accepts both successful deletion (HTTP 200/204) and already-deleted scenarios (HTTP 404) as valid outcomes, making it idempotent and safe for repeated execution. All artifact references are automatically removed by BTP when the policy is deleted.

---

## ⚙️ Inputs

| Name | Required | Description |
|------|----------|-------------|
| `bearer-token` | ✅ Yes | Bearer token with authorization to manage Access Policies in Integration Suite. |
| `btp-api-url` | ✅ Yes | Base URL for the BTP Integration Suite API (e.g., `https://my-tenant.it-cpi01.cfapps.eu10.hana.ondemand.com`). |
| `access-policy-name` | ✅ Yes | The `RoleName` of the Access Policy to delete. |

---

## 📝 Usage Example

```yaml
- name: Delete Access Policy
  uses: ./.github/actions/delete-access-policy
  with:
    bearer-token: ${{ steps.get-token.outputs.token }}
    btp-api-url: ${{ vars.BTP_API_URL }}
    access-policy-name: MyAccessPolicy
```

---

## 📂 Outputs

This action has no outputs. It performs a DELETE API operation and returns only exit status (success or failure).

**Side Effects:**
- Sends a DELETE request to the BTP Integration Suite API
- Removes the Access Policy and all its Artifact References from BTP (if it exists)
- No local file system changes

---

## 💡 Tips & Troubleshooting

- **Not Found**: If the Access Policy does not exist on BTP, the action exits successfully — nothing to delete.
- **Cascade Delete**: BTP automatically deletes all Artifact References when an Access Policy is deleted. No separate cleanup needed.
- **Bearer Token Format**: Ensure the token includes the `Bearer` prefix.
- **API URL Format**: Use the complete base URL without trailing slashes.

---

## 📄 License

This project is licensed under the Apache License 2.0.
