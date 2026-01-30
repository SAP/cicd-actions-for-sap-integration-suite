# 🔧 Installation

Welcome to the setup guide for **CICD Actions for SAP Integration Suite**.

This section covers the complete installation process to get you up and running.

---

## 📋 Prerequisites

You will need **two repositories** on the same GitHub Enterprise instance:

| Repository | Purpose |
|------------|---------|
| **cicd-actions** | Contains the CI/CD action definitions and reusable workflows |
| **cicd-intsuite** | Holds your Integration Suite packages, Partner Directory IDs, and executable workflows |

---

## 📖 Setup Guide

Follow these steps in order to complete the installation:

| Step | Guide | Description |
|:----:|-------|-------------|
| 1️⃣ | [Setup CICD Actions Repository](preparation-cicd-actions-repo.md) | Configure the main actions repository |
| 2️⃣ | [Setup CICD IntSuite Repository](preparation-cicd-intsuite-repo.md) | Prepare your content repository |
| 3️⃣ | [Create Organizational Teams](create-organizational-teams.md) | Set up teams for access control |
| 4️⃣ | [Create Organizational Token](create-organizational-token.md) | Generate org-level authentication |
| 5️⃣ | [Create CICD Token](create-cicd-token.md) | Create workflow authentication token |
| 6️⃣ | [Create Service Key](create-service-key.md) | Configure SAP BTP service key |
| 7️⃣ | [Create Technical User](create-technical-user.md) | Set up technical user credentials |
| 8️⃣ | [Setup GIT Environment](setup-git-env.md) | Set up GIT Environment |

---

## 🎯 Next Steps

Once installation is complete, head over to the [📘 Usage Guide](../usage/README.md) to learn how to run workflows.