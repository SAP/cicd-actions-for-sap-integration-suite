# 🌿 Recreate Branch GitHub Action

Creates (or re-creates) a branch from a specified source reference. Skips if the branch already exists.

---

## ✨ Overview

This action creates a new branch pointing to the same commit as a given source reference (branch, tag, or commit SHA). It is typically used after a release merge to re-create the development branch from main. If the branch already exists (restart scenario), the action skips creation and reports the existing branch.

---

## ⚙️ Inputs

| Name         | Required | Description                                                        |
|--------------|----------|--------------------------------------------------------------------|
| branch-name  | ✅ Yes   | Name of the branch to create.                                     |
| source-ref   | ✅ Yes   | Source reference (branch, tag, or SHA) to create the branch from.  |
| github-token | ✅ Yes   | GitHub token with `contents:write` permission.                     |

---

## 📝 Usage Example

```yaml
jobs:
  recreate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Recreate development branch from main
        id: recreate
        uses: ./.github/actions/recreate-branch
        with:
          branch-name: development
          source-ref: main
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Show result
        run: |
          echo "Status: ${{ steps.recreate.outputs.status }}"
          echo "SHA: ${{ steps.recreate.outputs.sha }}"
```

---

## 📂 Outputs

| Name   | Description                                                          |
|--------|----------------------------------------------------------------------|
| status | Status of the operation: `created`, `already-exists`, or `error`     |
| sha    | The SHA of the branch head                                           |

---

## 💡 Tips & Troubleshooting

- **Source Resolution**: The action resolves the source reference in order: branch → tag → commit SHA. It fails with a clear error if none match.
- **Restart Safety**: If the branch already exists, the action reports `already-exists` and returns the existing SHA without making changes.
- **Generic Action**: While designed for the release workflow, this action can be used anywhere a branch needs to be created from a reference.
- **GitHub Enterprise Support**: The action auto-detects the GitHub server hostname and works with GitHub Enterprise instances.

---

## 📄 License

This project is licensed under the Apache License 2.0.