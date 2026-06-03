# Templates

This folder contains two types of templates:

- **`workflows/`** — Workflow templates for SAP Integration Suite CI/CD operations
- **`actions/`** — Customer exit action templates you can copy and customize with your own business logic

---

## How to Use These Workflows

There are two ways to use the workflow templates:

### Option A — Sync Workflow (Recommended)

The recommended approach is to use the **sync workflow** (`sync-cicd-templates.yml`). Copy only this one file into your repository's `.github/workflows/` directory. It will:

1. Pull all workflow templates from this central repository automatically
2. Substitute `GIT_CICD_ORGREPO` and `GIT_CICD_REF` into all `uses:` references
3. Populate environment dropdowns dynamically from your configured GitHub environments
4. Keep all templates up to date on a daily schedule
5. Allow you to install or remove workflow sets (scenarios) via dropdown inputs

Changes are committed and pushed **directly to your default branch** — no pull request is created.

For full setup instructions see the [Setup Guide](../documentation/setup/README.md) and the [Sync & Scenario documentation](../documentation/setup/preparation-cicd-intsuite-repo.md).

### Option B — Manual Copy

You can copy individual workflow files directly into your `.github/workflows/` directory and adapt them freely. In this case:

- You manage updates yourself — no automatic sync
- You can modify the workflows without risk of them being overwritten
- Do **not** run both Option A and Option B for the same workflow file — the sync will overwrite your customisations unless you add the filename to `.github/cicd-sync-exclusions.txt`

---

## Workflow Reference

All workflows require **GitHub Apps authentication** — see [Setup GIT Environment](../documentation/setup/setup-git-env.md). PAT-based secrets (`GIT_ORG_TOKEN`, `GIT_CICD_TOKEN`, `GIT_SUITE_TOKEN`) are supported for backward compatibility only.

All environment-specific variables (`BTP_API_URL`, `BTP_API_USER`, `BTP_TOKEN_URL`, `BTP_API_PASSWORD`, etc.) must be set in the corresponding **GitHub Environment** (DEV, TST, …). See [Environment Specific Variables & Secrets](../documentation/setup/setup-git-env.md#environment-specific-variables--secrets).

---

### sync-cicd-templates.yml

Pulls the latest workflow templates from the central CICD repository and pushes changes directly to the default branch. Manages scenario lifecycle (install/remove) and injects dynamic environment dropdowns.

**Trigger:** Manual (`workflow_dispatch`) or daily at 01:00 UTC

**Key inputs:**
- `source-ref` — ref to sync from (defaults to `GIT_CICD_REF`)
- `install-scenario` — add a scenario (workflow set) to the active list
- `remove-scenario` — remove a scenario from the active list

**Required variables:** `GIT_CICD_ORGREPO`, `GIT_CICD_REF`, `GIT_CICD_APP_ID`, `GIT_GITHUB_APP_ID`

---

### btp-download-git-upload-deploy.yml

Downloads an Integration Package or Partner Directory from **DEV**, stores it in Git, then uploads and deploys to **TST**.

**Key inputs:** `id`, `mode` (IntegrationPackages / PartnerDirectory), `commit-message`

**Required variables:** `BTP_DEV_TEAM_SLUG`, `BTP_API_USER`, `BTP_TEC_USER`, `BTP_TOKEN_URL`, `BTP_API_URL`, `GIT_CICD_ORGREPO`

---

### btp-deploy-delete.yml

Uploads or deletes Integration Packages or Partner Directory entries to a selected environment.

**Key inputs:** `upload-ids`, `delete-ids`, `mode`, `source-ref`, `target-env` *(dynamic dropdown)*, `attach-zip-only` *(optional — attaches the package as a workflow artifact ZIP without deploying it to BTP; defaults to `false`)*

**Required variables:** `BTP_ADMIN_TEAM_SLUG`, `BTP_API_USER`, `BTP_TEC_USER`, `BTP_TOKEN_URL`, `BTP_API_URL`, `GIT_CICD_ORGREPO`

**Optional:** `BTP_EIC_RUNTIMES` + `BTP_EIC_URL_TEMPLATE` — when set, Partner Directory entries are also synced to configured Edge Integration Cell runtimes after deployment.

---

### btp-delete-from-btp-and-git.yml

Deletes an Integration Package or Partner Directory entry from both BTP (DEV and TST) and Git.

**Key inputs:** `id`, `mode`, `commit-message`, `delete` (must be `DELETE` to confirm)

**Required variables:** `BTP_DEV_TEAM_SLUG`, `BTP_API_USER`, `BTP_TEC_USER`, `BTP_TOKEN_URL`, `BTP_API_URL`, `GIT_CICD_ORGREPO`

---

### btp-download-to-git.yml

Downloads one or more packages or Partner Directory IDs from a selected environment to a Git branch.

**Key inputs:** `ids`, `source-env` *(dynamic dropdown)*, `mode`, `commit-message`

**Required variables:** `BTP_ADMIN_TEAM_SLUG`, `BTP_API_USER`, `BTP_TEC_USER`, `BTP_TOKEN_URL`, `BTP_API_URL`, `GIT_CICD_ORGREPO`

---

### btp-release-import.yml

Calculates the delta between two Git references and optionally deploys changed packages to a selected environment.

**Key inputs:** `base-ref`, `target-ref`, `perform-deploy`, `target-env` *(dynamic dropdown)*

**Required variables:** `BTP_ADMIN_TEAM_SLUG`, `BTP_API_USER`, `BTP_TEC_USER`, `BTP_TOKEN_URL`, `BTP_API_URL`, `GIT_CICD_ORGREPO`

**Customer exits:** `CX_IFLOW_EXCLUSIONS`, `CX_REPOSITORY`, `CX_REPOSITORY_REF` — see [Customer Exits](../documentation/usage/customer-exits.md)

---

### btp-update-externalized-iflow-parameters.yml

Updates externalized parameters for a specific IFlow and optionally deploys it.

**Key inputs:** `target-env` *(dynamic dropdown)*, `iflow-id`, `evaluate-deployment`

**Required variables:** `BTP_DEV_TEAM_SLUG`, `BTP_API_USER`, `BTP_TEC_USER`, `BTP_TOKEN_URL`, `BTP_API_URL`, `GIT_CICD_ORGREPO`

---

### btp-sync-partnerdirectory-to-eic.yml

Syncs Partner Directory entries directly from a Cloud Integration environment to configured Edge Integration Cell runtimes — without storing data in Git.

**Key inputs:** `partner-ids`, `target-env` *(dynamic dropdown)*

**Required variables:** `BTP_ADMIN_TEAM_SLUG`, `BTP_API_USER`, `BTP_TOKEN_URL`, `BTP_API_URL`, `BTP_EIC_RUNTIMES` *(environment)*, `BTP_EIC_URL_TEMPLATE` *(repository)*, `GIT_CICD_ORGREPO`

---

### btp-download-access-policies-to-git.yml

Downloads one or more Access Policies from a selected BTP environment to a Git branch.

**Key inputs:** `names`, `source-env` *(dynamic dropdown)*, `commit-message`

**Required variables:** `BTP_ADMIN_TEAM_SLUG`, `BTP_API_USER`, `BTP_TEC_USER`, `BTP_TOKEN_URL`, `BTP_API_URL`, `GIT_CICD_ORGREPO`

---

### btp-download-upload-access-policies.yml

Downloads Access Policies from **DEV** to Git, then uploads them to **TST**.

**Key inputs:** `names`, `commit-message`

**Required variables:** `BTP_ADMIN_TEAM_SLUG`, `BTP_API_USER`, `BTP_TEC_USER`, `BTP_TOKEN_URL`, `BTP_API_URL`, `GIT_CICD_ORGREPO`

---

### btp-delete-upload-access-policies.yml

Uploads or deletes Access Policies in a selected environment.

**Key inputs:** `upload-names`, `delete-names`, `source-ref`, `target-env` *(dynamic dropdown)*

**Required variables:** `BTP_ADMIN_TEAM_SLUG`, `BTP_API_USER`, `BTP_TEC_USER`, `BTP_TOKEN_URL`, `BTP_API_URL`, `GIT_CICD_ORGREPO`

---

### btp-dashboard-generator.yml

Generates an HTML dashboard showing the status of all Integration Packages and IFlows across all configured environments. Published to GitHub Pages. Also produces a JSON data file suitable for Excel import.

**Trigger:** Manual or daily (00:00 UTC)

**Required variables:** `PACKAGE_REGEX`, `BTP_API_USER`, `BTP_TEC_USER`, `BTP_TOKEN_URL`, `BTP_API_URL`, `GIT_CICD_ORGREPO`, `GIT_CICD_APP_ID`, `GIT_GITHUB_APP_ID`

> GitHub Pages must be enabled (Settings → Pages → Source → GitHub Actions) before the first run.

---

### git-create-release.yml

Creates a release from the `development` branch: squash-merges into `main`, creates a Git tag and GitHub release, and re-creates the `development` branch from `main`. Fully restart-safe.

Supports a **simulation mode** (`simulation: true`) that checks merge feasibility without making any changes.

**Key inputs:** `release-name`, `simulation`

**Required variables:** `BTP_ADMIN_TEAM_SLUG`, `GIT_CICD_ORGREPO`

---

## Edge Integration Cell (EIC)

EIC support allows Partner Directory entries to be synced to on-premises or third-party cloud runtimes managed by SAP Integration Suite.

Configure per environment (`BTP_EIC_RUNTIMES`) and at repository level (`BTP_EIC_URL_TEMPLATE`):
```
BTP_EIC_RUNTIMES=eicruntime01,deveiceur       # environment variable (per environment)
BTP_EIC_URL_TEMPLATE=<not yet published>       # repository variable (shared across environments)
```

Relevant workflows: `btp-deploy-delete.yml`, `btp-sync-partnerdirectory-to-eic.yml`
