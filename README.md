[![REUSE status](https://api.reuse.software/badge/github.com/SAP/cicd-actions-for-sap-integration-suite)](https://api.reuse.software/info/github.com/SAP/cicd-actions-for-sap-integration-suite) [![License: Apache-2.0](https://img.shields.io/badge/license-Apache%202-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

# CICD Actions for SAP Integration Suite

## About this project

This repository provides a GitHub Actions–based CI/CD control layer for SAP Integration Suite.

## Overview

- **Integration packages** and **Partner Directory IDs** are downloaded from SAP Integration Suite, extracted, and **stored in Git**  
- Git holds both the **content** and **configuration**:
  - Externalized parameter values for IFLOWs  
  - Deployment configuration for IFLOWs
- **GitHub Actions** orchestrate:
  - Synchronization between Design Time and Runtime  
  - Deployment of packages and Partner Directory content to DEV / TST / PRD  
  - Application of environment-specific configuration  
  - Calculate Release Import based on GIT Tags or Branches

All operations use **public Integration Suite APIs only**.

For more details on **initial setup** and **operations**, see the [detailed documentation](./documentation/README.md).

## Compatibility

Tested with GitHub Enterprise Cloud and GitHub Enterprise Server.

## Support, Feedback, Contributing

This project is open to feature requests/suggestions, bug reports etc. via [GitHub issues](https://github.com/SAP/cicd-actions-for-sap-integration-suite/issues). Contribution and feedback are encouraged and always welcome. For more information about how to contribute, the project structure, as well as additional contribution information, see our [Contribution Guidelines](CONTRIBUTING.md).

## Security / Disclosure
If you find any bug that may be a security problem, please follow our instructions at [in our security policy](https://github.com/SAP/cicd-actions-for-sap-integration-suite/security/policy) on how to report it. Please do not create GitHub issues for security-related doubts or problems.

## Code of Conduct

We as members, contributors, and leaders pledge to make participation in our community a harassment-free experience for everyone. By participating in this project, you agree to abide by its [Code of Conduct](https://github.com/SAP/.github/blob/main/CODE_OF_CONDUCT.md) at all times.

## Licensing

Copyright 2025 SAP SE or an SAP affiliate company and cicd-actions-for-sap-integration-suite contributors. Please see our [LICENSE](LICENSE) for copyright and license information. Detailed information including third-party components and their licensing/copyright information is available [via the REUSE tool](https://api.reuse.software/info/github.com/SAP/cicd-actions-for-sap-integration-suite).