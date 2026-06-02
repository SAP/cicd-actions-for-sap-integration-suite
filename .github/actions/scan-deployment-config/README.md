# Scan Deployment Configuration

Scans the `IntegrationPackages` directory in the checked-out repository for `Deployment_INTEGRATION_FLOW.json` files. Extracts per-IFlow per-environment settings (Deploy, LogLevel, Runtimes) and detects old vs new JSON format.

All package directories found in Git are scanned — no regex filtering is applied, since the repository already contains exactly the packages that matter.

## Usage

```yaml
- uses: ./cicd-actions/.github/actions/scan-deployment-config
  with:
    packages-dir: btp-insuite/IntegrationPackages
    environments: '["DEV","TST","PRD"]'
    output-file: ${{ runner.temp }}/git-data.json
```

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `packages-dir` | ✅ | — | Path to the `IntegrationPackages` directory |
| `environments` | ✅ | — | JSON array of environment names to extract settings for |
| `output-file` | ✅ | — | Path to write the output JSON file |

## Outputs

| Output | Description |
|--------|-------------|
| `file` | Path to the output JSON file containing Git config data |

## How it Works

1. Iterates over **all** package directories under `IntegrationPackages/`
2. Extracts the package name and ID from the directory name (format: `Name~ID`)
3. Locates the `Configuration/Deployment_INTEGRATION_FLOW.json` file
4. **Handles packages with no IFlows** (not an issue):
   - No deployment JSON file → package has no IFlows (e.g., value mapping packages)
   - Empty `IntegrationFlows: []` → package has no deployable IFlows
   - Both cases produce `jsonFormat: "none"` and `iflows: []` — this is expected and normal
5. **Detects JSON format** (when IFlows exist):
   - **New format** (`🟢`): Has `Environments` or `Rank` keys — supports per-environment overrides
   - **Old format** (`🟡`): Flat structure with only `Deploy` boolean flags
6. Extracts per-IFlow per-environment settings using this priority chain:
   - **Deploy**: `Environments[$ENV].Deploy` → `$ENV` (flat key) → `Deploy` (default)
   - **LogLevel**: `Environments[$ENV].LogLevel` → top-level `LogLevel` → `"INFO"`
   - **Runtimes**: `Environments[$ENV].Runtimes` → top-level `Runtimes` → `"iflmap"`

## Output JSON Structure

```json
{
  "packages": [
    {
      "id": "MyPackageId",
      "name": "My Package Name",
      "jsonFormat": "new",
      "iflows": [
        {
          "id": "MyIFlow_01",
          "name": "My IFlow 01",
          "rank": "10",
          "environments": {
            "DEV": { "deploy": "true", "logLevel": "DEBUG", "runtimes": "iflmap" },
            "TST": { "deploy": "true", "logLevel": "INFO", "runtimes": "iflmap" },
            "PRD": { "deploy": "false", "logLevel": "ERROR", "runtimes": "iflmap" }
          }
        }
      ]
    },
    {
      "id": "ValueMappingPackage",
      "name": "My Value Mappings",
      "jsonFormat": "none",
      "iflows": []
    }
  ]
}
```

## JSON Format Detection

| Format | Badge | Description |
|--------|-------|-------------|
| `new` | 🟢 | Enhanced format with `Environments` overrides per stage |
| `old` | 🟡 | Legacy format with flat `Deploy` boolean per environment |
| `none` | ⚪ | No IFlows in this package (no deployment JSON or empty `IntegrationFlows`) |
| `unknown` | ⚠️ | JSON file exists but structure is unrecognized |