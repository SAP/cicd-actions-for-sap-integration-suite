# Generate Dashboard

Generates a rich, interactive HTML dashboard from a consolidated JSON data file (produced by [`merge-dashboard-data`](../merge-dashboard-data/)). The dashboard is BTP-driven: it shows ALL packages and IFlows discovered on BTP tenants across all environments, enriched with Git deployment config. Packages or IFlows found on BTP but missing from Git are highlighted as important findings (⚠️).

The HTML output is suitable for **GitHub Pages** deployment and includes client-side filtering.

## Usage

```yaml
- uses: ./cicd-actions/.github/actions/generate-dashboard
  with:
    dashboard-data-file: suite-repo/dashboard/dashboard-data.json
    environments: '["DEV","TST","PRD"]'
    output-file: suite-repo/dashboard/index.html
    github-repository: ${{ github.repository }}
```

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `dashboard-data-file` | ✅ | — | Path to the consolidated `dashboard-data.json` file (from `merge-dashboard-data`) |
| `environments` | ✅ | — | JSON array of environment names |
| `output-file` | ❌ | `dashboard/index.html` | Path to write the generated HTML dashboard file |
| `github-repository` | ❌ | — | GitHub repository name (`owner/repo`) for display in header |

## Outputs

| Output | Description |
|--------|-------------|
| `file` | Path to the generated HTML dashboard file |
| `changed` | Whether the dashboard content changed (`true`/`false`) |

## How it Works

1. **Load data**: Reads the consolidated JSON from `dashboard-data-file` (produced by `merge-dashboard-data`)
2. **Render packages**: For each package, generates an HTML card with a table containing:
   - **Columns**: IFlow Name, IFlow ID, and one compact column per environment
   - Each environment column stacks **Deploy**, **LogLevel**, and **Runtime** vertically
   - **Visual badges** for quick scanning (✅ ❌ 🔴 🔵 🟢 ⚠️ etc.)
   - **JSON format indicator** (🟢 new / 🟡 old / ⚪ none)
3. **Gap highlighting**: Packages/IFlows found on BTP but missing from Git are marked with ⚠️ warning styling
4. **Git-only section**: Shows packages that exist in Git but were not found on any BTP tenant (🔍)
5. **Summary cards**: Visual summary with counts of BTP packages, missing Git configs, etc.
6. **Legend**: Explains all symbols used in the dashboard
7. **Client-side filtering**: Search bar to filter by package/IFlow name or ID, plus a checkbox to show only warning items

## Dashboard Features

- **Responsive design** with clean, GitHub-inspired styling
- **Interactive search/filter** — filter packages and IFlows by name or ID in real-time
- **Warning filter** — toggle to show only items missing Git configuration
- **Summary cards** — at-a-glance counts of packages and configuration gaps
- **Visual badges** — color-coded status indicators for quick scanning

## Generated Dashboard Structure

```
┌─────────────────────────────────────────────────┐
│  📊 Integration Suite Dashboard                  │
│  📁 org/my-repo  📅 2026-04-13  🌍 DEV,TST,PRD │
├─────────────────────────────────────────────────┤
│  🔍 Filter by package or IFlow...  ☐ warnings   │
├─────────────────────────────────────────────────┤
│  📦 My Package (MyPackageId)                     │
│  Deployment JSON: 🟢 new                         │
│  ┌────────────┬──────────┬────────┬────────┐    │
│  │ IFlow Name │ IFlow ID │ TST    │ PRD    │    │
│  ├────────────┼──────────┼────────┼────────┤    │
│  │ My IFlow   │ MyIFlow  │ ✅ true│ ❌ fls │    │
│  │            │          │ 🔵 INFO│ 🔵 INFO│    │
│  │            │          │ ✅ v1.2│ —      │    │
│  └────────────┴──────────┴────────┴────────┘    │
├─────────────────────────────────────────────────┤
│  ⚠️ 📦 BTP-Only Package (BTPOnlyPkg)            │
│  ⚠️ Not found in Git                            │
│  ┌────────────┬──────────┬────────┬────────┐    │
│  │ ⚠️ SomeFlow│ Flow1    │ —      │ —      │    │
│  │            │          │ —      │ —      │    │
│  │            │          │ ✅ v2.0│ —      │    │
│  └────────────┴──────────┴────────┴────────┘    │
├─────────────────────────────────────────────────┤
│  📈 Summary                                      │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐           │
│  │  13  │ │  3   │ │  12  │ │  2   │           │
│  │ BTP  │ │No Git│ │IFlows│ │Git-  │           │
│  │ Pkgs │ │Config│ │No Git│ │Only  │           │
│  └──────┘ └──────┘ └──────┘ └──────┘           │
│  ⚠️ Action required: 3 pkg(s) and 12 IFlow(s)  │
├─────────────────────────────────────────────────┤
│  📋 Legend                                       │
└─────────────────────────────────────────────────┘
```

## Visual Badges

| Symbol | Meaning |
|--------|---------|
| ✅ | Deployed / Enabled / Started |
| ❌ | Not deployed / Disabled |
| ⚫ | Not available on runtime |
| ⚠️ | No Git configuration found (BTP-only) |
| 🔴 | Error / ERROR log level |
| 🟡 | Warning / Old format |
| 🔵 | INFO log level |
| 🟢 | Debug / New format |
| 🟣 | TRACE log level |
| 🔍 | Exists in Git but not found on BTP |
| — | Not configured / Unknown |

## Dependencies

This action expects input data from:
- [`merge-dashboard-data`](../merge-dashboard-data/) — Consolidated JSON data file