# Reusable Workflows for SAP BTP Integration Suite CI/CD

> For the consumer-facing workflow reference (template workflows you copy into your repository), see [templates/README.md](../../templates/README.md).
> For project overview, see the main [README](../../README.md).

This folder contains the **reusable workflows** that are called by the template workflows in consuming repositories. They are not meant to be triggered directly — they are invoked via `uses:` references from consumer workflow templates.

---

## Available Workflows

| Workflow | Purpose |
|----------|---------|
| [analyze-changes.yml](#analyze-changesyml) | Compare two Git references and identify changed packages |
| [delete-upload.yml](#delete-uploadyml) | Deploy or delete integration packages and Partner Directory entries |
| [download-btp-to-git.yml](#download-btp-to-gityml) | Download integration content from BTP and commit to Git |
| [delete-dir-from-git.yml](#delete-dir-from-gityml) | Remove a package directory from the Git repository |
| [update-externalized-iflow-parameters.yml](#update-externalized-iflow-parametersyml) | Update externalized iFlow parameters and optionally deploy |
| [btp-download-access-policies-to-git.yml](#btp-download-access-policies-to-gityml) | Download Access Policies from BTP and commit to Git |
| [download-access-policies-to-git.yml](#download-access-policies-to-gityml) | Download Access Policies from a selected environment to a Git branch |
| [delete-upload-access-policies.yml](#delete-upload-access-policiesyml) | Upload or delete Access Policies in BTP |
| [sync-partnerdirectory-to-eic.yml](#sync-partnerdirectory-to-eicyml) | Sync Partner Directory entries to Edge Integration Cell runtimes |
| [create-release.yml](#create-releaseyml) | Create a release from the development branch |

---

## Authentication

All workflows support **GitHub Apps** (preferred) with PAT fallback for backward compatibility.

| Secret | Description |
|--------|-------------|
| `GIT_CICD_APP_PRIVATE_KEY` | PEM private key of the CICD reader app — preferred for `cicd-actions` checkout |
| `GIT_CICD_TOKEN` | PAT fallback for CICD repo access (backward compatibility only) |
| `GIT_GITHUB_APP_PRIVATE_KEY` | PEM private key of the consumer bot app — used for consumer repo operations |
| `GIT_SUITE_TOKEN` | PAT fallback for consumer repo operations (backward compatibility only) |

For setup details see [Setup GIT Environment](../../documentation/setup/setup-git-env.md).

---

## Workflow Reference

### analyze-changes.yml

Compares two Git references to identify changed integration packages and Partner Directory entries. Optionally triggers deployment of detected changes.

**Inputs**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `workflow-ref` | ✅ | Git reference to check out the cicd-actions repo from |
| `target-env` | ✅ | Target deployment environment |
| `base-ref` | ✅ | Base Git reference for comparison |
| `target-ref` | ✅ | Target Git reference for comparison |
| `perform-deploy` | ❌ | Deploy after analysis (`true`/`false`) |
| `btp-api-user` | ✅ | BTP OAuth client ID |
| `btp-tec-user` | ✅ | BTP technical username |
| `btp-token-url` | ✅ | BTP OAuth token URL |
| `btp-api-url` | ✅ | BTP API base URL |
| `git-cicd-orgrepo` | ✅ | CI/CD repository (`owner/repo`) |

**Secrets:** `BTP_API_PASSWORD`, `BTP_TEC_PASSWORD`, `GIT_CICD_APP_PRIVATE_KEY` (or `GIT_CICD_TOKEN`)

**Outputs:** `package_upload_csv_content`, `package_delete_csv_content`, `pid_upload_csv_content`, `pid_delete_csv_content`

---

### delete-upload.yml

Deploys or deletes integration packages and Partner Directory entries in BTP.

**Inputs**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `workflow-ref` | ✅ | Git reference to check out the cicd-actions repo from |
| `target-env` | ✅ | Target deployment environment |
| `source-ref` | ✅ | Git source reference containing the packages |
| `integrationpackages-upload-ids` | ❌ | Comma-separated package IDs to deploy |
| `integrationpackages-delete-ids` | ❌ | Comma-separated package IDs to delete |
| `partnerdirectory-upload-ids` | ❌ | Comma-separated Partner Directory IDs to deploy |
| `partnerdirectory-delete-ids` | ❌ | Comma-separated Partner Directory IDs to delete |
| `attach-zip-only` | ❌ | Attach package as workflow artifact ZIP without deploying to BTP (default: `false`) |
| `exclude-iflow-ids` | ❌ | Comma-separated iFlow IDs to exclude from deployment (manual override) |
| `base-ref` | ❌ | Base Git reference passed to the customer exit for context |
| `cx-iflow-exclusions` | ❌ | Run `cx-derive-iflow-exclusions` customer exit per deployment job (`true`/`false`) |
| `cx-repository` | ❌ | Remote extension repository for customer exits (`org/repo`) |
| `cx-repository-ref` | ❌ | Git ref of the extension repository (default: `main`) |
| `btp-eic-runtimes` | ❌ | Comma-separated EIC runtime IDs — syncs Partner Directory to EIC when set |
| `btp-eic-url-template` | ❌ | EIC API URL template (not yet published — required when `btp-eic-runtimes` is set) |
| `enable-set-log-level` | ❌ | Set MPL log level after deployment via undocumented API (default: `true`) |
| `btp-api-user` | ✅ | BTP OAuth client ID |
| `btp-tec-user` | ✅ | BTP technical username |
| `btp-token-url` | ✅ | BTP OAuth token URL |
| `btp-api-url` | ✅ | BTP API base URL |
| `git-cicd-orgrepo` | ✅ | CI/CD repository (`owner/repo`) |

**Secrets:** `BTP_API_PASSWORD`, `BTP_TEC_PASSWORD`, `GIT_CICD_APP_PRIVATE_KEY` (or `GIT_CICD_TOKEN`)

---

### download-btp-to-git.yml

Downloads integration packages or Partner Directory entries from BTP and commits them to a Git branch.

**Inputs**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `workflow-ref` | ✅ | Git reference to check out the cicd-actions repo from |
| `source-env` | ✅ | Source BTP environment to download from |
| `target-ref` | ✅ | Git branch to commit to |
| `ids` | ✅ | Comma-separated IDs to download |
| `mode` | ✅ | `IntegrationPackages` or `PartnerDirectory` |
| `commit-message` | ✅ | Commit message |
| `btp-api-user` | ✅ | BTP OAuth client ID |
| `btp-tec-user` | ✅ | BTP technical username |
| `btp-token-url` | ✅ | BTP OAuth token URL |
| `btp-api-url` | ✅ | BTP API base URL |
| `git-cicd-orgrepo` | ✅ | CI/CD repository (`owner/repo`) |

**Secrets:** `BTP_API_PASSWORD`, `BTP_TEC_PASSWORD`, `GIT_CICD_APP_PRIVATE_KEY` (or `GIT_CICD_TOKEN`)

---

### delete-dir-from-git.yml

Removes an integration package or Partner Directory folder from the Git repository.

**Inputs**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `workflow-ref` | ✅ | Git reference to check out the cicd-actions repo from |
| `id` | ✅ | ID of the package or directory to delete |
| `mode` | ✅ | `IntegrationPackages` or `PartnerDirectory` |
| `source-ref` | ✅ | Git branch to delete from |
| `commit-message` | ✅ | Commit message |
| `git-cicd-orgrepo` | ✅ | CI/CD repository (`owner/repo`) |

**Secrets:** `GIT_CICD_APP_PRIVATE_KEY` (or `GIT_CICD_TOKEN`)

---

### update-externalized-iflow-parameters.yml

Updates externalized parameters for a specific iFlow and optionally deploys it based on its deployment configuration.

**Inputs**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `workflow-ref` | ✅ | Git reference to check out the cicd-actions repo from |
| `target-env` | ✅ | Target environment |
| `iflow-id` | ✅ | iFlow ID to update |
| `evaluate-deployment` | ✅ | Evaluate `Deployment_*.json` and trigger deployment based on its configuration (`true`/`false`) |
| `source-ref` | ✅ | Git reference containing the parameter values |
| `enable-set-log-level` | ❌ | Set MPL log level after deployment via undocumented API (default: `true`) |
| `btp-api-user` | ✅ | BTP OAuth client ID |
| `btp-tec-user` | ✅ | BTP technical username |
| `btp-token-url` | ✅ | BTP OAuth token URL |
| `btp-api-url` | ✅ | BTP API base URL |
| `git-cicd-orgrepo` | ✅ | CI/CD repository (`owner/repo`) |

**Secrets:** `BTP_API_PASSWORD`, `BTP_TEC_PASSWORD`, `GIT_CICD_APP_PRIVATE_KEY` (or `GIT_CICD_TOKEN`)

---

### btp-download-access-policies-to-git.yml

Downloads one or more Access Policies and their artifact references from BTP and commits them to a Git branch. Called by the `btp-download-upload-access-policies` template workflow (DEV → TST flow).

**Inputs**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `workflow-ref` | ✅ | Git reference to check out the cicd-actions repo from |
| `source-env` | ✅ | Source BTP environment to download from |
| `target-ref` | ✅ | Git branch to commit to |
| `names` | ✅ | Comma-separated Access Policy names to download |
| `commit-message` | ✅ | Commit message |
| `btp-api-user` | ✅ | BTP OAuth client ID |
| `btp-tec-user` | ✅ | BTP technical username |
| `btp-token-url` | ✅ | BTP OAuth token URL |
| `btp-api-url` | ✅ | BTP API base URL |
| `git-cicd-orgrepo` | ✅ | CI/CD repository (`owner/repo`) |

**Secrets:** `BTP_API_PASSWORD`, `BTP_TEC_PASSWORD`, `GIT_CICD_APP_PRIVATE_KEY` (or `GIT_CICD_TOKEN`)

---

### download-access-policies-to-git.yml

Downloads Access Policies from a selected environment to a Git branch. Called by the `btp-download-access-policies-to-git` template workflow (free environment selection).

**Inputs**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `workflow-ref` | ✅ | Git reference to check out the cicd-actions repo from |
| `source-env` | ✅ | Source BTP environment to download from |
| `target-ref` | ✅ | Git branch to commit to |
| `names` | ✅ | Comma-separated Access Policy names to download |
| `commit-message` | ✅ | Commit message |
| `btp-api-user` | ✅ | BTP OAuth client ID |
| `btp-tec-user` | ✅ | BTP technical username |
| `btp-token-url` | ✅ | BTP OAuth token URL |
| `btp-api-url` | ✅ | BTP API base URL |
| `git-cicd-orgrepo` | ✅ | CI/CD repository (`owner/repo`) |

**Secrets:** `BTP_API_PASSWORD`, `BTP_TEC_PASSWORD`, `GIT_CICD_APP_PRIVATE_KEY` (or `GIT_CICD_TOKEN`)

---

### delete-upload-access-policies.yml

Uploads or deletes Access Policies in BTP. Upload always performs a delete-then-recreate to ensure a clean state.

**Inputs**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `workflow-ref` | ✅ | Git reference to check out the cicd-actions repo from |
| `target-env` | ✅ | Target environment |
| `source-ref` | ✅ | Git source reference containing the policy files |
| `accesspolicies-upload-names` | ❌ | Comma-separated Access Policy names to upload |
| `accesspolicies-delete-names` | ❌ | Comma-separated Access Policy names to delete |
| `btp-api-user` | ✅ | BTP OAuth client ID |
| `btp-tec-user` | ✅ | BTP technical username |
| `btp-token-url` | ✅ | BTP OAuth token URL |
| `btp-api-url` | ✅ | BTP API base URL |
| `git-cicd-orgrepo` | ✅ | CI/CD repository (`owner/repo`) |

**Secrets:** `BTP_API_PASSWORD`, `BTP_TEC_PASSWORD`, `GIT_CICD_APP_PRIVATE_KEY` (or `GIT_CICD_TOKEN`)

---

### sync-partnerdirectory-to-eic.yml

Syncs Partner Directory entries from a Cloud Integration environment directly to configured Edge Integration Cell runtimes — without storing data in Git.

**Inputs**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `workflow-ref` | ✅ | Git reference to check out the cicd-actions repo from |
| `target-env` | ✅ | Source Cloud Integration environment |
| `partnerdirectory-ids` | ✅ | Comma-separated Partner IDs to sync to EIC |
| `btp-eic-runtimes` | ✅ | Comma-separated EIC runtime identifiers |
| `btp-eic-url-template` | ❌ | EIC API URL template (not yet published — required when `btp-eic-runtimes` is set) |
| `btp-api-user` | ✅ | BTP OAuth client ID |
| `btp-tec-user` | ✅ | BTP technical username |
| `btp-token-url` | ✅ | BTP OAuth token URL |
| `btp-api-url` | ✅ | BTP API base URL |
| `git-cicd-orgrepo` | ✅ | CI/CD repository (`owner/repo`) |

**Secrets:** `BTP_API_PASSWORD`, `BTP_TEC_PASSWORD`, `GIT_CICD_APP_PRIVATE_KEY` (or `GIT_CICD_TOKEN`)

---

### create-release.yml

Creates a release from the development branch: squash-merges into main, creates a Git tag and GitHub release, then re-creates the development branch from main. Fully restart-safe. Supports a simulation mode to check merge feasibility without making changes.

**Inputs**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `workflow-ref` | ✅ | Git reference to check out the cicd-actions repo from |
| `release-name` | ✅ | Name/tag for the new release |
| `development-branch` | ❌ | Development branch name (default: `development`) |
| `main-branch` | ❌ | Main/production branch name (default: `main`) |
| `simulation` | ❌ | Check mergeability only, no changes made (default: `false`) |
| `git-cicd-orgrepo` | ✅ | CI/CD repository (`owner/repo`) |

**Secrets:** `GIT_CICD_APP_PRIVATE_KEY` (or `GIT_CICD_TOKEN`), `GIT_GITHUB_APP_PRIVATE_KEY` (or `GIT_SUITE_TOKEN`)
