# scan-iflow-roles

Scans integration flow (`.iflw`) files in the Git repository and extracts the configured `userRole` property for each IFlow, with externalized parameter resolution.

## Overview

The action is driven by the BTP API: it fetches the current IFlow list per package, then locates each IFlow's source file in the Git checkout to read its `userRole` configuration. This gives a complete view of all deployed IFlows — those without a Git counterpart are shown as **not in Git**.

**Not every IFlow has a `userRole` — this is normal** and does not produce an error. Only IFlows that use HTTPS/role-based authentication configure this property.

## Inputs

| Input | Required | Description |
|---|---|---|
| `bearer-token` | ✅ | OAuth Bearer token for BTP API |
| `btp-api-url` | ✅ | BTP API base URL |
| `packages` | ✅ | JSON array `[{Id, Name}]` from `get-packages-by-regex` |
| `environment` | ✅ | Environment name for ConfigParams resolution (e.g. `DEV`) |
| `packages-dir` | ✅ | Absolute path to `IntegrationPackages/` directory in Git checkout |
| `output-file` | ✅ | Path to write `roles-data.json` |

## Outputs

| Output | Description |
|---|---|
| `file` | Path to the generated `roles-data.json` |
| `iflow-count` | Total IFlows processed |
| `roles-found` | IFlows with a resolved `userRole` |

## Usage

```yaml
- name: Scan IFlow roles
  id: scan-roles
  uses: ./cicd-actions/.github/actions/scan-iflow-roles
  with:
    bearer-token: ${{ steps.get-token.outputs.token }}
    btp-api-url: ${{ vars.BTP_API_URL }}
    packages: ${{ steps.get-packages.outputs.packages }}
    environment: DEV
    packages-dir: ${{ github.workspace }}/btp-insuite/IntegrationPackages
    output-file: ${{ runner.temp }}/roles-data.json
```

## How It Works

For each package in the input list:

1. **Locate Git folder** — searches `packages-dir` for a subdirectory ending with `~{PackageID}` (ID-only match, robust to name differences between BTP and Git).
2. **Fetch IFlows from BTP** — calls `GET /api/v1/IntegrationPackages('{ID}')/IntegrationDesigntimeArtifacts`. A 404 is treated as "package not on BTP yet" (warning logged, package skipped).
3. **Load ConfigParams** — reads `{PackageDir}/Configuration/ConfigParams_INTEGRATION_FLOW.json` once per package (used for externalized parameter resolution).
4. **Per IFlow — find `.iflw` file** — searches the package directory for `{IFlowID}.iflw`; if not found, falls back to `{IFlowName}.iflw`. Uses `head -1` when multiple UUID-versioned content folders contain the same file.
5. **Extract `userRole`** from XML using perl (slurp mode, handles any whitespace/newline formatting):
   ```perl
   /userRole<\/key>\s*<value>(.*?)<\/value>/s
   ```
6. **Resolve externalized params** — if the value matches `{{paramName}}`:
   - Looks up `ParameterKey == paramName` in ConfigParams for the matching `ArtifactID`
   - Uses `ParameterValues[ENV]` first, falls back to `ParameterValues.Default`
   - If no match found: `roleStatus = "error"`

## Output JSON Structure

```json
{
  "generated": "2026-05-06T12:00:00Z",
  "devEnvironment": "DEV",
  "packages": [
    {
      "id": "MyPackageId",
      "name": "My Package Name",
      "iflows": [
        {
          "id": "IFlow_01",
          "name": "My IFlow 01",
          "userRole": "AuthGroup_BusinessExpert",
          "roleStatus": "defined",
          "roleSource": "direct"
        }
      ]
    }
  ],
  "summary": {
    "totalPackages": 5,
    "totalIflows": 42,
    "iflowsWithRole": 18,
    "iflowsWithoutRole": 20,
    "iflowsNotInGit": 3,
    "iflowsParamUnresolved": 1
  }
}
```

### `roleStatus` Reference

| Value | Meaning | Visual |
|---|---|---|
| `defined` | `userRole` found and resolved | ✅ green |
| `none` | No `userRole` property configured | neutral |
| `error` | `{{param}}` pattern, param not in ConfigParams | 🔴 red |
| `not-in-git` | `.iflw` file not found in Git checkout | ❓ gray |

### `roleSource` Reference

| Value | Meaning |
|---|---|
| `direct` | Value read directly from `.iflw` XML |
| `param-resolved` | Value was `{{param}}`, resolved from ConfigParams |
| `param-unresolved` | Value was `{{param}}`, no match in ConfigParams |
| `none` | No `.iflw` file found |

## ConfigParams Resolution Details

The `ConfigParams_INTEGRATION_FLOW.json` file lives at:
```
IntegrationPackages/{PackageName}~{PackageID}/Configuration/ConfigParams_INTEGRATION_FLOW.json
```

The action matches by `ArtifactID` (= IFlow ID from BTP) and `ParameterKey` (= the param name from `{{paramName}}`). The resolution order is:
1. `ParameterValues[ENV]` where ENV = the `environment` input
2. `ParameterValues.Default`
3. If neither exists: `roleStatus = "error"`

## Notes

- **Multiple UUID folders:** When the same IFlow name appears in multiple `{uuid}_content/` subdirectories (multiple artifact versions stored), `head -1` selects the lexicographically first one. The `userRole` is typically stable across versions.
- **XML entity encoding:** Raw XML entities (`&amp;`, `&lt;`) in role values are not decoded. Real-world role names (`AuthGroup_*` naming convention) do not contain XML special characters.
