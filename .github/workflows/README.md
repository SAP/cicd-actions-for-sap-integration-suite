# Reusable GitHub Workflows for SAP BTP Integration Suite CI/CD

> **For a high-level project introduction and overview, see the main [README](../../README.md).**

## Table of Contents
- [Introduction](#introduction)
- [Quick Start](#quick-start)
- [Available Workflows](#available-workflows)
- [Prerequisites](#prerequisites)
- [Workflow Reference](#workflow-reference)
- [Common Parameters](#common-parameters)
- [Examples](#examples)

---

## Introduction

This repository provides **reusable GitHub Actions workflows** for automating SAP BTP Integration Suite CI/CD operations. These workflows enable you to:

- 📥 **Download** integration packages from BTP to Git
- 📤 **Deploy** integration packages to BTP environments
- 🗑️ **Delete** packages from BTP and Git
- 📊 **Analyze** changes between Git references
- ⚙️ **Update** externalized iFlow parameters

### Key Concepts

**Integration Package Management**
> The smallest entity managed by these workflows is the **integration package**. All operations (deploy, download, delete) are performed at the package level, which may contain one or more iFlows.

**Supported Content Types**
- **IntegrationPackages**: Standard integration packages containing iFlows
- **PartnerDirectory**: Partner directory entries for B2B integration

**Landscape Support**
- Supports multi-tier landscapes (Development, Test, Production)
- Each environment requires its own credentials and endpoints
- Use GitHub Environments to manage environment-specific configurations

---

## Quick Start

### 1. Set Up GitHub Environments

Create GitHub Environments in your repository (e.g., `DEV`, `TST`, `PRD`) and configure the following secrets:

| Secret | Description |
|--------|-------------|
| `BTP_API_USER` | BTP Service Key (ClientID) for OAuth token |
| `BTP_API_PASSWORD` | BTP Service Key password |
| `BTP_TEC_USER` | BTP technical user with Integration Suite access |
| `BTP_TEC_PASSWORD` | BTP technical user password |
| `BTP_TOKEN_URL` | OAuth token endpoint URL |
| `BTP_API_URL` | BTP Integration Suite API base URL |
| `GIT_CICD_TOKEN` | GitHub Personal Access Token for CI/CD operations |

### 2. Call Workflows from Your Repository

Reference the workflows in your `.github/workflows` directory:

```yaml
jobs:
  deploy:
    uses: <owner>/<this-repo>/.github/workflows/delete-upload.yml@main
    with:
      workflow-ref: 'main'
      target-env: 'DEV'
      source-ref: 'main'
      integrationpackages-upload-ids: 'MyPackageId1,MyPackageId2'
      # ... other parameters
    secrets:
      BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
      BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}
```

> **Tip:** See the [examples](../../examples/README.md) folder for complete workflow templates you can copy and customize.

---

## Available Workflows

| Workflow | Purpose |
|----------|---------|
| **analyze-changes.yml** | Analyze changes between two Git references and optionally deploy |
| **delete-upload.yml** | Deploy or delete integration packages and partner directory entries |
| **download-btp-to-git.yml** | Download integration content from BTP and commit to Git |
| **delete-dir-from-git.yml** | Remove a package directory from Git repository |
| **update-externalized-iflow-parameters.yml** | Update and deploy iFlow with new externalized parameters |

---

## Prerequisites

### Required Access
- ✅ GitHub repository with Actions enabled
- ✅ SAP BTP Integration Suite tenant
- ✅ BTP technical user with appropriate permissions
- ✅ OAuth service key for BTP API access

### Recommended Setup
- Use **GitHub Environments** for environment-specific configurations
- Name environments to match BTP landscape stages (e.g., `DEV`, `TST`, `PRD`)
- Store all credentials as GitHub secrets
- Use branch protection rules for production deployments

---

## Workflow Reference

### analyze-changes.yml

Compares two Git references (branches/tags) to identify changed integration packages and optionally deploys them.

**Use Case:** Release deployments, automated change detection

#### Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `workflow-ref` | ✅ | Git reference where workflow runs (e.g., `main`) |
| `target-env` | ✅ | Target environment (e.g., `DEV`, `TST`, `PRD`) |
| `base-ref` | ✅ | Base Git reference for comparison |
| `target-ref` | ✅ | Target Git reference for comparison |
| `perform-deploy` | ❌ | Deploy after analysis (`true`/`false`) |
| `btp-api-user` | ✅ | BTP OAuth client ID |
| `btp-tec-user` | ✅ | BTP technical username |
| `btp-token-url` | ✅ | BTP OAuth token URL |
| `btp-api-url` | ✅ | BTP API base URL |
| `git-cicd-orgrepo` | ✅ | CI/CD repository (`owner/repo`) |

#### Secrets
- `BTP_API_PASSWORD`
- `BTP_TEC_PASSWORD`
- `GIT_CICD_TOKEN`

#### Example
```yaml
jobs:
  analyze_and_deploy:
    uses: owner/mb-cicd-btp-insuite/.github/workflows/analyze-changes.yml@main
    with:
      workflow-ref: 'main'
      target-env: 'PRD'
      base-ref: 'v1.0.0'
      target-ref: 'v1.1.0'
      perform-deploy: 'true'
      btp-api-user: ${{ vars.BTP_API_USER }}
      btp-tec-user: ${{ vars.BTP_TEC_USER }}
      btp-token-url: ${{ vars.BTP_TOKEN_URL }}
      btp-api-url: ${{ vars.BTP_API_URL }}
      git-cicd-orgrepo: 'owner/mb-cicd-btp-insuite'
    secrets:
      BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
      BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}
      GIT_CICD_TOKEN: ${{ secrets.GIT_CICD_TOKEN }}
```

---

### delete-upload.yml

Deploys or deletes integration packages and partner directory entries in BTP.

**Use Case:** Manual/automated deployments, cleanup operations

#### Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `workflow-ref` | ✅ | Git reference where workflow runs |
| `target-env` | ✅ | Target environment |
| `source-ref` | ✅ | Git source reference containing packages |
| `integrationpackages-upload-ids` | ❌ | Comma-separated package IDs to deploy |
| `integrationpackages-delete-ids` | ❌ | Comma-separated package IDs to delete |
| `partnerdirectory-upload-ids` | ❌ | Comma-separated partner directory IDs to deploy |
| `partnerdirectory-delete-ids` | ❌ | Comma-separated partner directory IDs to delete |
| `btp-api-user` | ✅ | BTP OAuth client ID |
| `btp-tec-user` | ✅ | BTP technical username |
| `btp-token-url` | ✅ | BTP OAuth token URL |
| `btp-api-url` | ✅ | BTP API base URL |
| `git-cicd-orgrepo` | ✅ | CI/CD repository (`owner/repo`) |

#### Secrets
- `BTP_API_PASSWORD`
- `BTP_TEC_PASSWORD`
- `GIT_CICD_TOKEN`

#### Example
```yaml
jobs:
  deploy_packages:
    uses: owner/mb-cicd-btp-insuite/.github/workflows/delete-upload.yml@main
    with:
      workflow-ref: 'main'
      target-env: 'DEV'
      source-ref: 'develop'
      integrationpackages-upload-ids: 'Package1~ID1,Package2~ID2'
      integrationpackages-delete-ids: ''
      partnerdirectory-upload-ids: ''
      partnerdirectory-delete-ids: ''
      btp-api-user: ${{ vars.BTP_API_USER }}
      btp-tec-user: ${{ vars.BTP_TEC_USER }}
      btp-token-url: ${{ vars.BTP_TOKEN_URL }}
      btp-api-url: ${{ vars.BTP_API_URL }}
      git-cicd-orgrepo: 'owner/mb-cicd-btp-insuite'
    secrets:
      BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
      BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}
      GIT_CICD_TOKEN: ${{ secrets.GIT_CICD_TOKEN }}
```

---

### download-btp-to-git.yml

Downloads integration packages or partner directory entries from BTP and commits them to Git.

**Use Case:** Sync BTP content to Git, backup, initial repository setup

#### Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `workflow-ref` | ✅ | Git reference where workflow runs |
| `source-env` | ✅ | Source BTP environment to download from |
| `target-ref` | ✅ | Git branch to commit to |
| `ids` | ✅ | Comma-separated IDs to download |
| `mode` | ✅ | `IntegrationPackages` or `PartnerDirectory` |
| `commit-message` | ✅ | Commit message for Git |
| `btp-api-user` | ✅ | BTP OAuth client ID |
| `btp-tec-user` | ✅ | BTP technical username |
| `btp-token-url` | ✅ | BTP OAuth token URL |
| `btp-api-url` | ✅ | BTP API base URL |
| `git-cicd-orgrepo` | ✅ | CI/CD repository (`owner/repo`) |

#### Secrets
- `BTP_API_PASSWORD`
- `BTP_TEC_PASSWORD`
- `GIT_CICD_TOKEN`

#### Example
```yaml
jobs:
  download_from_btp:
    uses: owner/mb-cicd-btp-insuite/.github/workflows/download-btp-to-git.yml@main
    with:
      workflow-ref: 'main'
      source-env: 'DEV'
      target-ref: 'main'
      ids: 'MyPackage~PackageId'
      mode: 'IntegrationPackages'
      commit-message: 'Download MyPackage from DEV'
      btp-api-user: ${{ vars.BTP_API_USER }}
      btp-tec-user: ${{ vars.BTP_TEC_USER }}
      btp-token-url: ${{ vars.BTP_TOKEN_URL }}
      btp-api-url: ${{ vars.BTP_API_URL }}
      git-cicd-orgrepo: 'owner/mb-cicd-btp-insuite'
    secrets:
      BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
      BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}
      GIT_CICD_TOKEN: ${{ secrets.GIT_CICD_TOKEN }}
```

---

### delete-dir-from-git.yml

Removes an integration package or partner directory folder from the Git repository.

**Use Case:** Clean up obsolete packages, repository maintenance

#### Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `workflow-ref` | ✅ | Git reference where workflow runs |
| `id` | ✅ | ID of package/directory to delete |
| `mode` | ✅ | `IntegrationPackages` or `PartnerDirectory` |
| `source-ref` | ✅ | Git branch to delete from |
| `commit-message` | ✅ | Commit message for deletion |
| `git-cicd-orgrepo` | ✅ | CI/CD repository (`owner/repo`) |

#### Secrets
- `GIT_CICD_TOKEN`

#### Example
```yaml
jobs:
  delete_from_git:
    uses: owner/mb-cicd-btp-insuite/.github/workflows/delete-dir-from-git.yml@main
    with:
      workflow-ref: 'main'
      id: 'ObsoletePackage~PackageId'
      mode: 'IntegrationPackages'
      source-ref: 'main'
      commit-message: 'Remove obsolete package'
      git-cicd-orgrepo: 'owner/mb-cicd-btp-insuite'
    secrets:
      GIT_CICD_TOKEN: ${{ secrets.GIT_CICD_TOKEN }}
```

---

### update-externalized-iflow-parameters.yml

Updates externalized parameters for a specific iFlow and optionally deploys it.

**Use Case:** Update configuration parameters, environment-specific settings

#### Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `workflow-ref` | ✅ | Git reference where workflow runs |
| `target-env` | ✅ | Target environment |
| `iflow-id` | ✅ | iFlow ID to update |
| `iflow-deploy` | ✅ | Deploy after update (`true`/`false`) |
| `source-ref` | ✅ | Git reference with parameter values |
| `btp-api-user` | ✅ | BTP OAuth client ID |
| `btp-tec-user` | ✅ | BTP technical username |
| `btp-token-url` | ✅ | BTP OAuth token URL |
| `btp-api-url` | ✅ | BTP API base URL |
| `git-cicd-orgrepo` | ✅ | CI/CD repository (`owner/repo`) |

#### Secrets
- `BTP_API_PASSWORD`
- `BTP_TEC_PASSWORD`
- `GIT_CICD_TOKEN`

#### Example
```yaml
jobs:
  update_parameters:
    uses: owner/mb-cicd-btp-insuite/.github/workflows/update-externalized-iflow-parameters.yml@main
    with:
      workflow-ref: 'main'
      target-env: 'TST'
      iflow-id: 'MyIFlow'
      iflow-deploy: 'true'
      source-ref: 'main'
      btp-api-user: ${{ vars.BTP_API_USER }}
      btp-tec-user: ${{ vars.BTP_TEC_USER }}
      btp-token-url: ${{ vars.BTP_TOKEN_URL }}
      btp-api-url: ${{ vars.BTP_API_URL }}
      git-cicd-orgrepo: 'owner/mb-cicd-btp-insuite'
    secrets:
      BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
      BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}
      GIT_CICD_TOKEN: ${{ secrets.GIT_CICD_TOKEN }}
```

---

## Common Parameters

### BTP Credentials

**`btp-api-user`** & **`BTP_API_PASSWORD`**
- OAuth client credentials from BTP service key
- Used for API authentication

**`btp-tec-user`** & **`BTP_TEC_PASSWORD`**
- Technical user with Integration Suite access policies
- Used for content deployment operations

**`btp-token-url`**
- OAuth token endpoint from BTP service key
- Example: `https://<subdomain>.authentication.<region>.hana.ondemand.com/oauth/token`

**`btp-api-url`**
- Integration Suite API base URL
- Example: `https://<tenant>.it-cpi<region>.cfapps.<region>.hana.ondemand.com/api/v1`

### Git Parameters

**`git-cicd-orgrepo`**
- The CI/CD repository containing these workflows
- Format: `owner/repository-name`

**`GIT_CICD_TOKEN`**
- GitHub Personal Access Token with repository access
- Required permissions: `repo` scope

---

## Examples

For complete, ready-to-use workflow examples, see the [examples](../../examples/README.md) folder. It includes:

- **btp-deploy-manager.yml** - Comprehensive deployment orchestration
- **btp-download-packages-to-git.yml** - Batch download from BTP
- **btp-delete-package-from-btp-and-git.yml** - Complete cleanup workflow
- **btp-update-externalized-iflow-parameters.yml** - Parameter management

---

## Best Practices

### Security
- ✅ Always use GitHub Environments for environment-specific secrets
- ✅ Never hardcode credentials in workflow files
- ✅ Use branch protection rules for production environments
- ✅ Rotate credentials regularly

### Organization
- ✅ Use consistent naming for environments across BTP and GitHub
- ✅ Keep integration package IDs consistent between environments
- ✅ Use meaningful commit messages for traceability
- ✅ Tag releases for production deployments

### CI/CD Strategy
- ✅ Test in DEV before promoting to TST/PRD
- ✅ Use `analyze-changes.yml` for release deployments
- ✅ Implement approval gates for production deployments
- ✅ Monitor deployment logs and set up notifications

---

## Troubleshooting

### Common Issues

**Authentication Errors**
- Verify BTP credentials are correct and not expired
- Check token URL and API URL are correct for your BTP region
- Ensure technical user has necessary Integration Suite permissions

**Package Not Found**
- Verify package ID matches exactly (case-sensitive)
- Check the package exists in the source environment
- Ensure mode (`IntegrationPackages` or `PartnerDirectory`) is correct

**Git Errors**
- Verify `GIT_CICD_TOKEN` has sufficient permissions
- Check branch protection rules aren't blocking commits
- Ensure target branch exists

---

## Additional Resources

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/SAP_CLOUD_PLATFORM_INTEGRATION_SUITE)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Main Project README](../../README.md)
- [Example Workflows](../../examples/README.md)

---

**Questions or Issues?** Please refer to the main repository documentation or contact your SAP BTP administrator.