# Merge Dashboard Data

Merges BTP runtime data (per-environment JSON files) with Git deployment configuration data into a single consolidated JSON file. The output JSON contains all packages and IFlows discovered on BTP tenants, enriched with Git deployment configuration.

The consolidated JSON file serves two purposes:
1. **Dashboard generation** — Used as input for the `generate-dashboard` action to build the HTML dashboard
2. **Data export** — Can be imported into Excel or other tools for further analysis

## Usage

```yaml
- uses: ./cicd-actions/.github/actions/merge-dashboard-data
  with:
    btp-data-dir: artifacts
    git-data-file: artifacts/git-data/git-data.json
    environments: '["DEV","TST","PRD"]'
    output-file: suite-repo/dashboard/dashboard-data.json
```

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `btp-data-dir` | ✅ | — | Directory containing `btp-data-*.json` files (one per environment) |
| `git-data-file` | ✅ | — | Path to the `git-data.json` file from `scan-deployment-config` |
| `environments` | ✅ | — | JSON array of environment names |
| `output-file` | ❌ | `dashboard-data.json` | Path to write the consolidated JSON file |

## Outputs

| Output | Description |
|--------|-------------|
| `file` | Path to the generated consolidated JSON file |
| `btp-package-count` | Number of packages discovered on BTP |
| `git-only-package-count` | Number of packages found only in Git (not on BTP) |

## Output JSON Structure

```json
{
  "generated": "2026-04-13T06:00:00Z",
  "environments": ["DEV", "TST", "PRD"],
  "packages": [
    {
      "id": "MyPackageId",
      "name": "My Package",
      "source": "btp",
      "gitConfig": {
        "found": true,
        "jsonFormat": "new"
      },
      "iflows": [
        {
          "id": "MyIFlow",
          "name": "My IFlow",
          "source": "btp",
          "hasGitConfig": true,
          "environments": {
            "DEV": {
              "deploy": "true",
              "logLevel": "INFO",
              "runtimeStatus": "STARTED",
              "runtimeVersion": "1.2.3"
            },
            "TST": {
              "deploy": "false",
              "logLevel": "ERROR",
              "runtimeStatus": "NOT_DEPLOYED",
              "runtimeVersion": null
            },
            "PRD": {
              "deploy": null,
              "logLevel": null,
              "runtimeStatus": null,
              "runtimeVersion": null
            }
          }
        }
      ]
    },
    {
      "id": "GitOnlyPkg",
      "name": "Git Only Package",
      "source": "git-only",
      "gitConfig": {
        "found": true,
        "jsonFormat": "old"
      },
      "iflows": [ ... ]
    }
  ],
  "summary": {
    "btpPackageCount": 13,
    "gitOnlyPackageCount": 2,
    "totalPackageCount": 15
  }
}
```

### Key Fields

| Field | Description |
|-------|-------------|
| `source` | Origin of the package/iflow: `"btp"` (discovered on BTP) or `"git-only"` (only in Git) |
| `gitConfig.found` | Whether the package has deployment configuration in Git |
| `gitConfig.jsonFormat` | Deployment JSON format: `"new"`, `"old"`, or `null` |
| `hasGitConfig` | Whether the specific IFlow has Git configuration |
| `environments.<ENV>.deploy` | Deploy flag from Git config (`"true"`/`"false"`/`null`) |
| `environments.<ENV>.logLevel` | Log level from Git config (`"ERROR"`/`"WARN"`/`"INFO"`/`"DEBUG"`/`"TRACE"`/`null`) |
| `environments.<ENV>.runtimeStatus` | BTP runtime status (`"STARTED"`/`"ERROR"`/`"NOT_DEPLOYED"`/`null`) |
| `environments.<ENV>.runtimeVersion` | Deployed version from BTP runtime (`"1.2.3"`/`null`) |

## How it Works

1. **BTP data collection**: Loads all BTP runtime data JSON files from `btp-data-dir` and builds a unified, de-duplicated list of all packages and IFlows seen across all environments
2. **Git data loading**: Loads the Git deployment configuration from `git-data-file`
3. **Package matching**: Matches BTP packages with Git configuration, identifies Git-only packages
4. **IFlow enrichment**: For each IFlow, merges per-environment data from both BTP runtime and Git config
5. **JSON output**: Writes the consolidated, structured JSON to the output file

## Dependencies

This action expects input data from:
- [`get-iflow-runtime-status`](../get-iflow-runtime-status/) — BTP runtime data files
- [`scan-deployment-config`](../scan-deployment-config/) — Git deployment configuration