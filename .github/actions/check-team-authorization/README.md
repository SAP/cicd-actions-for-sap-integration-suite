# 🔐 Check Team Authorization GitHub Action

Verifies if the workflow actor is a member of a specified GitHub team before proceeding with workflow execution.

---

## ✨ Overview

This action checks whether the user triggering the workflow is a member of a designated GitHub team within your organization. It supports auto-detection of the organization from the repository context and uses dual-method validation for robust team membership verification. Ideal for implementing role-based access control in your CI/CD pipelines and protecting sensitive workflows.

---

## ⚙️ Inputs

| Name          | Required | Description                                                            |
|---------------|----------|------------------------------------------------------------------------|
| team-slug     | ✅ Yes   | The GitHub team slug to check membership against.                      |
| github-token  | ✅ Yes   | GitHub token with `members:read` permission for API calls.             |
| organization  | ❌ No    | GitHub organization name. Auto-detects from repository if omitted.     |

---

## 📝 Usage Example

```yaml
jobs:
  protected-deployment:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Check Team Authorization
        uses: ./.github/actions/check-team-authorization
        with:
          team-slug: deployment-team
          github-token: ${{ secrets.GITHUB_TOKEN }}
          organization: my-org

      - name: Deploy Application
        run: |
          echo "User is authorized to deploy"
          # Your deployment commands here
```

---

## 📂 Outputs

| Name          | Description                                          |
|---------------|------------------------------------------------------|
| authorized    | Boolean string (`true` or `false`) indicating authorization status |
| user          | The GitHub username of the workflow actor             |
| organization  | The GitHub organization that was checked             |

**Using Outputs in Workflows:**
```yaml
jobs:
  check-access:
    runs-on: ubuntu-latest
    outputs:
      authorized: ${{ steps.auth.outputs.authorized }}
    steps:
      - name: Check Team Authorization
        id: auth
        uses: ./.github/actions/check-team-authorization
        with:
          team-slug: developers
          github-token: ${{ secrets.GITHUB_TOKEN }}

  deploy:
    needs: check-access
    if: needs.check-access.outputs.authorized == 'true'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Authorized user can proceed with deployment"
```

---

## 💡 Tips & Troubleshooting

- **Token Permissions**: Ensure your GitHub token has `members:read` permission to check team memberships. The default `GITHUB_TOKEN` in GitHub Actions typically includes this permission.
- **Auto-Detection**: If you don't specify an organization, the action automatically uses the repository owner. This works seamlessly for most workflows.
- **Team Slug Format**: Use the team slug (URL-safe identifier), not the team display name. For example, use `deployment-team` instead of "Deployment Team".
- **GitHub Enterprise Support**: The action detects your GitHub server URL and works with GitHub Enterprise instances. The hostname is automatically extracted from the server URL.
- **Dual Validation Method**: The action uses two approaches to verify membership: direct membership API first, then falls back to checking the team members list. This ensures compatibility with different GitHub configurations.
- **Access Denied**: If authorization fails, the action exits with code 1, which will stop workflow execution unless explicitly handled. Users receive clear instructions to contact their team administrator.
- **Conditional Workflows**: Combine this action with the `if` condition on subsequent jobs to create role-based workflow gates.
- **Logging**: The action provides timestamped, formatted output logs for audit trails and troubleshooting.

---

## 📄 License

This project is licensed under the Apache License 2.0.