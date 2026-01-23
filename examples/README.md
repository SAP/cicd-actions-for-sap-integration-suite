<!-- SPDX-License-Identifier: MIT --->
# Examples for Wrapper Workflows

This folder contains example wrapper workflows for SAP Integration Suite CI/CD automation. Each workflow demonstrates how to use reusable workflows and can be adapted for your own repository.

## Usage Instructions

The YAML files in this folder contain **complete, working parameter structures**. You should:

1. **Copy the desired workflow file(s)** to a new empty repository's `.github/workflows/` directory.

2. **Configure GitHub Environments** (DEV, TST, PRD) with the required variables and secrets referenced in the workflows.

3. **Adjust workflow names and descriptions** to match your team's conventions and requirements.

4. **Modify the reusable workflow reference** (e.g., `SAP/cicd-actions-for-sap-integration-suite/.github/workflows/...@v1`) if you need to point to a different version or fork.

## Workflow Files & Parameter Explanations

### 1. btp-delete-from-btp-and-git.yml
Deletes a specified integration package or partner directory from BTP DEV/TST and Git.

**Workflow Inputs:**
- `id` (string, required): ID of the package or directory to delete.
- `mode` (choice, required): Select `IntegrationPackages` or `PartnerDirectory`.
- `commit-message` (string, required): JIRA Story or SNOW Incident reference.
- `delete` (string, required): Must be set to `DELETE` to confirm deletion.

**Required Variables:**
- `BTP_DEV_TEAM_SLUG` - GitHub team slug for authorization
- `BTP_API_USER` - BTP API username
- `BTP_TEC_USER` - BTP Technical user
- `BTP_TOKEN_URL` - BTP OAuth token URL
- `BTP_API_URL` - BTP API base URL
- `GIT_CICD_ORGREPO` - Git organization/repository reference

**Required Secrets:**
- `GIT_ORG_TOKEN` - GitHub organization token
- `BTP_API_PASSWORD` - BTP API password
- `BTP_TEC_PASSWORD` - BTP Technical user password
- `GIT_CICD_TOKEN` - Git CI/CD token

### 2. btp-deploy-delete.yml
Manages deployment, upload, and deletion of packages/directories across environments.

**Workflow Inputs:**
- `upload-ids` (string, optional): Comma-separated list of IDs to upload.
- `delete-ids` (string, optional): Comma-separated list of IDs to delete.
- `mode` (choice, required): `IntegrationPackages` or `PartnerDirectory`.
- `source-ref` (string, required): Git source reference (branch/tag).
- `target-env` (choice, optional): Target BTP environment (`PRD`, `TST`, `DEV`).

**Required Variables:**
- `BTP_ADMIN_TEAM_SLUG` - GitHub team slug for admin authorization
- `BTP_API_USER` - BTP API username
- `BTP_TEC_USER` - BTP Technical user
- `BTP_TOKEN_URL` - BTP OAuth token URL
- `BTP_API_URL` - BTP API base URL
- `GIT_CICD_ORGREPO` - Git organization/repository reference

**Required Secrets:**
- `GIT_ORG_TOKEN` - GitHub organization token
- `BTP_API_PASSWORD` - BTP API password
- `BTP_TEC_PASSWORD` - BTP Technical user password
- `GIT_CICD_TOKEN` - Git CI/CD token

### 3. btp-download-git-upload-deploy.yml
Downloads a package from BTP DEV to Git, then uploads and deploys to TST.

**Workflow Inputs:**
- `id` (string, required): ID of the package or directory.
- `mode` (choice, required): `IntegrationPackages` or `PartnerDirectory`.
- `commit-message` (string, required): JIRA Story or SNOW Incident reference.

**Required Variables:**
- `BTP_DEV_TEAM_SLUG` - GitHub team slug for authorization
- `BTP_API_USER` - BTP API username
- `BTP_TEC_USER` - BTP Technical user
- `BTP_TOKEN_URL` - BTP OAuth token URL
- `BTP_API_URL` - BTP API base URL
- `GIT_CICD_ORGREPO` - Git organization/repository reference

**Required Secrets:**
- `GIT_ORG_TOKEN` - GitHub organization token
- `BTP_API_PASSWORD` - BTP API password
- `BTP_TEC_PASSWORD` - BTP Technical user password
- `GIT_CICD_TOKEN` - Git CI/CD token

### 4. btp-download-to-git.yml
Downloads one or more packages from a BTP environment into a Git branch.

**Workflow Inputs:**
- `ids` (string, required): Comma-separated list of IDs to download.
- `source-env` (choice, required): Source BTP environment (`DEV`, `TST`, `PRD`).
- `mode` (choice, required): `IntegrationPackages` or `PartnerDirectory`.
- `commit-message` (string, required): JIRA Story or SNOW Incident reference.

**Required Variables:**
- `BTP_ADMIN_TEAM_SLUG` - GitHub team slug for admin authorization
- `BTP_API_USER` - BTP API username
- `BTP_TEC_USER` - BTP Technical user
- `BTP_TOKEN_URL` - BTP OAuth token URL
- `BTP_API_URL` - BTP API base URL
- `GIT_CICD_ORGREPO` - Git organization/repository reference

**Required Secrets:**
- `GIT_ORG_TOKEN` - GitHub organization token
- `BTP_API_PASSWORD` - BTP API password
- `BTP_TEC_PASSWORD` - BTP Technical user password
- `GIT_CICD_TOKEN` - Git CI/CD token

### 5. btp-release-import.yml
Manages release import and optional deployment between Git references and BTP environments.

**Workflow Inputs:**
- `base-ref` (string, required): Git base reference for comparison.
- `target-ref` (string, required): Git target reference for deployment.
- `perform-deploy` (choice, required): `true` or `false` to perform deployment after calculation.
- `target-env` (choice, optional): Target BTP environment (`PRD`, `TST`, `DEV`).

**Required Variables:**
- `BTP_ADMIN_TEAM_SLUG` - GitHub team slug for admin authorization
- `BTP_API_USER` - BTP API username
- `BTP_TEC_USER` - BTP Technical user
- `BTP_TOKEN_URL` - BTP OAuth token URL
- `BTP_API_URL` - BTP API base URL
- `GIT_CICD_ORGREPO` - Git organization/repository reference

**Required Secrets:**
- `GIT_ORG_TOKEN` - GitHub organization token
- `BTP_API_PASSWORD` - BTP API password
- `BTP_TEC_PASSWORD` - BTP Technical user password
- `GIT_CICD_TOKEN` - Git CI/CD token

### 6. btp-update-externalized-iflow-parameters.yml
Updates externalized parameters for a specific iFlow in DEV or TST, with optional deployment.

**Workflow Inputs:**
- `target-env` (choice, required): Target environment (`DEV`, `TST`).
- `iflow-id` (string, required): IFlow ID to update.
- `iflow-deploy` (choice, required): `true` or `false` to deploy after update.

**Required Variables:**
- `BTP_DEV_TEAM_SLUG` - GitHub team slug for authorization
- `BTP_API_USER` - BTP API username
- `BTP_TEC_USER` - BTP Technical user
- `BTP_TOKEN_URL` - BTP OAuth token URL
- `BTP_API_URL` - BTP API base URL
- `GIT_CICD_ORGREPO` - Git organization/repository reference

**Required Secrets:**
- `GIT_ORG_TOKEN` - GitHub organization token
- `BTP_API_PASSWORD` - BTP API password
- `BTP_TEC_PASSWORD` - BTP Technical user password
- `GIT_CICD_TOKEN` - Git CI/CD token

---

## Additional Notes

- All workflows include authorization checks against GitHub teams. Ensure your teams are configured correctly.
- Environment-specific variables and secrets must be set up in GitHub repository settings under Environments.
- Review and adjust the reusable workflow version tags (e.g., `@v1`) to match your requirements.
- For more details, see comments in each workflow file and refer to the main documentation. Place these workflows in your repository and adapt as needed for your CI/CD process.

---

## Variables & Secrets Configuration

This section provides a complete overview of all variables and secrets that need to be configured. Some are set **per environment** (DEV, TST, PRD), while others are set **globally** at the repository level.

### Environment-Specific Variables (per DEV, TST, PRD)

These variables must be configured in each GitHub Environment (Settings → Environments → [Environment Name] → Environment variables):

| Variable | Description |
|----------|-------------|
| `BTP_API_USER` | BTP API username for the specific environment |
| `BTP_TEC_USER` | BTP Technical user for the specific environment |
| `BTP_TOKEN_URL` | BTP OAuth token URL for the specific environment |
| `BTP_API_URL` | BTP API base URL for the specific environment |
| `BTP_DEV_TEAM_SLUG` | GitHub team slug for developer authorization |
| `BTP_ADMIN_TEAM_SLUG` | GitHub team slug for admin authorization |

### Environment-Specific Secrets (per DEV, TST, PRD)

These secrets must be configured in each GitHub Environment (Settings → Environments → [Environment Name] → Environment secrets):

| Secret | Description |
|--------|-------------|
| `BTP_API_PASSWORD` | Password for the BTP API user |
| `BTP_TEC_PASSWORD` | Password for the BTP Technical user |

### Repository-Level Variables (Global)

These variables are set once at the repository level (Settings → Secrets and variables → Actions → Variables):

| Variable | Description |
|----------|-------------|
| `GIT_CICD_ORGREPO` | Git organization/repository reference (e.g., `org-name/repo-name`) |

### Repository-Level Secrets (Global)

These secrets are set once at the repository level (Settings → Secrets and variables → Actions → Secrets):

| Secret | Description |
|--------|-------------|
| `GIT_ORG_TOKEN` | GitHub organization token for team authorization checks |
| `GIT_CICD_TOKEN` | Git CI/CD token for repository operations |

### Quick Setup Checklist

Use this checklist to ensure all required configuration is in place:

**For each environment (DEV, TST, PRD):**
- [ ] `BTP_API_USER` - Variable
- [ ] `BTP_TEC_USER` - Variable
- [ ] `BTP_TOKEN_URL` - Variable
- [ ] `BTP_API_URL` - Variable
- [ ] `BTP_DEV_TEAM_SLUG` - Variable (for dev workflows)
- [ ] `BTP_ADMIN_TEAM_SLUG` - Variable (for admin workflows)
- [ ] `BTP_API_PASSWORD` - Secret
- [ ] `BTP_TEC_PASSWORD` - Secret

**Repository-level (global):**
- [ ] `GIT_CICD_ORGREPO` - Variable
- [ ] `GIT_ORG_TOKEN` - Secret
- [ ] `GIT_CICD_TOKEN` - Secret