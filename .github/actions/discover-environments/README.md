# Discover GitHub Environments

Discovers all GitHub environments configured on the repository, filtered to those with required BTP variables defined.

## Usage

```yaml
- uses: ./cicd-actions/.github/actions/discover-environments
  with:
    github-token: ${{ steps.app-token-suite.outputs.token }}
    github-api-url: ${{ github.api_url }}
    github-repository: ${{ github.repository }}
```

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `github-token` | ✅ | — | GitHub token with `Actions: Read-only` and `Environments: Read-only` permissions |
| `github-api-url` | ✅ | — | GitHub API base URL (use `${{ github.api_url }}`) |
| `github-repository` | ✅ | — | GitHub repository in `owner/repo` format |
| `required-variables` | ❌ | `["BTP_API_URL","BTP_API_USER","BTP_TOKEN_URL"]` | JSON array of variable names that must exist on an environment for it to be included. Set to `"[]"` to skip validation. |

## Outputs

| Output | Description |
|--------|-------------|
| `environments` | JSON array of qualified environment names, sorted alphabetically (e.g. `["DEV","PRD","TST"]`) |
| `count` | Number of qualified environments |

## How it Works

1. Calls `GET /repos/{owner}/{repo}/environments` to list all environments
2. Excludes `github-pages` unconditionally
3. For each remaining environment, calls `GET /environments/{env}/variables` and checks that all `required-variables` are defined
4. Returns the qualified environments sorted alphabetically

## Required GitHub App Permissions

The token must have:
- `Actions: Read-only` — to list environments
- `Environments: Read-only` — to read per-environment variables

## Example Output

If the repository has environments `DEV`, `TST`, `PRD`, and `POC` configured, and only `DEV`, `TST`, `PRD` have `BTP_TOKEN_URL` defined:

```json
["DEV", "PRD", "TST"]
```

`POC` is excluded because it is missing the required variables.
