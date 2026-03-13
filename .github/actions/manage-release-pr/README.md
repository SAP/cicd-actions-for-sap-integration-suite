# 📋 Manage Release Pull Request GitHub Action

Finds or creates a PR from a source to target branch, checks mergeability, and performs a squash merge.

---

## ✨ Overview

This action manages the entire lifecycle of a release pull request:
1. **Searches** for an existing PR with a deterministic title (for restart detection)
2. **Creates** a new PR if none exists
3. **Checks** if the PR can be automatically merged (no conflicts)
4. **Squash-merges** the PR into the target branch

If the PR has merge conflicts, the action fails with a clear error message. The PR remains open so the user can resolve conflicts and restart the workflow.

---

## ⚙️ Inputs

| Name           | Required | Description                                                          |
|----------------|----------|----------------------------------------------------------------------|
| release-name   | ✅ Yes   | The release name (used for deterministic PR title).                  |
| source-branch  | ✅ Yes   | Source branch for the PR.                                            |
| target-branch  | ❌ No    | Target branch for the PR. Defaults to `main`.                        |
| github-token   | ✅ Yes   | GitHub token with `contents:write` and `pull-requests:write`.        |

---

## 📝 Usage Example

```yaml
jobs:
  merge:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Manage release PR
        id: pr
        uses: ./.github/actions/manage-release-pr
        with:
          release-name: v1.0.0
          source-branch: tmp/release-v1.0.0
          target-branch: main
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Show result
        run: |
          echo "PR #${{ steps.pr.outputs.pr-number }}: ${{ steps.pr.outputs.pr-state }}"
          echo "Merge SHA: ${{ steps.pr.outputs.merge-sha }}"
```

---

## 📂 Outputs

| Name       | Description                                                          |
|------------|----------------------------------------------------------------------|
| pr-number  | The PR number                                                        |
| pr-url     | The URL of the PR                                                    |
| pr-state   | State after this action: `merged`, `no-changes`, `conflict`, or `error` |
| merge-sha  | The merge commit SHA (only set when PR is merged)                    |

---

## 💡 Tips & Troubleshooting

- **PR Title Convention**: The PR title follows the pattern `Release <release-name>: Merge into <target-branch>`. This deterministic naming enables the action to find existing PRs on restart.
- **Mergeability Check**: GitHub may take a moment to compute mergeability after PR creation. The action retries up to 5 times with a 3-second delay.
- **Conflict Resolution**: If the PR has conflicts, resolve them manually on the source branch, then restart the workflow. The action will find the existing PR and retry the merge.
- **No Changes**: If the source branch has no commits ahead of the target branch (i.e., nothing to release), the action exits successfully with `pr-state=no-changes` instead of failing. No PR is created.
- **Already Merged**: If the PR is already merged (restart after successful merge), the action reports success and returns the existing merge SHA.
- **Squash Merge**: The action always uses squash merge to keep the main branch history clean.
- **GitHub Enterprise Support**: The action auto-detects the GitHub server hostname and works with GitHub Enterprise instances.

---

## 📄 License

This project is licensed under the Apache License 2.0.