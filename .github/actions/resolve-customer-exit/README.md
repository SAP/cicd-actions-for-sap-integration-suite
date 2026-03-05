# 🔍 Resolve Customer Exit GitHub Action

Generic orchestrator that checks if a customer exit is active and resolves its implementation location across repositories.

---

## ✨ Overview

This action serves as the **generic resolution layer** of the customer exit framework. It determines whether a given customer exit is active and locates the exit's action implementation by searching repositories in a defined priority order:

1. **Intsuite repository** (current content repository) — takes precedence
2. **Extension repository** (remote repository) — fallback

The action does **not** execute the customer exit itself; it only resolves the location. Exit-specific caller actions (e.g., `call-cx-derive-iflow-exclusions`) use this action to determine where to find the implementation before invoking it.

---

## ⚙️ Inputs

| Name                 | Required | Default | Description                                                                 |
|----------------------|----------|---------|-----------------------------------------------------------------------------|
| cx-active            | ✅ Yes   | `false` | Whether the customer exit is active (`true`/`false`)                        |
| exit-action-name     | ✅ Yes   | —       | The action directory name to look for (e.g., `cx-derive-iflow-exclusions`)  |
| intsuite-repo-path   | ✅ Yes   | —       | Path to the checked-out intsuite (current) repository                       |
| extension-repo-path  | ❌ No    | `''`    | Path to the checked-out extension repository (may not exist if not configured) |

---

## 📂 Outputs

| Name   | Description                                                                  |
|--------|------------------------------------------------------------------------------|
| active | Boolean string (`true` or `false`) indicating if the customer exit is active |
| source | Where the action was found: `intsuite`, `extension`, or `none`               |

---

## 📝 Usage Example

```yaml
steps:
  - name: Resolve customer exit location
    id: resolve
    uses: ./.github/actions/resolve-customer-exit
    with:
      cx-active: ${{ vars.CX_IFLOW_EXCLUSIONS }}
      exit-action-name: cx-derive-iflow-exclusions
      intsuite-repo-path: intsuite-repo
      extension-repo-path: cx-extension-repo

  - name: Use resolution result
    run: |
      echo "Active: ${{ steps.resolve.outputs.active }}"
      echo "Source: ${{ steps.resolve.outputs.source }}"
```

**Using Outputs for Conditional Execution:**
```yaml
steps:
  - name: Resolve exit
    id: resolve
    uses: ./.github/actions/resolve-customer-exit
    with:
      cx-active: 'true'
      exit-action-name: cx-derive-iflow-exclusions
      intsuite-repo-path: intsuite-repo
      extension-repo-path: cx-extension-repo

  - name: Call from intsuite repo
    if: ${{ steps.resolve.outputs.source == 'intsuite' }}
    uses: ./intsuite-repo/.github/actions/cx-derive-iflow-exclusions

  - name: Call from extension repo
    if: ${{ steps.resolve.outputs.source == 'extension' }}
    uses: ./cx-extension-repo/.github/actions/cx-derive-iflow-exclusions
```

---

## 🔎 Resolution Logic

The action searches for the customer exit implementation at:

```
<repo-path>/.github/actions/<exit-action-name>/action.yml
```

| Priority | Repository         | Path Checked                                                        |
|----------|--------------------|---------------------------------------------------------------------|
| 1️⃣       | Intsuite (current) | `<intsuite-repo-path>/.github/actions/<exit-action-name>/action.yml` |
| 2️⃣       | Extension (remote) | `<extension-repo-path>/.github/actions/<exit-action-name>/action.yml` |

> **Note:** The intsuite repository always takes precedence. If the action exists in both repositories, only the intsuite location is returned.

---

## 💡 Tips & Troubleshooting

- **Extensible Design**: This action is generic and supports any customer exit. Simply pass a different `exit-action-name` to resolve different exits.
- **Inactive Exit**: When `cx-active` is not `true`, the action immediately returns `active=false` and `source=none` without checking any paths.
- **Missing Implementation**: If the exit is active but the action file is not found in either repository, the action returns `active=true` and `source=none` with a warning message.
- **Logging**: The action provides formatted console output showing which paths were checked and where the action was found.

---

## 📄 License

This project is licensed under the Apache License 2.0.