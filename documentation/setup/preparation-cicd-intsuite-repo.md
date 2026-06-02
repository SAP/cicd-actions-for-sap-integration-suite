# Preparation of Target Repository

This guide explains how to prepare your target repository where SAP Integration Suite artifacts and partner directory entries will be stored and managed.

## 📁 Repository Setup

Create a new Git repository that will serve as the central storage for your integration design artifacts downloaded from SAP Integration Suite.

### Initial Setup

#### 1. Create Repository Structure

Your repository requires a single directory:

```
.github/workflows/
```

> **⚠️ Required GitHub environment names:** The CI/CD pipeline workflows require GitHub environments named exactly **`DEV`** and **`TST`**. These names are hardcoded in the pipeline flows — use different names and those workflows will fail. Additional environments (`PRD`, `POC`, etc.) are optional and appear automatically in all dropdowns once configured with BTP credentials.

#### 2. Bootstrap the Sync Workflow

Instead of copying all workflow files manually, you only need to copy **one file** — the template sync workflow. It will pull all remaining templates automatically.

1. Navigate to `templates/workflows/` in the [cicd-actions-for-sap-integration-suite](https://github.com/SAP/cicd-actions-for-sap-integration-suite) repository.
2. Copy **`sync-cicd-templates.yml`** to your repository's `.github/workflows/` directory.
3. No reference adjustments are needed — the workflow reads `GIT_CICD_ORGREPO` and `GIT_CICD_REF` from your repository variables and applies them automatically on every sync.

#### 3. Complete GitHub Environment Setup

Before running the sync, configure all required variables and secrets as described in [Setup GIT Environment](setup-git-env.md). Pay particular attention to:

- `GIT_CICD_ORGREPO` — the org/repo of the cicd-actions repository (e.g. `SAP/cicd-actions-for-sap-integration-suite` or your fork)
- `GIT_CICD_REF` — the version tag to use in all `uses:` references (e.g. `v1`)
- `GIT_GITHUB_APP_ID` + `GIT_GITHUB_APP_PRIVATE_KEY` — consumer bot app (required)
- `GIT_CICD_APP_ID` + `GIT_CICD_APP_PRIVATE_KEY` — CICD reader app (required)

#### 4. Run the Initial Sync

Once variables and secrets are in place:

1. Go to **Actions** → **Sync CICD Workflow Templates** in your repository.
2. Click **Run workflow** (leave `source-ref` blank to use `GIT_CICD_REF`, leave scenario inputs empty).
3. The workflow contacts the central repository, discovers available scenarios, and populates the **install-scenario** dropdown for future runs. No workflow files are installed yet.
4. Run the workflow a second time, this time selecting a scenario in the **Add a scenario** dropdown to install the workflow templates you need.
5. Changes are committed and pushed **directly to your default branch** — no PR is created.

> **📝 Note:** No integration artifacts or configuration files are needed initially. These will be automatically added to your repository through the CI/CD automation process when you run the workflows.

---

## 🌍 Dynamic Environment Dropdowns

All workflow templates that ask you to select a target or source BTP environment (e.g. `btp-deploy-delete.yml`, `btp-release-import.yml`, `btp-download-to-git.yml`) show a dropdown populated with your **actual configured GitHub environments** — not a hardcoded list.

### How it works

Every time `sync-cicd-templates.yml` runs (daily or manually), it:

1. Calls the GitHub API to list all environments in your repository
2. Filters to environments that have the required BTP variables defined (`BTP_API_URL`, `BTP_API_USER`, `BTP_TOKEN_URL`)
3. Excludes the reserved `github-pages` environment
4. Injects the resulting list into every workflow template that contains a `target-env` or `source-env` dropdown
5. Commits the updated workflow files to your repository

### What you see

If your repository has environments `DEV`, `TST`, and `PRD` configured with BTP credentials, the `target-env` dropdown will show:

```
(empty — no selection)
DEV
PRD
TST
```

A partially-configured environment (missing `BTP_API_URL`, `BTP_API_USER`, or `BTP_TOKEN_URL`) will not appear in any dropdown.

### When dropdowns update

- **Daily at 01:00 UTC** — the scheduled sync run refreshes all dropdowns automatically
- **On manual sync** — run `sync-cicd-templates.yml` any time to force an immediate refresh after adding or removing environments

> **Note:** The empty first option is intentional — it prevents accidental execution against a default environment. The workflow will fail fast if no environment is selected.

---

## 📦 Scenario Management

Workflows are grouped into **scenarios** — sets of related templates that are installed or removed together. The sync workflow only downloads and keeps workflow files that belong to an active scenario.

### Install a scenario

1. Go to **Actions** → **Sync CICD Workflow Templates**
2. Click **Run workflow**
3. In the **Add a scenario** dropdown, select the scenario you want to activate
4. Click **Run workflow** — the sync will add it to the active list and download its workflow files

### Remove a scenario

1. Go to **Actions** → **Sync CICD Workflow Templates**
2. Click **Run workflow**
3. In the **Remove a scenario** dropdown, select the scenario you want to deactivate
4. Click **Run workflow** — the sync will remove it from the active list and delete its workflow files

### How scenarios work

- Active scenarios are tracked in `.github/cicd-scenarios.txt` in your repository
- On every sync, only workflow files belonging to an active scenario are downloaded or updated
- Files belonging to a removed scenario are automatically deleted from `.github/workflows/`
- Workflow files you created yourself (not part of any scenario) are never touched
- The **install** dropdown shows only scenarios not yet active; the **remove** dropdown shows only currently active scenarios — both are populated dynamically at sync time

---

## 🔁 Keeping Templates Up-to-Date

The sync workflow runs **daily at 01:00 UTC** automatically. When templates change in the central repo:

- Changed workflow files are committed and pushed **directly to your default branch** with a `[skip ci]` commit message.
- If nothing changed, the run exits silently without a commit.

To protect a customised template from being overwritten, create `.github/cicd-sync-exclusions.txt`:

```
# Filenames to never overwrite (one per line, # = comment)
btp-deploy-delete.yml      # customised; do not sync
```

Customer-built workflows with unique filenames are automatically safe — the sync only ever touches files that exist as templates in the central repo.

> **Note on the sync workflow itself:** `sync-cicd-templates.yml` is included in future syncs, so improvements to it are automatically delivered. Add it to the exclusions file if you want to freeze your local version.

---

## ✅ Verification

After the initial sync completes, verify your repository structure:

```
cicd-intsuite/
├── .github/
│   └── workflows/
│       ├── sync-cicd-templates.yml
│       ├── btp-deploy-delete.yml
│       ├── btp-delete-from-btp-and-git.yml
│       ├── btp-download-git-upload-deploy.yml
│       ├── btp-download-to-git.yml
│       ├── btp-release-import.yml
│       ├── btp-update-externalized-iflow-parameters.yml
│       ├── btp-sync-partnerdirectory-to-eic.yml
│       ├── btp-download-access-policies-to-git.yml
│       ├── btp-download-upload-access-policies.yml
│       ├── btp-delete-upload-access-policies.yml
│       ├── btp-dashboard-generator.yml
│       └── git-create-release.yml
└── ... (integration artifacts added later by workflows)
```

All `uses:` references in the workflow files will point to `GIT_CICD_ORGREPO@GIT_CICD_REF`.
