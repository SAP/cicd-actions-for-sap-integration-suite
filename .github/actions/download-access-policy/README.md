# 📥 Download Access Policy GitHub Action

Download an access policy from SAP BTP Integration Suite to Git.

---

## ✨ Overview

This action fetches an Access Policy and its Artifact References from SAP BTP Integration Suite and saves them to the Git repository. OData metadata fields are stripped before saving to keep the files clean and diff-friendly.

**Created Git file structure:**
```
btp-insuite/AccessPolicies/<access-policy-name>/
├── AccessPolicy.json
└── ArtifactReferences.json
```

---

## ⚙️ Inputs

| Name | Required | Description |
|------|----------|-------------|
| `bearer-token` | ✅ Yes | Bearer token with authorization to read Access Policies from Integration Suite. |
| `btp-api-url` | ✅ Yes | Base URL for the BTP Integration Suite API (e.g., `https://my-tenant.it-cpi01.cfapps.eu10.hana.ondemand.com`). |
| `access-policy-name` | ✅ Yes | The `RoleName` of the Access Policy to download. |

---

## 📂 Outputs

This action produces no outputs. All data is written directly to the Git working directory.

---

## 📝 Usage Example

```yaml
- name: Download Access Policy
  id: get-access-policy
  uses: ./.github/actions/download-access-policy
  with:
    bearer-token: ${{ steps.get-token.outputs.token }}
    btp-api-url: ${{ vars.BTP_API_URL }}
    access-policy-name: MyAccessPolicy
```

---

## 💡 Tips & Troubleshooting

- **Policy Not Found**: If the Access Policy does not exist on BTP the action exits with an error.
- **Existing Files**: If files already exist in Git a diff is printed before overwriting.
- **Metadata Stripped**: `__metadata`, `Id`, `ArtifactReferences` (inline), `AccessPolicyRuntimeAssignments` and `AccessPolicy` (on references) are removed from saved files. `Id` is excluded on both the policy and each artifact reference — both are environment-specific dynamic values that differ across tenants.

---

## 🔑 Why `Id` is not stored in Git

The `Id` field returned by the BTP API (e.g. `"Id": "1901"`) is an **environment-specific internal identifier**. The same Access Policy will have a different `Id` in DEV, TST, and PRD. Storing it in Git would cause confusion and could lead to accidental cross-environment operations.

**`RoleName` is the stable, portable identifier** — it is unique per tenant and is what all other actions (`upload-access-policy`, `delete-access-policy`) use to locate a policy at runtime.

### Fetching Artifact References without a stored Id

This action fetches Artifact References within the same run by resolving the `Id` in-memory (API response → step output → next step). The `Id` is never written to disk.

If you need the `Id` independently (e.g. in a custom action that re-fetches artifact references), resolve it at runtime by filtering on `RoleName`:

```
GET /api/v1/AccessPolicies?$filter=RoleName eq '<policy-name>'&$format=json
```

The response contains the current environment-specific `Id`, which you can then use to call:

```
GET /api/v1/AccessPolicies(<Id>L)/ArtifactReferences?$format=json
```

This is the same pattern used by `upload-access-policy` and `delete-access-policy`.

---

## 📄 License

This project is licensed under the Apache License 2.0.
