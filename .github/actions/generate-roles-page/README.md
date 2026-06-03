# generate-roles-page

Generates an interactive HTML page (`docs/roles.html`) showing all IFlows and their configured `userRole`, grouped by package. The page matches the visual style of the Integration Suite Dashboard and includes shared navigation.

## Overview

The page is generated from the JSON output of `scan-iflow-roles`. It provides:
- A summary of how many IFlows have roles configured, how many don't, and how many have issues
- Per-package collapsible tables with IFlow Name, IFlow ID, and User Role
- Color-coded rows indicating role status
- Filter bar for searching and filtering by status
- Navigation bar linking to the main dashboard

## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `roles-data-file` | ✅ | — | Path to `roles-data.json` from `scan-iflow-roles` |
| `output-file` | ❌ | `docs/roles.html` | Path to write the generated HTML |
| `github-repository` | ❌ | `""` | `owner/repo` for display in header |

## Outputs

| Output | Description |
|---|---|
| `file` | Path to the generated HTML file |
| `changed` | `true` if content changed since last git commit, `false` otherwise |

## Usage

```yaml
- name: Generate roles page
  id: roles-page
  uses: ./cicd-actions/.github/actions/generate-roles-page
  with:
    roles-data-file: artifacts/roles-data/roles-data.json
    output-file: suite-repo/docs/roles.html
    github-repository: ${{ github.repository }}
```

## Row Color Coding

| Status | Row Color | Prefix | Meaning |
|---|---|---|---|
| `defined` | ✅ green | ✅ | `userRole` found and resolved |
| `none` | neutral | *(none)* | No `userRole` configured — uses different auth type |
| `error` | 🔴 red | 🔴 | Externalized `{{param}}` — not found in ConfigParams |
| `not-in-git` | ❓ gray | ❓ | `.iflw` file not found in Git development branch |

## Package Header Colors

The package header color reflects the worst status among its IFlows:
- 🔴 red — any IFlow has an unresolved parameter
- ❓ gray — any IFlow not found in Git (no red errors)
- ⚠️ yellow — all IFlows found, some have no role (no errors/not-in-git)
- ✅ green — all IFlows have roles defined

## Navigation

The page includes a navigation bar in the header:

```
📊 Dashboard  |  🔑 IFlow Roles (active)
```

This links to `index.html` (dashboard) using a relative URL, suitable for GitHub Pages. Additional tabs can be added by editing the `<nav class="page-nav">` block.

## Implementation Notes

- Uses the same CSS variables, typography, and component structure as `generate-dashboard`
- All JavaScript attribute strings use double quotes (no single quotes inside `HTML+='...'` bash strings)
- The `changed` output uses `git diff` and is safe to use in conditional commit logic
