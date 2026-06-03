# 🔍 Check Commit Has Release GitHub Action

Checks whether the HEAD commit of a branch already has any GitHub release pointing to it.

---

## ✨ Overview

This action resolves a branch to its HEAD commit SHA, then scans all repository tags to find any that point to that commit. If a matching tag has a GitHub release, the action reports `has-release=true`.

It is used in release workflows as a duplicate-release guard for the `no-changes` scenario: when the PR source branch is already in sync with `main` (e.g., after a manual merge), there may still be no release tag for that commit. This action decides whether it is safe to create one.

---

## ⚙️ Inputs

| Name         | Required | Description                                              |
|--------------|----------|----------------------------------------------------------|
| branch-name  | ✅ Yes   | Branch whose HEAD commit to check (e.g., `main`).        |
| github-token | ✅ Yes   | GitHub token with `contents:read` permission.            |

---

## 📂 Outputs

| Name         | Description                                                                    |
|--------------|--------------------------------------------------------------------------------|
| has-release  | Boolean string (`true`/`false`) — whether any release points to this commit    |
| release-name | Name of the existing release if found, otherwise empty string                  |

---

## 📝 Usage Example

```yaml
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Check if main commit already has a release
        id: check-commit-release
        uses: ./.github/actions/check-commit-has-release
        with:
          branch-name: main
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Create release (if not already released)
        if: steps.check-commit-release.outputs.has-release != 'true'
        run: echo "Safe to create release"

      - name: Skip release (already released)
        if: steps.check-commit-release.outputs.has-release == 'true'
        run: echo "Release '${{ steps.check-commit-release.outputs.release-name }}' already exists for this commit"
```

---

## 💡 How It Works

1. Resolves `branch-name` to its HEAD commit SHA via the GitHub API
2. Lists all repository tags — GitHub automatically dereferences annotated tags to their commit SHA
3. Filters for tags pointing to the HEAD commit
4. For each matching tag, checks whether a GitHub release exists
5. Returns `has-release=true` and the release name on the first match; `has-release=false` if none found

---

## 💡 Tips & Troubleshooting

- **GitHub Enterprise Support**: The action auto-detects the GitHub server hostname and works with GitHub Enterprise instances.
- **Annotated vs lightweight tags**: Both are handled — the `/tags` endpoint always returns the underlying commit SHA regardless of tag type.
- **Multiple tags on one commit**: The action stops at the first tag that has a release. The `release-name` output reflects that first match.
- **No tags on commit**: If the commit has no tags at all, `has-release=false` is returned immediately without further API calls.

---

## 📄 License

This project is licensed under the Apache License 2.0.
