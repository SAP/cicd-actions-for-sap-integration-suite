# generate-github-token

Generates a GitHub token from a **GitHub App installation** (preferred) or falls back to a **Personal Access Token (PAT)**. This action allows teams to migrate from PATs to GitHub Apps incrementally without breaking existing workflows.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `app-id` | No | GitHub App Client/App ID |
| `private-key` | No | GitHub App private key PEM content |
| `token` | No | PAT fallback (used when app credentials are not provided) |
| `owner` | No | Org/owner to scope the app token to (defaults to current repo owner) |

## Outputs

| Output | Description |
|--------|-------------|
| `token` | Resolved GitHub token (app installation token or PAT) |

## Priority

1. If `app-id` **and** `private-key` are both provided → generates a GitHub App installation token
2. Else if `token` is provided → uses it as-is (PAT)
3. Else → fails with a clear error message

## Usage

```yaml
- uses: ./cicd-btp-insuite/.github/actions/generate-github-token
  id: github-token
  with:
    app-id: ${{ vars.GIT_GITHUB_APP_ID }}
    private-key: ${{ secrets.GIT_GITHUB_APP_PRIVATE_KEY }}
    token: ${{ secrets.GIT_SUITE_TOKEN }}   # PAT fallback

- name: Use the token
  env:
    GH_TOKEN: ${{ steps.github-token.outputs.token }}
  run: gh api /repos/${{ github.repository }}/releases
```

## GitHub App Setup

1. Create a GitHub App in your organization with these permissions:
   - **Contents**: Read and write
   - **Pull requests**: Read and write
   - **Members** (org): Read-only
2. Generate a private key and download the `.pem` file
3. Install the app in your repository/organization
4. Store credentials:
   - `GIT_GITHUB_APP_ID` → repository or org **variable** (not secret)
   - `GIT_GITHUB_APP_PRIVATE_KEY` → repository or org **secret** (full `.pem` content)

## Notes

- App installation tokens expire after 1 hour and are automatically revoked after the job completes
- On **GitHub Enterprise Server (GHES)**, `actions/create-github-app-token` may have limitations — use the PAT fallback if issues arise
