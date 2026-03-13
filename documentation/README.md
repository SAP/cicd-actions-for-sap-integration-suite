# 📚 Documentation

Welcome to the documentation for **CICD Actions for SAP Integration Suite**.

This guide will help you set up and use the GitHub Actions–based CI/CD control layer for SAP Integration Suite.

---

## 🚀 Quick Overview

This solution enables you to:

- 📦 Download **Integration packages** and **Partner Directory IDs** from SAP Integration Suite
- 🗃️ Store content and configuration in **Git**
- ⚙️ Orchestrate deployments across **DEV / TST / PRD** environments
- 🔄 Synchronize between Design Time and Runtime

---

## 📖 Table of Contents

| Section | Description |
|---------|-------------|
| [🔧 Setup](setup/README.md) | Installation and configuration instructions |
| [📘 Usage](usage/README.md) | How to use the workflows and actions |
| [🔌 Customer Exits](usage/customer-exits.md) | Extend the pipeline with custom logic |

---

## 🏗️ Setup Highlights

The setup process involves configuring two repositories:

1. **cicd-actions** — Contains the CI/CD action definitions
2. **cicd-intsuite** — Holds your Integration Suite content and workflows

Key setup steps include:
- Creating organizational teams and tokens
- Setting up service keys and technical users
- Configuring Git environments

➡️ [Get started with Setup](setup/README.md)

---

## 💡 Need Help?

- Check the [templates](../templates/README.md) folder for workflow templates
- Review the main [README](../README.md) for project overview