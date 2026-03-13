# Templates

This folder contains templates for SAP Integration Suite CI/CD automation:

- **`workflows/`** — Workflow templates demonstrating how to use reusable workflows, adaptable for your own repository.
- **`actions/`** — Customer exit action templates that you can copy into your own repository and customize with your business logic.

---

# Workflow Templates

## Usage Instructions

The YAML files in the `workflows/` subfolder contain **complete, working parameter structures**. You should:

1. **Copy the desired workflow file(s)** from the `workflows/` subfolder to a new empty repository's `.github/workflows/` directory.

2. **Configure GitHub Environments and Variables** - Follow the setup guide in [`setup-git-env.md`](../documentation/setup/setup-git-env.md) for detailed instructions on configuring all required variables and secrets for DEV, TST, and PRD environments.

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

**Optional Variables (Customer Exits):**
- `CX_IFLOW_EXCLUSIONS` - Activates the IFlow exclusions customer exit (`true`/`false`)
- `CX_REPOSITORY` - Remote extension repository for customer exit implementations (`org/repo` format)
- `CX_REPOSITORY_REF` - Branch or tag of the extension repository (defaults to `main`)

For more details on customer exits, see the [Customer Exits documentation](../documentation/usage/customer-exits.md).

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

### 7. git-create-release.yml
Creates a new release from the `development` branch by squash-merging into `main`, tagging, and re-creating the development branch. The workflow is fully restart-safe — it detects the current state and resumes from where it left off.

**Workflow Flow:**
1. Validates that the release/tag does not already exist (or detects restart phase)
2. Renames `development` branch → `tmp/release-<release-name>`
3. Creates a PR from temp branch → `main` (or finds existing PR from previous run)
4. Checks PR mergeability — fails if there are conflicts (PR stays open for manual resolution and restart)
5. Squash-merges the PR into `main`
6. Creates a GitHub release with tag on `main`
7. Re-creates `development` branch from `main`
8. Deletes the temporary branch

**Simulation Mode:**

The workflow supports a **simulation mode** that allows you to verify whether the release merge would succeed **without making any changes** to your repository. This is useful for pre-release validation and conflict detection.

When `simulation` is set to `true`:
- A temporary PR is created directly from `development` → `main` (no branch rename)
- The PR mergeability is checked
- The PR is automatically closed after the check — **no merge, no tag, no branch modifications**
- The workflow summary reports one of the following results:
  - ✅ **simulation-ok** — Merge would succeed
  - ❌ **simulation-conflict** — Merge would fail due to conflicts
  - ℹ️ **no-changes** — No differences between `development` and `main`

This enables teams to safely verify that a release can be created before committing to the actual release process.

**Workflow Inputs:**
- `release-name` (string, required): Name/tag for the new release (e.g., `v1.0.0`).
- `simulation` (boolean, optional, default: `false`): Enable simulation mode — creates a PR to check mergeability but does not merge, tag, or delete branches.

**Required Variables:**
- `BTP_ADMIN_TEAM_SLUG` - GitHub team slug for admin authorization
- `GIT_CICD_ORGREPO` - Git organization/repository reference

**Required Secrets:**
- `GIT_SUITE_TOKEN` - GitHub token for the integration suite repository (needs `contents:write` and `pull-requests:write`)
- `GIT_ORG_TOKEN` - GitHub organization token (needed for team authorization in the initialize job)
- `GIT_CICD_TOKEN` - Git CI/CD token

**Restart Behavior:**
The workflow can be safely restarted at any point of failure:
- If the temp branch already exists, it skips the rename step
- If the PR already exists, it reuses it
- If the PR is already merged, it skips to release creation
- If the release already exists, it skips to development branch re-creation and cleanup
- If everything is already complete, it reports success without changes

---

## Additional Notes

- All workflows include authorization checks against GitHub teams. Ensure your teams are configured correctly.
- Environment-specific variables and secrets must be set up in GitHub repository settings under Environments.
- Review and adjust the reusable workflow version tags (e.g., `@v1`) to match your requirements.
- For detailed setup instructions, refer to [`setup-git-env.md`](../documentation/setup/setup-git-env.md).
- Place these workflows in your repository and adapt as needed for your CI/CD process.
