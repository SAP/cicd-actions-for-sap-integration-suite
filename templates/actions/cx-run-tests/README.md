# 🔌 Customer Exit Template - Run Tests

Template action for the `cx-run-tests` customer exit. Copy this to your own repository and implement your custom test logic.

---

## ✨ Overview

This is a **template/reference implementation** for the test execution customer exit. It demonstrates the expected interface (inputs and outputs) that the customer exit framework requires. The template file itself is a placeholder — the Gradle/Java example below is provided in this README as a starting point for your own implementation.

To use this customer exit, copy this action to your repository and replace the placeholder logic with your own test framework and assertions.

---

## 📦 Where to Place This Action

### Option A: In Your Intsuite Repository (Recommended)

```
your-intsuite-repo/
└── .github/
    └── actions/
        └── cx-run-tests/
            └── action.yml
```

### Option B: In a Remote Extension Repository

```
your-extension-repo/
└── .github/
    └── actions/
        └── cx-run-tests/
            └── action.yml
```

> **Note:** The intsuite repository takes precedence. If the action exists in both, only the intsuite version is executed. See [Customer Exits documentation](../../../documentation/usage/customer-exits.md) for details.

---

## ⚙️ Inputs

All inputs are provided automatically by the caller action (`call-cx-run-tests`). Use whichever inputs your custom logic requires.

| Name               | Required | Description                                            |
|--------------------|----------|--------------------------------------------------------|
| intsuite-repo-path | ❌ No    | Path where the integration suite repository is checked out |
| extension-repo-path| ❌ No    | Path where the extension repository is checked out (only when called from extension) |
| package-id         | ❌ No    | ID of the integration package to run tests for         |
| btp-api-url        | ❌ No    | URL of the BTP API                                     |
| bearer-token       | ❌ No    | Bearer token for authenticating against the BTP API    |
| mode               | ❌ No    | Mode of the package (e.g. `PartnerDirectory` or `IntegrationPackages`) |

---

## 📂 Outputs

| Name         | Description                                          |
|--------------|------------------------------------------------------|
| test-results | Results of the executed tests (format defined by your implementation) |

> **Tip:** Define a consistent format for your test results (e.g., JSON, plain text summary) so downstream steps can parse them if needed.

---

## 📝 Implementation Example

The included template uses **Gradle with Java 17** as an example test framework:

```yaml
name: 'CX Tests'
description: 'Customer exit tests for integration packages.'

inputs:
  package-id:
    description: 'Package ID being tested'
    required: false

outputs:
  test-results:
    description: 'Test execution results'
    value: ${{ steps.test.outputs.test-results }}

runs:
  using: 'composite'
  steps:
    - name: Setup Java
      uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: '17'

    - name: Setup Gradle
      uses: gradle/actions/setup-gradle@v4

    - name: Run Tests
      id: test
      shell: bash
      run: |
        echo "🧪 Running tests for package: ${{ inputs.package-id }}"
        gradle build -DbtpPackagePath=${{ github.workspace }}/btp-insuite
        echo "test-results=passed" >> $GITHUB_OUTPUT
```

You can replace this with any test framework — npm, pytest, Maven, shell scripts, or API-based validation.

---

## 🔧 Configuration

To activate this customer exit, set the following environment variable in your GitHub repository:

| Variable       | Value  | Description                              |
|----------------|--------|------------------------------------------|
| CX_RUN_TESTS   | `true` | Activates the test execution exit        |

For remote extension repositories, also set:

| Variable          | Value      | Description                          |
|-------------------|------------|--------------------------------------|
| CX_REPOSITORY     | `org/repo` | Extension repository                 |
| CX_REPOSITORY_REF | `main`     | Branch or tag to use                 |

---

## 💡 Tips

- **Use the package-id**: The caller provides the current package ID — use it to run package-specific tests or load package-specific test configurations.
- **Access BTP APIs**: The `bearer-token` and `btp-api-url` inputs allow your tests to call BTP APIs (e.g., to verify runtime artifacts, check deployment status, or validate configurations).
- **Access repository content**: Use `intsuite-repo-path` to access the checked-out integration packages and their content for file-based assertions.
- **Any test framework**: The template uses Gradle/Java, but you can use any language or framework — Node.js/Jest, Python/pytest, shell scripts, etc.
- **Return meaningful results**: Use the `test-results` output to communicate test outcomes to downstream workflow steps.

---

## 📄 License

This project is licensed under the Apache License 2.0.