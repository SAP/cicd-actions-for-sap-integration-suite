# 📞 Call Customer Exit - Derive IFlow Exclusions

Calls the `cx-derive-iflow-exclusions` customer exit action to derive a list of IFlow IDs to exclude from deployment.

---

## ✨ Overview

This action is the **exit-specific caller** for the IFlow exclusions customer exit. It:

1. Checks out the intsuite (current) repository and optionally the extension repository
2. Uses the generic `resolve-customer-exit` orchestrator to determine if the exit is active and where the implementation is located
3. Conditionally invokes the `cx-derive-iflow-exclusions` action from the resolved repository (intsuite or extension)
4. Returns the `exclude-iflow-ids` output for use by downstream deployment steps

This action is designed to be called from the `btp-release-import` workflow, between the change analysis and deployment execution steps.

---

## ⚙️ Inputs

| Name                 | Required | Default              | Description                                                      |
|----------------------|----------|----------------------|------------------------------------------------------------------|
| cx-active            | ✅ Yes   | `false`              | Whether the customer exit is active (`true`/`false`)             |
| intsuite-repo-path   | ✅ Yes   | `intsuite-repo`      | Path to check out the intsuite (current) repository into         |
| extension-repo-path  | ❌ No    | `cx-extension-repo`  | Path to check out the extension repository into                  |
| cx-repository        | ❌ No    | `''`                 | Remote extension repository (`org/repo`). Leave empty if not configured. |
| cx-repository-ref    | ❌ No    | `main`               | Git ref for the extension repository                             |
| git-cicd-token       | ✅ Yes   |                      | GitHub token for checking out private repositories               |
| btp-tec-password     | ❌ No    | `''`                 | BTP technical user password                                      |
| btp-api-password     | ❌ No    | `''`                 | BTP API password (Service Key client secret)                     |
| target-env           | ❌ No    | `''`                 | Target BTP Environment (DEV/TST/PRD)                             |
| base-ref             | ❌ No    | `''`                 | GIT Base Reference                                               |
| target-ref           | ❌ No    | `''`                 | GIT Target Reference                                             |
| perform-deploy       | ❌ No    | `''`                 | Whether deployment is being performed (`true`/`false`)           |
| btp-api-user         | ❌ No    | `''`                 | BTP Service Key (ClientID) to access Token Endpoint              |
| btp-tec-user         | ❌ No    | `''`                 | BTP technical user with Access Policy for Integration Suite      |
| btp-token-url        | ❌ No    | `''`                 | URL on BTP to request Token                                      |
| btp-api-url          | ❌ No    | `''`                 | URL on BTP to access APIs                                        |
| git-cicd-orgrepo     | ❌ No    | `''`                 | Remote GIT Org/Repo for CICD                                     |

All optional inputs are passed through to the customer exit implementation, providing full context about the current workflow execution.

---

## 📂 Outputs

| Name              | Description                                              |
|-------------------|----------------------------------------------------------|
| exclude-iflow-ids | Comma-separated list of IFlow IDs to exclude from deployment (e.g., `IFlow_A,IFlow_B`) |

Returns an empty string if:
- The customer exit is not active
- The customer exit implementation was not found
- The implementation returned no exclusions

---

## 📝 Usage Example

```yaml
jobs:
  customer-exit-iflow-exclusions:
    runs-on: ubuntu-latest
    outputs:
      exclude-iflow-ids: ${{ steps.call-exit.outputs.exclude-iflow-ids }}
    steps:
      - name: Checkout cicd-actions repo
        uses: actions/checkout@v4
        with:
          repository: my-org/cicd-actions
          ref: v1
          path: cicd-btp-insuite
          token: ${{ secrets.GIT_CICD_TOKEN }}

      - name: Call Customer Exit
        id: call-exit
        uses: ./cicd-btp-insuite/.github/actions/call-cx-derive-iflow-exclusions
        with:
          cx-active: ${{ vars.CX_IFLOW_EXCLUSIONS }}
          intsuite-repo-path: intsuite-repo
          extension-repo-path: cx-extension-repo
          cx-repository: ${{ vars.CX_REPOSITORY }}
          cx-repository-ref: ${{ vars.CX_REPOSITORY_REF || 'main' }}
          git-cicd-token: ${{ secrets.GIT_CICD_TOKEN }}
          btp-tec-password: ${{ secrets.BTP_TEC_PASSWORD }}
          btp-api-password: ${{ secrets.BTP_API_PASSWORD }}
          target-env: PRD
          target-ref: main

  deployment:
    needs: customer-exit-iflow-exclusions
    steps:
      - name: Deploy with exclusions
        run: echo "Excluding: ${{ needs.customer-exit-iflow-exclusions.outputs.exclude-iflow-ids }}"
```

---

## 🔄 Internal Flow

```
┌──────────────────────────────────────────┐
│  call-cx-derive-iflow-exclusions         │
│                                          │
│  1. Checkout intsuite repository         │
│  2. Checkout extension repository        │
│     (if cx-repository is set)            │
│                                          │
│  3. resolve-customer-exit                │
│     ├─ cx-active? ──► no ──► return ""   │
│     └─ yes                               │
│        ├─ intsuite? ──► source=intsuite  │
│        └─ extension? ──► source=extension│
│                                          │
│  4. Call action from resolved source     │
│     ├─ intsuite ──► ./intsuite-repo/...  │
│     └─ extension ──► ./cx-extension-repo/│
│                                          │
│  5. Return exclude-iflow-ids             │
└──────────────────────────────────────────┘
```

---

## 💡 Tips & Troubleshooting

- **Prerequisites**: The cicd-actions repository must be checked out before calling this action (since the action itself lives in that repository). The intsuite and extension repository checkouts are handled automatically by the action.
- **Extension Repository**: Set `cx-repository` to the `org/repo` of your extension repository. If left empty, the extension checkout is skipped.
- **Checkout Paths**: The `intsuite-repo-path` and `extension-repo-path` control where the repositories are checked out. The defaults (`intsuite-repo` and `cx-extension-repo`) match the paths used by the resolve and exit steps.
- **Empty Result**: An empty `exclude-iflow-ids` output means no IFlows are excluded — deployment proceeds with all IFlows.
- **Logging**: The action logs which source was resolved and what the customer exit returned for easy debugging.

---

## 📄 License

This project is licensed under the Apache License 2.0.