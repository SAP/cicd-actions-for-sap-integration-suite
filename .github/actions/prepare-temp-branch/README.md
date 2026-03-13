# 🔀 Prepare Temporary Release Branch GitHub Action

Renames the development branch to a temporary release branch, or validates restart state.

---

## ✨ Overview

This action handles the first step of a release process: moving the development branch to a temporary branch name that includes the release name. This makes the development branch "slot" available for re-creation after the release is merged into main.

In restart scenarios, the action detects if the temporary branch already exists and skips the rename operation.

---

## ⚙️ Inputs

| Name                | Required | Description                                                        |
|---------------------|----------|--------------------------------------------------------------------|
| release-name        | ✅ Yes   | The release name, used to construct the temp branch name.          |
| development-branch  | ❌ No    | Name of the development branch. Defaults to `development`.         |
| github-token        | ✅ Yes   | GitHub token with `contents:write` permission.                     |

---

## 📝 Usage Example

```yaml
jobs:
  prepare:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Prepare temp branch
        id: prepare
        uses: ./.github/actions/prepare-temp-branch
        with:
          release-name: v1.0.0
          development-branch: development
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Show result
        run: |
          echo "Temp branch: ${{ steps.prepare.outputs.temp-branch }}"
          echo "Status: ${{ steps.prepare.outputs.status }}"
```

---

## 📂 Outputs

| Name        | Description                                                              |
|-------------|--------------------------------------------------------------------------|
| temp-branch | The name of the temporary release branch (`tmp/release-<release-name>`)  |
| status      | Status of the operation: `created`, `already-exists`, or `error`         |

---

## 💡 Tips & Troubleshooting

- **Branch Naming**: The temp branch is created as `tmp/release-<release-name>` (e.g., `tmp/release-v1.0.0`).
- **Rename Operation**: Git does not have a native branch rename via API. This action creates the temp branch at the same SHA as the development branch, then deletes the development branch.
- **Restart Safety**: If the temp branch already exists (from a previous run), the action skips the rename and reports `already-exists`.
- **Error Handling**: If neither the development branch nor the temp branch exists, the action fails with a clear error message.
- **GitHub Enterprise Support**: The action auto-detects the GitHub server hostname and works with GitHub Enterprise instances.

---

## 📄 License

This project is licensed under the Apache License 2.0.