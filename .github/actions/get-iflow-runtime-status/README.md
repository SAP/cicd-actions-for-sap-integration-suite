# Get IFlow Runtime Status

For a given list of packages, fetches all IFlows per package from BTP Integration Suite and queries their runtime status including deployed version.

## Usage

```yaml
- uses: ./cicd-actions/.github/actions/get-iflow-runtime-status
  with:
    bearer-token: ${{ steps.get-token.outputs.token }}
    btp-api-url: ${{ vars.BTP_API_URL }}
    packages: ${{ steps.get-packages.outputs.packages }}
    environment: DEV
    output-file: ${{ runner.temp }}/btp-data-DEV.json
```

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `bearer-token` | ✅ | — | Bearer token to access Integration Suite APIs |
| `btp-api-url` | ✅ | — | BTP Integration Suite API base URL |
| `packages` | ✅ | — | JSON array of packages `[{Id, Name}]` from `get-packages-by-regex` |
| `environment` | ✅ | — | Environment name (e.g. `DEV`, `TST`, `PRD`) used for labeling |
| `output-file` | ✅ | — | Path to write the output JSON file |

## Outputs

| Output | Description |
|--------|-------------|
| `file` | Path to the output JSON file containing runtime data |

## How it Works

1. Iterates over each package in the input list
2. For each package, calls `IntegrationDesigntimeArtifacts` API to get all IFlows
3. For each IFlow, calls `IntegrationRuntimeArtifacts` API to get runtime status and version
4. Writes a structured JSON file with all collected data

## Output JSON Structure

```json
{
  "environment": "DEV",
  "packages": [
    {
      "id": "MyPackage",
      "name": "My Package",
      "iflows": [
        {
          "id": "MyIFlow_01",
          "name": "My IFlow 01",
          "designtimeVersion": "1.0.5",
          "runtimeStatus": "STARTED",
          "runtimeVersion": "1.0.5"
        }
      ]
    }
  ]
}
```

## Runtime Status Values

| Status | Meaning |
|--------|---------|
| `STARTED` | IFlow is deployed and running |
| `ERROR` | IFlow is deployed but in error state |
| `NOT_DEPLOYED` | IFlow exists in design time but is not deployed |
| `UNKNOWN` | Status could not be determined |