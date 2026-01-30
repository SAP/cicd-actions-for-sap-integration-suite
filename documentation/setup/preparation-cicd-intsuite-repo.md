# Preparation of Target Repository

This guide explains how to prepare your target repository where SAP Integration Suite artifacts and partner directory entries will be stored and managed.

## 📁 Repository Setup

Create a new Git repository that will serve as the central storage for your integration design artifacts downloaded from SAP Integration Suite.

### Initial Setup

#### 1. Create Repository Structure

At the beginning, your repository only requires a single directory:

```
.github/workflows/
```

#### 2. Add GitHub Actions Workflows

Copy the example GitHub Action workflow files from the [cicd-actions-for-sap-integration-suite](https://github.com/SAP/cicd-actions-for-sap-integration-suite) repository:

1. Navigate to the `examples/` folder in the cicd-actions-for-sap-integration-suite repository
2. Copy the workflow YAML files to your repository's `.github/workflows/` directory
3. Customize the workflows according to your specific requirements and CI/CD strategy
   
   > ⚠️ **Important:** You must adapt the action paths in the workflow files to match your environment. Replace all references to `SAP/cicd-actions-for-sap-integration-suite@main` with your actual action repository location (e.g., `your-org/your-action-repo@main` or the appropriate branch/tag).

**Available Example Workflows:**
- `btp-download-to-git.yml` - Download artifacts from Integration Suite to Git
- `btp-deploy-delete.yml` - Deploy or delete artifacts in Integration Suite
- `btp-download-git-upload-deploy.yml` - Combined download, commit, and deploy workflow
- `btp-delete-from-btp-and-git.yml` - Remove artifacts from both systems
- `btp-release-import.yml` - Import release packages
- `btp-update-externalized-iflow-parameters.yml` - Update iFlow parameters

> **📝 Note:** No integration artifacts or configuration files are needed initially. These will be automatically added to your repository through the CI/CD automation process when you run the workflows.
