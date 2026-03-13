# 🏷️ Create GitHub Release Action

Creates a GitHub release with a tag on a specified branch.

---

## ✨ Overview

This action creates a GitHub release with an associated tag on the specified branch. It includes automatic release notes generation. In restart scenarios, if the release already exists, the action skips creation and reports the existing release details.

---

## ⚙️ Inputs

| Name           | Required | Description                                                  |
|----------------|----------|--------------------------------------------------------------|
| release-name   | ✅ Yes   | The release/tag name to create (e.g., `v1.0.0`).            |
| target-branch  | ❌ No    | The branch to create the release from. Defaults to `main`.   |
| github-token   | ✅ Yes   | GitHub token with `contents:write` permission.               |

---

## 📝 Usage Example

```yaml
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Create GitHub release
        id: release
        uses: ./.github/actions/create-github-release
        with:
          release-name: v1.0.0
          target-branch: main
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Show result
        run: |
          echo "Release URL: ${{ steps.release.outputs.release-url }}"
          echo "Status: ${{ steps.release.outputs.status }}"
```

---

## 📂 Outputs

| Name        | Description                                                            |
|-------------|------------------------------------------------------------------------|
| release-id  | The ID of the created (or existing) release                            |
| release-url | The URL of the created (or existing) release                           |
| status      | Status of the operation: `created`, `already-exists`, or `error`       |

---

## 💡 Tips & Troubleshooting

- **Auto-Generated Release Notes**: The action uses GitHub's `generate_release_notes` feature to automatically populate the release body with a summary of changes.
- **Restart Safety**: If the release already exists, the action skips creation and reports `already-exists` with the existing release URL.
- **Tag Creation**: The release automatically creates a git tag with the same name as the release on the target branch.
- **GitHub Enterprise Support**: The action auto-detects the GitHub server hostname and works with GitHub Enterprise instances.

---

## 📄 License

This project is licensed under the Apache License 2.0.