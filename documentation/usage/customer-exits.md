# 🔌 Customer Exits

Customer exits are extension points that allow you to inject custom logic into the CI/CD pipeline at predefined steps. They follow a **convention-based** approach where the framework automatically discovers and invokes your custom actions based on configuration and file location.

---

## 📋 Overview

The customer exit framework consists of three layers:

| Layer | Action | Purpose |
|-------|--------|---------|
| **Orchestrator** | `resolve-customer-exit` | Generic resolver that checks if a customer exit is active and determines where the action is located |
| **Caller** | `call-cx-<exit-name>` | Exit-specific caller that invokes the resolved action with the correct parameters |
| **Implementation** | `cx-<exit-name>` | Your custom action that contains the actual business logic |

### Resolution Order

When a customer exit is active, the framework searches for the implementation in this order:

1. **Intsuite repository** (your content repository) — `.github/actions/cx-<exit-name>/action.yml`
2. **Extension repository** (remote repository) — `.github/actions/cx-<exit-name>/action.yml`

> **Note:** The intsuite repository always takes precedence. If the action exists in both repositories, only the intsuite version is executed.

---

## 🔧 Available Customer Exits

### `cx-derive-iflow-exclusions`

**Purpose:** Derive a list of IFlow IDs that should be excluded from deployment during release import.

**When it runs:** During the `btp-release-import` workflow, after change analysis and before deployment execution.

**Output:** A comma-separated string of IFlow IDs to exclude (e.g., `IFlow_A,IFlow_B,IFlow_C`).

**Use case examples:**
- Exclude IFlows that are still under development in the target environment
- Exclude IFlows that require manual deployment steps
- Dynamically determine exclusions based on environment or other runtime conditions

---

## ⚙️ Configuration

### Environment Variables

Customer exits are controlled via **environment-specific variables** in your GitHub repository settings.

| Variable | Type | Description |
|----------|------|-------------|
| `CX_IFLOW_EXCLUSIONS` | `true` / `false` | Activates the `cx-derive-iflow-exclusions` customer exit |
| `CX_REPOSITORY` | `org/repo` | *(Optional)* Remote extension repository containing customer exit implementations |
| `CX_REPOSITORY_REF` | branch/tag | *(Optional)* Branch or tag of the extension repository. Defaults to `main` |

> **Tip:** Set these variables per environment (DEV, TST, PRD) to enable customer exits only where needed.

---

## 🚀 Implementing a Customer Exit

### Option A: In Your Intsuite Repository (Recommended)

Place your custom action directly in your intsuite (content) repository:

```
your-intsuite-repo/
├── .github/
│   └── actions/
│       └── cx-derive-iflow-exclusions/
│           └── action.yml          ← Your implementation
├── IntegrationPackages/
├── PartnerDirectory/
└── ...
```

### Option B: In a Remote Extension Repository

If you prefer to maintain customer exits in a separate repository:

1. Create a repository (e.g., `your-org/cicd-extensions`)
2. Place the action at `.github/actions/cx-derive-iflow-exclusions/action.yml`
3. Set the environment variables:
   - `CX_REPOSITORY` = `your-org/cicd-extensions`
   - `CX_REPOSITORY_REF` = `main` (or your desired branch/tag)

### Action Template

Below is a template for implementing the `cx-derive-iflow-exclusions` customer exit:

```yaml
name: 'Customer Exit - Derive IFlow Exclusions'
description: 'Custom logic to derive IFlow IDs to exclude from deployment'

inputs:
  target-env:
    description: 'Target BTP Environment (DEV/TST/PRD)'
    required: false
  base-ref:
    description: 'GIT Base Reference'
    required: false
  target-ref:
    description: 'GIT Target Reference'
    required: false
  perform-deploy:
    description: 'Whether deployment is being performed (true/false)'
    required: false
  btp-api-user:
    description: 'BTP API user'
    required: false
  btp-tec-user:
    description: 'BTP technical user'
    required: false
  btp-token-url:
    description: 'BTP token URL'
    required: false
  btp-api-url:
    description: 'BTP API URL'
    required: false
  git-cicd-orgrepo:
    description: 'CICD org/repo reference'
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
        # ╔════════════════════════════════════════════════════╗
        # ║ IMPLEMENT YOUR CUSTOM LOGIC HERE                  ║
        # ╚════════════════════════════════════════════════════╝
        #
        # Available inputs:
        #   ${{ inputs.target-env }}
        #   ${{ inputs.base-ref }}
        #   ${{ inputs.target-ref }}
        #   ${{ inputs.perform-deploy }}
        #   ${{ inputs.btp-api-user }}
        #   ${{ inputs.btp-tec-user }}
        #   ${{ inputs.btp-token-url }}
        #   ${{ inputs.btp-api-url }}
        #   ${{ inputs.git-cicd-orgrepo }}
        #
        # Output a comma-separated list of IFlow IDs:
        EXCLUDED=""
        echo "exclude-iflow-ids=$EXCLUDED" >> $GITHUB_OUTPUT
```

> **Important:** The action **must** output `exclude-iflow-ids`. Return an empty string if no IFlows should be excluded.

---

## 📊 Workflow Integration

The following diagram shows how the customer exit fits into the `btp-release-import` workflow:

```
┌──────────────┐
│  authorize   │
└──────┬───────┘
       │
┌──────▼────────┐
│ read-env-vars │
└──────┬────────┘
       │
┌──────▼───────────────┐
│  analyze-changes     │
└──────┬───────────────┘
       │
┌──────▼──────────────────────────┐
│ customer-exit-iflow-exclusions  │  ← Customer Exit
│   - Resolves action location    │
│   - Calls your implementation   │
│   - Returns exclude-iflow-ids   │
└──────┬──────────────────────────┘
       │
┌──────▼──────────────────┐
│ btp-execute-deployment  │
│   - Receives exclusions │
│     via exclude-iflow-ids│
└─────────────────────────┘
```

---

## 🔍 Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| Customer exit is not executed | `CX_IFLOW_EXCLUSIONS` is not set to `true` | Set the variable to `true` in the environment settings |
| "Action was not found" warning | Action file is missing or misnamed | Ensure file is at `.github/actions/cx-derive-iflow-exclusions/action.yml` |
| Extension repo not checked out | `CX_REPOSITORY` variable is empty | Set `CX_REPOSITORY` to `org/repo` format |
| Wrong branch of extension repo | `CX_REPOSITORY_REF` not set | Set `CX_REPOSITORY_REF` to the desired branch/tag |
| Exclusions not applied | Output name mismatch | Ensure your action outputs `exclude-iflow-ids` |

---

## 🏗️ Creating New Customer Exits

The framework is designed to be extensible. To add a new customer exit:

1. Create a new **caller action** in the cicd-actions repository at `.github/actions/call-cx-<exit-name>/action.yml`
2. Add a new **activation variable** (e.g., `CX_<EXIT_NAME>`) following the `CX_` prefix convention
3. Provide a **template action** at `.github/actions/cx-<exit-name>/action.yml` for customers to reference
4. Wire the caller into the appropriate workflow

The `resolve-customer-exit` orchestrator is generic and can be reused for any new exit by passing the `exit-action-name` parameter.