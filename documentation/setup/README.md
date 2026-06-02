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

## 🔐 Authentication Requirements

### ✅ Path A — GitHub Apps (Required for new installations)

The **sync workflow** (`sync-cicd-templates.yml`) and all **admin/new workflows** require GitHub Apps authentication. Without GitHub Apps configured, the sync workflow will fail on startup.

GitHub Apps issue short-lived installation tokens automatically — no manual rotation, no long-lived secrets stored in repositories.

**Steps to follow: 1 → 2 → 3 → 6 → 7 → 8**

> Skip steps 4 and 5 entirely — the two GitHub Apps replace both tokens.

### Path B — Personal Access Tokens (Backward compatibility only)

PATs continue to work **only for workflows that were already delivered and installed before the GitHub Apps migration**. They do not work with the sync workflow or any new admin workflows.

Use this path only if you have an existing installation and cannot yet migrate to GitHub Apps.

**Steps to follow: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8**

---

## 📖 Setup Guide

| Step | Guide | Description | Path |
|:----:|-------|-------------|------|
| 1️⃣ | [Setup CICD Actions Repository](preparation-cicd-actions-repo.md) | Configure the main actions repository | A + B |
| 2️⃣ | [Setup CICD IntSuite Repository](preparation-cicd-intsuite-repo.md) | Prepare your content repository | A + B |
| 3️⃣ | [Create Organizational Teams](create-organizational-teams.md) | Set up teams for access control | A + B |
| 4️⃣ | [Create Organizational Token](create-organizational-token.md) | Generate org-level PAT for team membership checks | **B only** *(backward compat)* |
| 5️⃣ | [Create CICD Token](create-cicd-token.md) | Create PAT for CICD repo access | **B only** *(backward compat)* |
| 6️⃣ | [Create Service Key](create-service-key.md) | Configure SAP BTP service key | A + B |
| 7️⃣ | [Create Technical User](create-technical-user.md) | Set up technical user credentials | A + B |
| 8️⃣ | [Setup GIT Environment](setup-git-env.md) | Configure variables, secrets, and GitHub Apps | A + B |

---

## 🎯 Next Steps

Once installation is complete, head over to the [📘 Usage Guide](../usage/README.md) to learn how to run workflows.
