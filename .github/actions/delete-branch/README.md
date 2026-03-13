# 🗑️ Delete Branch GitHub Action

Deletes a branch if it exists. Skips silently if the branch does not exist.

---

## ✨ Overview

This action deletes a specified branch from the repository via the GitHub API. If the branch does not exist (e.g., already cleaned up from a previous run), the action completes successfully without error. This makes it safe to use in restart scenarios.

---

## ⚙️ Inputs

| Name         | Required | Description                                            |
|--------------|----------|--------------------------------------------------------|
| branch-name  | ✅ Yes   | Name of the branch to delete.                         |
| github-token | ✅ Yes   | GitHub token with `contents:write` permission.         |

---

## 📝 Usage Example

```yaml
jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Delete temporary branch
        id: delete
        uses: ./.github/actions/delete-branch
        with:
          branch-name: tmp/release-v1.0.0
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Show result
        run: |
          echo "Status: ${{ steps.delete.outputs.status }}"
```

---

## 📂 Outputs

| Name   | Description                                                      |
|--------|------------------------------------------------------------------|
| status | Status of the operation: `deleted`, `not-found`, or `error`     |

---

## 💡 Tips & Troubleshooting

- **Idempotent**: The action is safe to run multiple times. If the branch does not exist, it reports `not-found` and exits successfully (exit code 0).
- **Protected Branches**: This action cannot delete branches that are protected by branch protection rules. Ensure the target branch is not protected if you intend to delete it.
- **Generic Action**: While designed for cleanup in the release workflow, this action can be used anywhere a branch needs to be deleted.
- **GitHub Enterprise Support**: The action auto-detects the GitHub server hostname and works with GitHub Enterprise instances.

---

## 📄 License

This project is licensed under the Apache License 2.0.