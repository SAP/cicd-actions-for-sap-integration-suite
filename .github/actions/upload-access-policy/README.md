# 📤 Upload Access Policy GitHub Action

Upload an access policy from Git to SAP BTP Integration Suite.

---

## ✨ Overview

This action reads an Access Policy and its Artifact References from the Git repository and syncs them to SAP BTP Integration Suite. If the policy already exists it is updated via PUT; if it does not exist it is created via POST. All existing Artifact References are deleted and recreated from Git to ensure a clean sync.

**Expected Git file structure:**
```
btp-insuite/AccessPolicies/<access-policy-name>/
├── AccessPolicy.json
└── ArtifactReferences.json
```

---

## ⚙️ Inputs

| Name | Required | Description |
|------|----------|-------------|
| `bearer-token` | ✅ Yes | Bearer token with authorization to manage Access Policies in Integration Suite. |
| `btp-api-url` | ✅ Yes | Base URL for the BTP Integration Suite API (e.g., `https://my-tenant.it-cpi01.cfapps.eu10.hana.ondemand.com`). |
| `access-policy-name` | ✅ Yes | The `RoleName` of the Access Policy to upload. Must match the folder name and `RoleName` in `AccessPolicy.json`. |

---

## 📂 Outputs

| Name | Description |
|------|-------------|
| `policy-id` | The BTP-internal numeric ID of the created or updated Access Policy. |

---

## 📝 Usage Example

```yaml
- name: Upload Access Policy
  uses: ./.github/actions/upload-access-policy
  with:
    bearer-token: ${{ steps.get-token.outputs.token }}
    btp-api-url: ${{ vars.BTP_API_URL }}
    access-policy-name: MyAccessPolicy
```

---

## 📄 File Format

### AccessPolicy.json
```json
{
  "RoleName": "MyAccessPolicy",
  "Description": "My access policy description"
}
```

### ArtifactReferences.json
```json
{
  "d": {
    "results": [
      {
        "Name": "MyIFlow",
        "Description": "",
        "Type": "INTEGRATION_FLOW",
        "ConditionAttribute": "Name",
        "ConditionValue": "MyIFlow",
        "ConditionType": "exactString"
      }
    ]
  }
}
```

---

## 💡 Tips & Troubleshooting

- **ArtifactReferences.json missing**: If the file is not present the action skips syncing references without error.
- **Empty results**: If `ArtifactReferences.json` contains an empty `results` array, all existing references are deleted and no new ones are created.
- **Bearer Token Format**: Ensure the token includes the `Bearer` prefix.
- **API URL Format**: Use the complete base URL without trailing slashes.

---

## 📄 License

This project is licensed under the Apache License 2.0.
