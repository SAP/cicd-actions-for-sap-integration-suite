# 🔍 Resolve IFlow Deploy Task GitHub Action

Read `Deployment_INTEGRATION_FLOW.json` for a single iFlow and produce a deploytasks JSON file ready for `deploy-package-artifacts`.

---

## ✨ Overview

This action resolves whether a specific iFlow should be deployed in a target environment and generates the corresponding deploytask file. It reads the package's `Configuration/Deployment_INTEGRATION_FLOW.json` from the consumer repo checkout, applies the same **3-level environment priority chain** used by `add-iflows-for-deployment`, and outputs a deploytasks JSON consumable by `deploy-package-artifacts`.

The action locates the package directory automatically by scanning for a folder matching `*~${PACKAGE_ID}` — no API call for the package name is required.

Both JSON formats are supported:
- **New format**: `Environments` block with per-env overrides (`Environments.TST.Deploy`)
- **Legacy flat format**: top-level env keys (e.g., `"TST": "true"`)

---

## ⚙️ Inputs

| Name         | Required | Description                                              |
|--------------|----------|----------------------------------------------------------|
| `package-id`  | ✅ Yes   | Package ID (used to locate the `PackageName~PackageID` folder). |
| `iflow-id`    | ✅ Yes   | Artifact ID of the iFlow to resolve.                     |
| `target-env`  | ✅ Yes   | Target environment (e.g., `DEV`, `TST`, `PRD`).         |

---

## 📤 Outputs

| Name            | Description                                                          |
|-----------------|----------------------------------------------------------------------|
| `file`          | Absolute path to the generated deploytasks JSON file.               |
| `should-deploy` | `"true"` if the iFlow is marked for deployment in `target-env`, `"false"` otherwise. |

---

## 📂 Output File Structure

When `should-deploy` is `"true"`, the file contains a single deploytask entry:

```json
{
  "d": {
    "deploytasks": [
      {
        "id": "my-iflow-001",
        "type": "Integration",
        "loglevel": "ERROR",
        "runtimes": "iflmap"
      }
    ]
  }
}
```

When `should-deploy` is `"false"`, the file contains an empty `deploytasks` array (passed to `deploy-package-artifacts`, which exits gracefully with no-op).

---

## 📝 Usage Example

```yaml
steps:
  - name: Checkout consumer repo
    uses: actions/checkout@v4
    with:
      path: btp-insuite

  - name: Checkout cicd-actions repo
    uses: actions/checkout@v4
    with:
      repository: ${{ vars.GIT_CICD_ORGREPO }}
      ref: ${{ vars.GIT_CICD_REF }}
      path: cicd-btp-insuite
      token: ${{ steps.cicd-token.outputs.token }}

  - name: Resolve IFlow Deploy Task
    id: deployment-file
    uses: ./cicd-btp-insuite/.github/actions/resolve-iflow-deploy-task
    with:
      package-id: ${{ steps.get-packageid.outputs.packageID }}
      iflow-id: my-iflow-001
      target-env: TST

  - name: Deploy Package Artifacts
    uses: ./cicd-btp-insuite/.github/actions/deploy-package-artifacts
    with:
      bearer-token: ${{ steps.get-token.outputs.token }}
      btp-api-url: ${{ inputs.btp-api-url }}
      file: ${{ steps.deployment-file.outputs.file }}
      action: Deploy
      enable-set-log-level: "true"
```

---

## 💡 Tips & Troubleshooting

- **Deploy decision priority chain** — three levels, highest first:
  1. `Environments[$TARGET_ENV].Deploy` — new format per-env override
  2. `$TARGET_ENV` flat key — legacy format (e.g., `"TST": "true"`)
  3. `Deploy` — global default fallback

- **LogLevel & Runtimes** use the same priority chain:
  - `Environments[$TARGET_ENV].LogLevel` → top-level `LogLevel` → `"INFO"`
  - `Environments[$TARGET_ENV].Runtimes` → top-level `Runtimes` → `"iflmap"`

- **Deployment_INTEGRATION_FLOW.json example** (legacy flat format):
  ```json
  {
    "PackageIntegrationFlowDeployments": {
      "PackageName": "My_Package",
      "PackageID": "MYPKG001",
      "IntegrationFlows": [
        {
          "ArtifactID": "my-iflow-001",
          "ArtifactName": "My Integration Flow",
          "Deploy": "false",
          "DEV": "false",
          "TST": "true",
          "PRD": "true",
          "Rank": "1",
          "LogLevel": "ERROR"
        }
      ]
    }
  }
  ```
  Running with `target-env=TST` resolves to `should-deploy=true` and `loglevel=ERROR`.

- **Deployment_INTEGRATION_FLOW.json example** (new Environments format):
  ```json
  {
    "ArtifactID": "my-iflow-001",
    "Deploy": "false",
    "LogLevel": "INFO",
    "Runtimes": "iflmap",
    "Environments": {
      "TST": { "Deploy": "true", "LogLevel": "ERROR" },
      "PRD": { "Deploy": "true" }
    }
  }
  ```

- **Working directory**: The action runs in `btp-insuite/IntegrationPackages`. The consumer repo must be checked out at `btp-insuite/` before calling this action.

- **Package directory lookup**: The action scans for a directory matching `*~${PACKAGE_ID}`. If multiple matches are found, the action fails. This avoids requiring the package name as an input.

- **Environment names are case-sensitive**: Use uppercase values (`DEV`, `TST`, `PRD`) matching the keys in your JSON file.

- **Relation to `add-iflows-for-deployment`**: This action covers the single-iFlow case (resolves one specific iFlow by ID). `add-iflows-for-deployment` processes all iFlows in a package for bulk deployment. Both apply the same priority chain.

---

## 📄 License

This project is licensed under the Apache License 2.0.
