# Setup GIT Environment

> **Path A users: this is your core setup step.** If you are following the GitHub Apps path, start here — you can skip the token creation guides (steps 4 and 5).

After all necessary credentials have been created, the needed GIT environment configuration can be done. It is differentiated into 3 main areas:

- Organizational global variables & secrets
- Repository global variables & secrets
- Environment specific variables & secrets

Find below a section for each area that you need to setup in your repository:

- [Authentication](#authentication)
- [Organizational Variables & Secrets](#organizational-variables--secrets)
- [Repository Global Variables & Secrets](#repository-global-variables--secrets)
- [Environment Specific Variables & Secrets](#environment-specific-variables--secrets)

## Authentication

Workflows need GitHub credentials for two purposes:

- **CICD library access** — checkout of the central `cicd-actions` repository (cross-org, read-only)
- **Consumer repo operations** — PR management, branch operations, release tagging, team membership checks (write)

These two purposes are served by **two separate GitHub Apps** with different permission scopes. Keeping them separate ensures that credentials stored in consumer repos cannot be used to modify the central CICD codebase.

### Option A: GitHub Apps (Required for new installations)

> **The sync workflow and all new admin workflows only work with GitHub Apps.** Configure both apps below before running any workflow.

#### App 1 — CICD Reader (`cicd-actions-reader`)

Installed **only in the CICD central org** by the team that owns the `cicd-actions` repository. Its private key is stored in consumer repos but it can only read from the central CICD repo — a compromised consumer repo cannot push malicious code to the shared library.

Required permissions:

| Permission | Level | Needed For |
|-----------|-------|-----------|
| `Contents` | Repository — Read-only | Checkout of central CICD repo, template downloads |
| `Actions` | Repository — Read-only | Template file listing via contents API |

Add to your organization (or repository) **Variables**:

| Name | Value |
|------|-------|
| `GIT_CICD_APP_ID` | The numeric App ID of the CICD reader app (provided by the `cicd-actions` repo owner) |

Add to your organization (or repository) **Secrets**:

| Name | Value |
|------|-------|
| `GIT_CICD_APP_PRIVATE_KEY` | The PEM-encoded private key of the CICD reader app (provided by the `cicd-actions` repo owner) |

#### App 2 — Consumer Bot (`{your-org-name}-cicd-bot`)

Created and installed **only in your consumer org** by your team. Has write access to your consumer repo only.

> **Naming:** GitHub App names must be unique across the entire GitHub instance. Use the pattern `{your-org-name}-cicd-bot` (e.g. `my-org-cicd-bot`). The name is irrelevant to the workflows — only the numeric App ID stored in `GIT_GITHUB_APP_ID` matters at runtime.

**Suggested description:**
> Drives automated CI/CD operations in SAP Integration Suite consumer repositories. Issues short-lived, org-scoped installation tokens for branch management, pull request creation and merge, release tagging, workflow template sync, and team authorization checks. Grants write access to this consumer repo only — not to the central CICD library.

Required permissions:

| Permission | Level | Needed For |
|-----------|-------|-----------|
| `Contents` | Repository — Read & Write | Git push, branch create/delete, create releases |
| `Actions` | Repository — Read-only | List GitHub environments (`GET /repos/{owner}/{repo}/environments`) |
| `Environments` | Repository — Read-only | Read environment variables (`GET /environments/{env}/variables`) for dynamic dropdown population |
| `Workflows` | Repository — Read & Write | Push changes to `.github/workflows/` (template sync) |
| `Pull requests` | Repository — Read & Write | PR create, merge, close |
| `Members` | Organization — Read-only | Team membership check |

> **Note:** The `Actions: Read-only` permission is required to call the GitHub environments list API. The `Environments: Read-only` permission is required to read per-environment variables (used to determine which environments are fully configured for BTP). Despite appearances, GHES gates `GET /environments/{env}/variables` under the Environments permission — not Secrets or Actions.

Add to your organization (or repository) **Variables**:

| Name | Value |
|------|-------|
| `GIT_GITHUB_APP_ID` | The numeric App ID of your consumer bot app |

Add to your organization (or repository) **Secrets**:

| Name | Value |
|------|-------|
| `GIT_GITHUB_APP_PRIVATE_KEY` | The PEM-encoded private key of your consumer bot app |

> **Note on GHES:** `actions/create-github-app-token@v1` has known compatibility issues with some GitHub Enterprise Server configurations. If your workflows fail with GitHub App credentials on GHES, check your GHES version — App token support requires a sufficiently recent release. Falling back to PATs (Option B) is only viable if you have an existing installation; PATs do not support the sync workflow or new admin workflows and cannot serve as a workaround for new installations.

When both apps are configured, the PAT secrets (`GIT_CICD_TOKEN`, `GIT_ORG_TOKEN`, `GIT_SUITE_TOKEN`) become optional and can be removed.

### Option B: Personal Access Tokens (Backward compatibility only)

PATs continue to work **only for workflows that were already delivered and installed before the GitHub Apps migration**. The sync workflow and new admin workflows will not function with PATs alone.

Configure the PAT secrets listed in the sections below if you have an existing installation that has not yet migrated to GitHub Apps.

---

## Organizational Variables & Secrets

Go to your organization → **Settings**

![GIT Env Settings](../img/GIT_Env_Settings.jpg)

And from there to → **Secrets and variables**

![GIT Env SecretsVariables](../img/GIT_Env_SecretsVariables.jpg)

Maintain the following variables and secrets:

| Type     | Name                      | Value                                 |
|----------|---------------------------|---------------------------------------|
| Variable | BTP_ADMIN_TEAM_SLUG       | cicd_release_manager                  |
| Variable | BTP_DEV_TEAM_SLUG         | cicd_developer                        |
| Variable | GIT_CICD_APP_ID           | \<CICD reader App ID> (see [Authentication](#authentication)) |
| Variable | GIT_CICD_ORGREPO          | \<yourorg>/\<cicd-actions>            |
| Variable | GIT_GITHUB_APP_ID         | \<Consumer bot App ID> (see [Authentication](#authentication)) |
| Variable | RUNS_ON                   | JSON string of the runner, e.g. `"ubuntu-latest"` or `["self-hosted", "linux"]` |
| Secret   | GIT_CICD_APP_PRIVATE_KEY  | \<PEM private key of CICD reader app> (see [Authentication](#authentication)) |
| Secret   | GIT_CICD_TOKEN            | \<insertyourtoken> (optional when GitHub Apps are configured) |
| Secret   | GIT_GITHUB_APP_PRIVATE_KEY | \<PEM private key of consumer bot app> (see [Authentication](#authentication)) |
| Secret   | GIT_ORG_TOKEN             | \<insertyourtoken> (optional when GitHub Apps are configured) |

> **Important:** The `RUNS_ON` value must be a valid **JSON** string. Use double quotes for a single runner (e.g. `"ubuntu-latest"`) or a JSON array for multiple labels (e.g. `["self-hosted", "linux"]`). A plain string without quotes (e.g. `ubuntu-latest`) will cause a workflow error.


## Repository Global Variables & Secrets

Maintain the following secrets at the **repository level** (in your `cicd-intsuite` repository under Settings → Secrets and variables → Actions):

| Type     | Name              | Value              |
|----------|-------------------|--------------------|
| Variable | GIT_CICD_REF      | `v1` (or the tag/branch you want all `uses:` references to point to) |
| Variable | BTP_SET_LOG_LEVEL | `false` — set only if you want to **disable** the automatic log-level update after deployment. Omit or leave empty to keep the feature active. |
| Variable | BTP_EIC_URL_TEMPLATE | \<EIC API URL path template — not yet published, subject to change> (required when `BTP_EIC_RUNTIMES` is set in any environment) |
| Variable | PACKAGE_REGEX     | Regex to filter which Integration Packages are shown in the dashboard (e.g. `.*` for all, or `MyPackage.*` for a subset). Required by `btp-dashboard-generator.yml` — the workflow fails on startup if unset. |
| Secret   | GIT_SUITE_TOKEN   | \<insertyourtoken> (**Path B only** — not needed when GitHub Apps are configured) |

> **Note (Path B only):** `GIT_SUITE_TOKEN` is a fine-grained personal access token scoped to the `cicd-intsuite` repository with `contents:write` and `pull-requests:write` permissions. It is used by the **create-release** workflow for branch management, PR creation/merge, and release tagging operations when no GitHub App is configured. **Path A users can skip this entirely** — when `GIT_GITHUB_APP_ID` + `GIT_GITHUB_APP_PRIVATE_KEY` are configured, the App token is used and `GIT_SUITE_TOKEN` is not required.

> **Note on `BTP_SET_LOG_LEVEL`:** After each deployment, the workflows automatically set the IFlow log level to `ERROR` via an internal SAP API. This API is undocumented and may be changed or removed by SAP at any time. Set `BTP_SET_LOG_LEVEL=false` as a repository variable to disable this feature should the API become unavailable.

## Environment Specific Variables & Secrets

### Required environment names

The CI/CD pipeline workflows (`btp-download-git-upload-deploy.yml`, `btp-download-upload-access-policies.yml`, `btp-delete-from-btp-and-git.yml`) hardcode the environment names **`DEV`** and **`TST`**. These two environments **must exist with exactly these names** or those workflows will fail.

Additional environments (e.g. `PRD`, `POC`) can be created freely. They will appear automatically in all `target-env` and `source-env` dropdowns once they have the required BTP variables configured — no further changes needed.

> **Summary:** `DEV` and `TST` are mandatory. `PRD` and any other stages are optional and fully dynamic.

### Configure environment variables & secrets

In your `cicd-intsuite` repository, create the environments under **Settings → Environments**. Start with **DEV** and **TST** as a minimum.

![GIT Env NewEnv](../img/GIT_Env_NewEnv.jpg)

After creation:

![GIT Env Created](../img/GIT_Env_Created.jpg)

For each environment, maintain the specific variables & secrets as shown in the table below the screenshot:

![GIT Env ExampleDEV](../img/GIT_Env_ExampleDEV.jpg)

| Type     | Name             | Value                                            |
|----------|------------------|--------------------------------------------------|
| Variable | BTP_API_URL      | \<URL from service key JSON DEV>                 |
| Variable | BTP_API_USER     | \<clientid from service key JSON DEV>            |
| Variable | BTP_IS_URL       | \<Integration Suite web UI URL, e.g. `https://xxx.integrationsuite.cfapps.eu10.hana.ondemand.com`> (optional — enables clickable IFlow/package links in the dashboard) |
| Variable | BTP_TEC_USER     | \<dev tec user> (leave empty if not needed)      |
| Variable | BTP_TOKEN_URL    | \<URL from service key JSON DEV>                 |
| Variable | BTP_EIC_RUNTIMES | \<comma-separated EIC runtime IDs> (optional, see below) |
| Secret   | BTP_API_PASSWORD | \<clientsecret from service key JSON DEV>        |
| Secret   | BTP_TEC_PASSWORD | \<dev tec user password> (leave empty if not needed) |

> **Dashboard prerequisite:** If you intend to use the `btp-dashboard-generator.yml` workflow, you must enable GitHub Pages before the first run: go to your `cicd-intsuite` repository → **Settings** → **Pages** → set **Source** to **GitHub Actions**. Without this, the dashboard publish step will fail.

### Customer Exit Variables (Optional)

If you want to use [Customer Exits](../usage/customer-exits.md), add the following **environment-specific** variables:

| Type     | Name                | Value                                                        |
|----------|---------------------|--------------------------------------------------------------|
| Variable | CX_IFLOW_EXCLUSIONS | `true` or `false` — activates the IFlow exclusions exit      |
| Variable | CX_RUN_TESTS        | `true` or `false` — activates the test execution exit        |
| Variable | CX_REPOSITORY       | \<org/repo> — remote extension repository *(optional)*       |
| Variable | CX_REPOSITORY_REF   | \<branch or tag> — extension repo ref, defaults to `main` *(optional)* |

> **Note:** These variables are optional. If not set, customer exits are inactive and the standard deployment behavior applies. See the [Customer Exits documentation](../usage/customer-exits.md) for details.

### Edge Integration Cell (EIC) Support

If you have Edge Integration Cell (EIC) runtimes connected to your Cloud Integration tenant, you can configure the following variables to automatically sync Partner Directory entries to your EIC runtimes when deploying.

**Important:** One Cloud Integration tenant can have multiple EIC runtimes connected to it. Each EIC runtime is identified by a location identifier (e.g., `eicruntime01`, `deveiceur`).

**How it works:**
- When both `BTP_EIC_RUNTIMES` (environment variable) and `BTP_EIC_URL_TEMPLATE` (repository variable) are configured and Partner Directory entries are deployed to Cloud Integration, they will automatically be synced to all configured EIC runtimes.
- The EIC API URL path template is not yet published — subject to change. Configure `BTP_EIC_URL_TEMPLATE` when `BTP_EIC_RUNTIMES` is set.

**Example configuration:**
```
BTP_EIC_RUNTIMES=eicruntime01,deveiceur          # environment variable (per environment)
BTP_EIC_URL_TEMPLATE=<not yet published>          # repository variable (shared across environments)
```

This would sync Partner Directory entries to both the `eicruntime01` and `deveiceur` EIC runtimes.

**Note:** Leave `BTP_EIC_RUNTIMES` empty if you don't have EIC runtimes or don't want automatic syncing to EIC. Both `BTP_EIC_RUNTIMES` and `BTP_EIC_URL_TEMPLATE` must be set together — configuring only one will result in an error.

---

## 📘 Next: Usage Guides

See the [Usage Guide](../usage/README.md) for available guides and an overview of what's coming.

How-to blog posts covering common scenarios (downloading packages, deploying across environments, release management, Access Policies, dashboard setup) will be published on [blogs.sap.com](https://blogs.sap.com) and linked there once available.
