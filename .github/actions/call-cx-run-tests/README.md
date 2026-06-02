# 📞 Call Customer Exit - Run Tests

Calls the `cx-run-tests` customer exit action to execute tests for integration packages.

---

## ✨ Overview

This action is the **exit-specific caller** for the test execution customer exit. It:

1. Checks out the intsuite (current) repository and optionally the extension repository
2. Uses the generic `resolve-customer-exit` orchestrator to determine if the exit is active and where the implementation is located
3. Conditionally invokes the `cx-run-tests` action from the resolved repository (intsuite or extension)
4. Returns the `test-results` output for use by downstream steps

This action is designed to be called from workflows that process integration packages and need to execute custom tests as part of the pipeline.

---

## ⚙️ Inputs

| Name                | Required | Default | Description                                                          |
|---------------------|----------|---------|----------------------------------------------------------------------|
| cx-active           | ✅ Yes   | `false` | Whether the customer exit is active (`true`/`false`)                 |
| intsuite-repo-path  | ✅ Yes   |         | Path where the integration suite repository is checked out           |
| extension-repo-path | ✅ Yes   |         | Path where the extension repository is checked out                   |
| cx-repository       | ✅ Yes   |         | Repository containing the customer exit implementation (`org/repo`)  |
| cx-repository-ref   | ❌ No    | `main`  | Branch, tag, or commit to checkout of the customer exit repository   |
| package-id          | ✅ Yes   |         | ID of the package to run tests for                                   |
| btp-api-url         | ✅ Yes   |         | URL of the BTP API                                                   |
| bearer-token        | ✅ Yes   |         | Bearer token for authenticating against the BTP API                  |
| target-ref          | ❌ No    | `''`    | GIT Target Reference for checkout                                    |
| git-cicd-token      | ✅ Yes   |         | GitHub token for checking out private repositories                   |
| mode                | ❌ No    | `''`    | Mode of the package (e.g. `PartnerDirectory` or `IntegrationPackages`) |

---

## 📂 Outputs

| Name         | Description                                      |
|--------------|--------------------------------------------------|
| test-results | Results of the executed tests from the customer exit implementation |

Returns an empty string if:
- The customer exit is not active
- The customer exit implementation was not found
- The implementation returned no test results

---

## 📝 Usage Example

```yaml
jobs:
  run-tests:
    runs-on: ubuntu-latest
    outputs:
      test-results: ${{ steps.call-exit.outputs.test-results }}
    steps:
      - name: Checkout cicd-actions repo
        uses: actions/checkout@v4
        with:
          repository: my-org/cicd-actions
          ref: v1
          path: cicd-btp-insuite
          token: ${{ secrets.GIT_CICD_TOKEN }}

      - name: Call Customer Exit - Run Tests
        id: call-exit
        uses: ./cicd-btp-insuite/.github/actions/call-cx-run-tests
        with:
          cx-active: ${{ vars.CX_RUN_TESTS }}
          intsuite-repo-path: intsuite-repo
          extension-repo-path: cx-extension-repo
          cx-repository: ${{ vars.CX_REPOSITORY }}
          cx-repository-ref: ${{ vars.CX_REPOSITORY_REF || 'main' }}
          git-cicd-token: ${{ secrets.GIT_CICD_TOKEN }}
          package-id: MyIntegrationPackage
          btp-api-url: ${{ vars.BTP_API_URL }}
          bearer-token: ${{ steps.get-token.outputs.bearer-token }}
```

---

## 🔄 Internal Flow

```
┌──────────────────────────────────────────┐
│  call-cx-run-tests                       │
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
│  5. Return test-results                  │
└──────────────────────────────────────────┘
```

---

## 💡 Tips & Troubleshooting

- **Prerequisites**: The cicd-actions repository must be checked out at `cicd-btp-insuite` before calling this action, since the action and the `resolve-customer-exit` orchestrator live in that repository.
- **Extension Repository**: Set `cx-repository` to the `org/repo` of your extension repository. If left empty, the extension checkout is skipped.
- **Checkout Paths**: The `intsuite-repo-path` and `extension-repo-path` control where the repositories are checked out. These must match the hardcoded paths used by the `uses:` directives (`intsuite-repo` and `cx-extension-repo`).
- **Empty Result**: An empty `test-results` output means no test results were returned — this does not necessarily indicate failure.
- **Resolution Priority**: The intsuite repository always takes precedence. If `cx-run-tests` exists in both repos, only the intsuite version is executed.

---

## 📄 License

This project is licensed under the Apache License 2.0.