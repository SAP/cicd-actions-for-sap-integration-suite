# 🔌 Customer Exit Template - Derive IFlow Exclusions

Template action for the `cx-derive-iflow-exclusions` customer exit. Copy this to your own repository and implement your custom logic.

---

## ✨ Overview

This is a **template/reference implementation** for the IFlow exclusions customer exit. It demonstrates the expected interface (inputs and outputs) that the customer exit framework requires.

To use this customer exit, copy this action to your repository and replace the placeholder logic with your own business rules for determining which IFlows to exclude from deployment.

---

## 📦 Where to Place This Action

### Option A: In Your Intsuite Repository (Recommended)

```
your-intsuite-repo/
└── .github/
    └── actions/
        └── cx-derive-iflow-exclusions/
            └── action.yml
```

### Option B: In a Remote Extension Repository

```
your-extension-repo/
└── .github/
    └── actions/
        └── cx-derive-iflow-exclusions/
            └── action.yml
```

> **Note:** The intsuite repository takes precedence. If the action exists in both, only the intsuite version is executed. See [Customer Exits documentation](../../../documentation/usage/customer-exits.md) for details.

---

## ⚙️ Inputs

All inputs are provided automatically by the caller action (`call-cx-derive-iflow-exclusions`). Use whichever inputs your custom logic requires.

| Name             | Required | Description                                                      |
|------------------|----------|------------------------------------------------------------------|
| target-env       | ❌ No    | Target BTP Environment (DEV/TST/PRD)                             |
| base-ref         | ❌ No    | GIT Base Reference for comparison                                |
| target-ref       | ❌ No    | GIT Target Reference for deployment                              |
| perform-deploy   | ❌ No    | Whether deployment is being performed (`true`/`false`)           |
| btp-api-user     | ❌ No    | BTP Service Key (ClientID)                                       |
| btp-api-password | ❌ No    | BTP API password (Service Key client secret)                     |
| btp-tec-user     | ❌ No    | BTP technical user                                               |
| btp-tec-password | ❌ No    | BTP technical user password                                      |
| btp-token-url    | ❌ No    | URL on BTP to request Token                                      |
| btp-api-url      | ❌ No    | URL on BTP to access APIs                                        |
| git-cicd-orgrepo | ❌ No    | Remote GIT Org/Repo for CICD                                     |
| git-cicd-token   | ❌ No    | GitHub token for accessing private repositories                  |

---

## 📂 Outputs

| Name              | Description                                                              |
|-------------------|--------------------------------------------------------------------------|
| exclude-iflow-ids | **Required.** Comma-separated list of IFlow IDs to exclude from deployment |

> **Important:** This output is mandatory. Return an empty string if no IFlows should be excluded.

---

## 📝 Implementation Example

```yaml
name: 'Customer Exit - Derive IFlow Exclusions'
description: 'Custom logic to derive IFlow IDs to exclude from deployment'

inputs:
  target-env:
    description: 'Target BTP Environment'
    required: false
  base-ref:
    description: 'GIT Base Reference'
    required: false
  target-ref:
    description: 'GIT Target Reference'
    required: false

outputs:
  exclude-iflow-ids:
    description: 'Comma-separated list of IFlow IDs to exclude'
    value: ${{ steps.derive.outputs.exclude-iflow-ids }}

runs:
  using: 'composite'
  steps:
    - name: Derive IFlow Exclusions
      id: derive
      shell: bash
      run: |
        TARGET_ENV="${{ inputs.target-env }}"
        
        # Example: Exclude specific IFlows for PRD
        if [ "$TARGET_ENV" == "PRD" ]; then
          EXCLUDED="IFlow_UnderDevelopment,IFlow_ManualDeploy"
        else
          EXCLUDED=""
        fi
        
        echo "exclude-iflow-ids=$EXCLUDED" >> $GITHUB_OUTPUT
```

---

## 🔧 Configuration

To activate this customer exit, set the following environment variable in your GitHub repository:

| Variable            | Value  | Description                           |
|---------------------|--------|---------------------------------------|
| CX_IFLOW_EXCLUSIONS | `true` | Activates the IFlow exclusions exit   |

For remote extension repositories, also set:

| Variable           | Value          | Description                            |
|--------------------|----------------|----------------------------------------|
| CX_REPOSITORY      | `org/repo`     | Extension repository                   |
| CX_REPOSITORY_REF  | `main`         | Branch or tag to use                   |

---

## 💡 Tips

- **Keep it simple**: Start with a static list and evolve to dynamic logic as needed.
- **Use inputs**: The caller provides full context (environment, refs, BTP credentials) — use them to make environment-aware decisions.
- **Test locally**: The action is a standard composite action. You can test the shell logic independently.
- **Return empty for no exclusions**: If your logic determines nothing should be excluded, output an empty string.

---

## 📄 License

This project is licensed under the Apache License 2.0.