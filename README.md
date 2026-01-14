[![REUSE status](https://api.reuse.software/badge/github.com/SAP/cicd-actions-for-sap-integration-suite)](https://api.reuse.software/info/github.com/SAP/cicd-actions-for-sap-integration-suite)

# cicd-actions-for-sap-integration-suite

## About this project

An open-source solution leveraging GitHub Actions to automate deployment for SAP Integration Suite. It standardizes CI/CD processes, supports package management, parameter updates, and one-click release imports, ensuring consistent and efficient integration across environments

🛠️ Requirements and Setup
This repository provides GitHub Actions–based CI/CD automation for SAP BTP Integration Suite.
Below are the prerequisites and high‑level steps required to get started.


## ⚙️ Requirements

To use the GitHub‑Actions–based CI/CD automation for **SAP BTP Integration Suite**, ensure the following prerequisites are in place:

### 📁 GitHub Repository Structure
Your repository should contain:
- **Integration artifacts** exported from SAP Integration Suite (Design Time)
- **Configuration files** (e.g., externalized parameters per environment)
- **GitHub Actions workflows** located under:
  ```
  .github/workflows/
  ```

### 🌐 Access to SAP BTP Integration Suite APIs
The CI/CD pipelines use **publicly documented APIs** of the Integration Suite for:
- Package download & upload
- Synchronization of Design Time ↔ Runtime
- Deployment of releases
- Updating external parameters

Ensure that:
- API access is enabled
- Required roles/permissions are assigned

### ⚡ GitHub Actions Enabled
The repository must allow:
- Running GitHub Actions
- Using reusable workflows
- Accessing GitHub Environments (optional but recommended)

### 🔐 Required Service Credentials
Add the following secrets under `Settings → Secrets and variables → Actions`:

| Secret Name          | Purpose                                  |
|----------------------|-------------------------------------------|
| `BTP_HOST`           | Base URL of the Integration Suite API     |
| `BTP_CLIENT_ID`      | OAuth client ID for API authentication    |
| `BTP_CLIENT_SECRET`  | OAuth client secret for API authentication |

### 🧩 Optional (Recommended)
- Separate GitHub environments (`dev`, `qa`, `prod`)
- Branch protection rules
- Environment-specific parameter files (e.g., `parameters-dev.json`)

## Support, Feedback, Contributing

This project is open to feature requests/suggestions, bug reports etc. via [GitHub issues](https://github.com/SAP/cicd-actions-for-sap-integration-suite/issues). Contribution and feedback are encouraged and always welcome. For more information about how to contribute, the project structure, as well as additional contribution information, see our [Contribution Guidelines](CONTRIBUTING.md).

## Security / Disclosure
If you find any bug that may be a security problem, please follow our instructions at [in our security policy](https://github.com/SAP/cicd-actions-for-sap-integration-suite/security/policy) on how to report it. Please do not create GitHub issues for security-related doubts or problems.

## Code of Conduct

We as members, contributors, and leaders pledge to make participation in our community a harassment-free experience for everyone. By participating in this project, you agree to abide by its [Code of Conduct](https://github.com/SAP/.github/blob/main/CODE_OF_CONDUCT.md) at all times.

## Licensing

Copyright 2025 SAP SE or an SAP affiliate company and cicd-actions-for-sap-integration-suite contributors. Please see our [LICENSE](LICENSE) for copyright and license information. Detailed information including third-party components and their licensing/copyright information is available [via the REUSE tool](https://api.reuse.software/info/github.com/SAP/cicd-actions-for-sap-integration-suite).
