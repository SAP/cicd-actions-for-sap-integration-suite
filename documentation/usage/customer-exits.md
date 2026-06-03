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

**When it runs:** During the `btp-release-import` workflow, inside each per-package deployment job. This ensures fresh exclusion data on every run, including job restarts.

**Output:** A comma-separated string of IFlow IDs to exclude (e.g., `IFlow_A,IFlow_B,IFlow_C`).

**Use case examples:**
- Exclude IFlows that are still under development in the target environment
- Exclude IFlows that require manual deployment steps
- Dynamically determine exclusions based on environment or other runtime conditions

### `cx-run-tests`

**Purpose:** Execute custom tests for integration packages after they have been downloaded from BTP.

**When it runs:** During the `download-btp-to-git` workflow, after each integration package is downloaded and before the Git commit.

**Output:** A `test-results` string containing the outcome of the test execution (format defined by your implementation).

**Available context:** The action receives `package-id`, `btp-api-url`, `bearer-token`, `mode`, and `intsuite-repo-path`. When the implementation lives in the extension repository, `extension-repo-path` is also passed. Use these to access the downloaded package content and the BTP runtime APIs.

**Use case examples:**
- Run automated validation tests against downloaded integration packages
- Verify IFlow configurations or mappings against expected values
- Execute API-based runtime checks (e.g., verify deployed artifacts match the downloaded content)
- Run linting or compliance checks on integration content

---

## ⚙️ Configuration

### Environment Variables

Customer exits are controlled via **environment-specific variables** in your GitHub repository settings.

| Variable | Type | Description |
|----------|------|-------------|
| `CX_IFLOW_EXCLUSIONS` | `true` / `false` | Activates the `cx-derive-iflow-exclusions` customer exit |
| `CX_RUN_TESTS` | `true` / `false` | Activates the `cx-run-tests` customer exit |
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
│       ├── cx-derive-iflow-exclusions/
│       │   └── action.yml          ← IFlow exclusions implementation
│       └── cx-run-tests/
│           └── action.yml          ← Test execution implementation
├── IntegrationPackages/
├── PartnerDirectory/
└── ...
```

### Option B: In a Remote Extension Repository

If you prefer to maintain customer exits in a separate repository:

1. Create a repository (e.g., `your-org/cicd-extensions`)
2. Place the action at `.github/actions/cx-<exit-name>/action.yml`
3. Set the environment variables:
   - `CX_REPOSITORY` = `your-org/cicd-extensions`
   - `CX_REPOSITORY_REF` = `main` (or your desired branch/tag)

### Action Template

Ready-to-use templates for both customer exits are provided in the [`templates/actions/`](../../templates/actions/) folder of this repository:

- [`templates/actions/cx-derive-iflow-exclusions/action.yml`](../../templates/actions/cx-derive-iflow-exclusions/action.yml)
- [`templates/actions/cx-run-tests/action.yml`](../../templates/actions/cx-run-tests/action.yml)

Copy the relevant file into your intsuite or extension repository at `.github/actions/<exit-name>/action.yml` and implement your custom logic where indicated.

> **Important:** The `cx-derive-iflow-exclusions` action **must** output `exclude-iflow-ids`. Return an empty string if no IFlows should be excluded. The `cx-run-tests` action **must** output `test-results`.

---

## 📊 Workflow Integration

The following diagram shows how the customer exit fits into the `btp-release-import` workflow:

```
┌──────────────┐
│  initialize  │
└──────┬───────┘
       │
┌──────▼───────────────┐
│  analyze-changes     │
└──────┬───────────────┘
       │
┌──────▼──────────────────────────────────────────┐
│ btp-execute-deployment (delete-upload.yml)       │
│                                                  │
│   ┌──────────────────────────────────────────┐   │
│   │ btp-update-runtime (per package matrix)  │   │
│   │                                          │   │
│   │  1. call-cx-derive-iflow-exclusions      │   │
│   │     ← Customer Exit (fresh per restart)  │   │
│   │                                          │   │
│   │  2. update-runtime                       │   │
│   │     → Receives exclude-iflow-ids         │   │
│   │     → add-iflows-for-deployment          │   │
│   │     → deploy-package-artifacts           │   │
│   └──────────────────────────────────────────┘   │
└──────────────────────────────────────────────────┘
```

> **Note:** The customer exit runs inside the deployment job (not as a separate preceding job). This means each per-package deployment gets fresh exclusion data, and job restarts re-execute the customer exit with current BTP state.

---

## 🔍 Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| Customer exit is not executed | Activation variable not set to `true` | Set `CX_IFLOW_EXCLUSIONS` or `CX_RUN_TESTS` to `true` in the environment settings |
| "Action was not found" warning | Action file is missing or misnamed | Ensure file is at `.github/actions/cx-<exit-name>/action.yml` |
| Action not found on target branch | Action exists on `main` but not on the checked-out branch | Merge `main` into the target branch or cherry-pick the action files |
| Extension repo not checked out | `CX_REPOSITORY` variable is empty | Set `CX_REPOSITORY` to `org/repo` format |
| Wrong branch of extension repo | `CX_REPOSITORY_REF` not set | Set `CX_REPOSITORY_REF` to the desired branch/tag |
| Exclusions not applied | Output name mismatch | Ensure your action outputs `exclude-iflow-ids` |
| Test results not returned | Output name mismatch | Ensure your action outputs `test-results` |

---

## 🏗️ Adding New Customer Exit Types

> **Note:** This section is for maintainers of the `cicd-actions` framework, not for customers implementing exits. Customers add their own logic inside the existing exit types described above.

The framework is designed to be extensible. To add a new customer exit type to the framework:

1. Create a new **caller action** in the cicd-actions repository at `.github/actions/call-cx-<exit-name>/action.yml`
2. Add a new **activation variable** (e.g., `CX_<EXIT_NAME>`) following the `CX_` prefix convention
3. Provide a **template action** at `templates/actions/cx-<exit-name>/action.yml` for customers to reference
4. Wire the caller into the appropriate workflow

The `resolve-customer-exit` orchestrator is generic and can be reused for any new exit by passing the `exit-action-name` parameter.