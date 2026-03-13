# 🔍 Check Release/Tag Exists GitHub Action

Checks if a git tag or GitHub release already exists for a given release name.

---

## ✨ Overview

This action verifies whether a release or tag with the specified name already exists in the repository. It is used as an early validation step in release workflows to prevent duplicate releases and to detect restart scenarios where a partial release process needs to be resumed.

---

## ⚙️ Inputs

| Name          | Required | Description                                              |
|---------------|----------|----------------------------------------------------------|
| release-name  | ✅ Yes   | The release/tag name to check (e.g., `v1.0.0`).         |
| github-token  | ✅ Yes   | GitHub token with `contents:read` permission.            |

---

## 📝 Usage Example

```yaml
jobs:
  check-release:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Check if release exists
        id: check
        uses: ./.github/actions/check-release-tag-exists
        with:
          release-name: v1.0.0
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Handle result
        run: |
          if [ "${{ steps.check.outputs.release-exists }}" == "true" ]; then
            echo "Release already exists!"
          else
            echo "Release does not exist, safe to create."
          fi
```

---

## 📂 Outputs

| Name           | Description                                                    |
|----------------|----------------------------------------------------------------|
| release-exists | Boolean string (`true`/`false`) — whether the release exists   |
| tag-exists     | Boolean string (`true`/`false`) — whether the tag exists       |

---

## 💡 Tips & Troubleshooting

- **GitHub Enterprise Support**: The action auto-detects the GitHub server hostname and works with GitHub Enterprise instances.
- **Tag vs Release**: A tag can exist without a release (e.g., created via `git tag`). This action checks both independently.
- **Restart Safety**: Use this action at the start of release workflows to determine whether a previous run already created the release, enabling safe restart logic.

---

## 📄 License

This project is licensed under the Apache License 2.0.