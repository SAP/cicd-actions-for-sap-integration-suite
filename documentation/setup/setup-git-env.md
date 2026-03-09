# Setup GIT Environment

After all necessary credentials have been created, the needed GIT environment configuration can be done. It is differentiated into 3 main areas:

- Organizational global variables & secrets
- Repository global variables & secrets
- Environment specific variables & secrets

Find below a section for each area that you need to setup in your repository:

- [Organizational Variables & Secrets](#organizational-variables--secrets)
- [Repository Global Variables & Secrets](#repository-global-variables--secrets)
- [Environment Specific Variables & Secrets](#environment-specific-variables--secrets)

## Organizational Variables & Secrets

Go to your organization → **Settings**

![GIT Env Settings](../img/GIT_Env_Settings.jpg)

And from there to → **Secrets and variables**

![GIT Env SecretsVariables](../img/GIT_Env_SecretsVariables.jpg)

Maintain the following variables and secrets:

| Type     | Name                | Value                                 |
|----------|---------------------|---------------------------------------|
| Variable | BTP_ADMIN_TEAM_SLUG | cicd_release_manager                  |
| Variable | BTP_DEV_TEAM_SLUG   | cicd_developer                        |
| Variable | GIT_CICD_ORGREPO    | \<yourorg>/\<cicd-actions>            |
| Variable | RUNS_ON             | JSON string of the runner, e.g. `"ubuntu-latest"` or `["self-hosted", "linux"]` |
| Secret   | GIT_CICD_TOKEN      | \<insertyourtoken>                    |
| Secret   | GIT_ORG_TOKEN       | \<insertyourtoken>                    |

> **Important:** The `RUNS_ON` value must be a valid **JSON** string. Use double quotes for a single runner (e.g. `"ubuntu-latest"`) or a JSON array for multiple labels (e.g. `["self-hosted", "linux"]`). A plain string without quotes (e.g. `ubuntu-latest`) will cause a workflow error.


## Repository Global Variables & Secrets

Currently no repository global variables or secrets required.

## Environment Specific Variables & Secrets

In your newly created repository `cicd-intsuite`, create 3 environments: **DEV**, **TST** and **PRD**.

![GIT Env NewEnv](../img/GIT_Env_NewEnv.jpg)

After creation:

![GIT Env Created](../img/GIT_Env_Created.jpg)

For each environment, maintain the specific variables & secrets as shown in the table below the screenshot:

![GIT Env ExampleDEV](../img/GIT_Env_ExampleDEV.jpg)

| Type     | Name             | Value                                            |
|----------|------------------|--------------------------------------------------|
| Variable | BTP_API_URL      | \<URL from service key JSON DEV>                 |
| Variable | BTP_API_USER     | \<clientid from service key JSON DEV>            |
| Variable | BTP_TEC_USER     | \<dev tec user> (leave empty if not needed)      |
| Variable | BTP_TOKEN_URL    | \<URL from service key JSON DEV>                 |
| Secret   | BTP_API_PASSWORD | \<clientsecret from service key JSON DEV>        |
| Secret   | BTP_TEC_PASSWORD | \<dev tec user password> (leave empty if not needed) |

### Customer Exit Variables (Optional)

If you want to use [Customer Exits](../usage/customer-exits.md), add the following **environment-specific** variables:

| Type     | Name                | Value                                                        |
|----------|---------------------|--------------------------------------------------------------|
| Variable | CX_IFLOW_EXCLUSIONS | `true` or `false` — activates the IFlow exclusions exit      |
| Variable | CX_REPOSITORY       | \<org/repo> — remote extension repository *(optional)*       |
| Variable | CX_REPOSITORY_REF   | \<branch or tag> — extension repo ref, defaults to `main` *(optional)* |

> **Note:** These variables are optional. If not set, customer exits are inactive and the standard deployment behavior applies. See the [Customer Exits documentation](../usage/customer-exits.md) for details.
