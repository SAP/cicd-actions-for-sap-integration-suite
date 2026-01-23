# 💾 GIT Commit GitHub Action

Stage, commit, and push changes to Git with automatic conflict resolution and verification.

---

## ✨ Overview

This action stages all modified files in the repository, creates a Git commit with a provided message, and pushes the changes to the remote branch. It includes intelligent retry logic with automatic rebasing to handle concurrent commits and potential merge conflicts. The action configures Git with the workflow actor's identity, only commits if there are staged changes, and verifies that the remote branch is updated with the commit before completing.

---

## ⚙️ Inputs

| Name    | Required | Description                     |
|---------|----------|---------------------------------|
| comment | ✅ Yes   | Commit message/comment text.    |

---

## 📝 Usage Example

```yaml
jobs:
  commit-changes:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Make Changes
        run: |
          echo "Modified content" > btp-insuite/IntegrationPackages/file.txt
      
      - name: Commit Changes
        uses: ./.github/actions/git-commit
        with:
          comment: "Update integration package configuration"

  extract-and-commit:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Download Package
        id: download
        uses: ./.github/actions/get-cpi-package-as-zip
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          package-name: my-package
      
      - name: Extract Package
        uses: ./.github/actions/unzip-package-into-repo
        with:
          location-zip: ${{ steps.download.outputs.location }}
      
      - name: Commit to Git
        uses: ./.github/actions/git-commit
        with:
          comment: "Sync package from CPI - $(date +'%Y-%m-%d %H:%M:%S')"

  prepare-and-commit:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Prepare Repository
        uses: ./.github/actions/prepare-repo
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          package-name: my-package
      
      - name: Download and Extract
        id: download
        uses: ./.github/actions/get-cpi-package-as-zip
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          package-name: my-package
      
      - name: Unzip Package
        uses: ./.github/actions/unzip-package-into-repo
        with:
          location-zip: ${{ steps.download.outputs.location }}
      
      - name: Create Deployment Configuration
        uses: ./.github/actions/create-iflow-deployment-file
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          package-name: my-package
          file: iflow-list.json
      
      - name: Commit All Changes
        uses: ./.github/actions/git-commit
        with:
          comment: "Refresh package and update deployment configuration"
```

---

## 📂 Outputs

This action has no outputs. It performs Git operations directly on the repository.

**Side Effects:**
- Stages all modified and new files in the current working directory
- Creates a commit with the provided message
- Pushes the commit to the remote branch
- Automatically rebases and retries on push failures
- Verifies remote branch synchronization

---

## 💡 Tips & Troubleshooting

- **Git User Identity**: The action automatically configures Git with the GitHub workflow actor's username and email. No manual Git configuration is needed.

- **Working Directory**: The action operates in `btp-insuite/IntegrationPackages` directory. Only changes within this directory are staged and committed.

- **Stage All Changes**: The action uses `git add -A` to stage all modifications, new files, and deletions in the working directory.

- **Empty Changeset**: If no changes are detected, the action exits gracefully without creating a commit. This prevents empty commits and keeps the repository clean.

- **Push Retry Logic**: The action implements automatic retry with exponential backoff (up to 5 attempts) if the initial push fails due to remote changes.

- **Rebase Conflict Resolution**: When a push fails, the action automatically rebases your changes against the remote branch to resolve conflicts. This is safer than merge for maintaining a clean history.

- **Remote Verification**: After pushing, the action verifies that the remote branch reflects your commit (up to 10 attempts with 2-second waits). This ensures the push was successful before the action completes.

- **Retry Attempts**: Push retry attempts are limited to 5 tries. If all retries fail, the action exits with an error code 1.

- **Branch Detection**: The action automatically detects the current branch using `git rev-parse --abbrev-ref HEAD` and pushes to that same branch on origin.

- **Concurrent Commits**: The rebase retry mechanism handles scenarios where other workflows or developers push commits to the same branch concurrently.

- **Commit Message**: Use clear, descriptive commit messages. Include context about what changed or why. Example: "Add integration flow X configuration" or "Sync packages from BTP environment".

- **Email Privacy**: The action uses GitHub's privacy-protected email format (`{actor}@users.noreply.github.com`) to keep your email address private.

- **Error Handling**: The action uses `set -e` to exit immediately on any Git command failure, ensuring clean error handling.

- **SSH vs HTTPS**: The action uses the default Git configuration from the checkout step. If using SSH keys, ensure they're properly configured in the workflow.

- **Branch Protection**: If your branch is protected and requires status checks, pull requests, or approvals, the direct push may be blocked. Adjust branch protection rules if needed.

- **Permission Issues**: Ensure the workflow has permission to push to your repository. Check GitHub token permissions and branch access rules.

- **Multiple Commits**: If you need to create multiple commits in a single workflow, call this action multiple times with different comments and ensure changes are made between calls.

- **Cleanup**: After committing, use this action to ensure your repository reflects the current state, useful after preparing, downloading, and extracting packages.

- **Timestamps**: Include timestamps in commit messages for audit trails, especially for automated package syncs.

---

## 📄 License

This project is licensed under the Apache License 2.0.