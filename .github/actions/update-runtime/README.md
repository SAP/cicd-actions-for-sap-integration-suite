# ⚡ Update Runtime from Design Time (Deploy / Undeploy) GitHub Action

Orchestrate multi-artifact deployment and undeployment of integration packages to SAP BTP Integration Suite runtime.

---

## ✨ Overview

This is a sophisticated composite orchestration action that manages the complete artifact deployment and undeployment lifecycle. It discovers all artifact types in a package (Integration Flows, Message Mappings, Script Collections, Value Mappings), collects their deployment configurations, builds a consolidated deployment task list, and executes the deployment or undeployment operation. The action intelligently handles both deployment (with optional iFlow configuration file override) and undeployment scenarios, providing comprehensive artifact lifecycle management in a single operation.

---

## ⚙️ Inputs

| Name             | Required | Description                                                                |
|------------------|----------|----------------------------------------------------------------------------|
| target-env       | ✅ Yes   | Target environment for parameter configuration (e.g., DEV, TST, PRD).     |
| source-ref       | ✅ Yes   | Git reference to checkout (branch name or tag).                           |
| package-id       | ✅ Yes   | The package ID to deploy or undeploy.                                     |
| mode             | ✅ Yes   | Operation mode: `deploy` or `undeploy`.                                   |
| iflow-deploy     | ❌ No    | Optional: `true` to use JSON configuration file for iFlow deployment, `false` otherwise |
| btp-api-user     | ✅ Yes   | BTP Service Key Client ID for OAuth authentication.                       |
| btp-tec-user     | ✅ Yes   | BTP technical user username with Integration Suite permissions.          |
| btp-token-url    | ✅ Yes   | OAuth token endpoint URL.                                                 |
| btp-api-url      | ✅ Yes   | Base URL for the SAP BTP Integration Suite APIs.                          |
| BTP_API_PASSWORD | ✅ Yes   | Client Secret for the API user/service account.                           |
| BTP_TEC_PASSWORD | ✅ Yes   | Password for the technical user.                                          |

---

## 📝 Usage Example

```yaml
jobs:
  deploy-all-artifacts:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy Package to Runtime
        uses: ./.github/actions/update-runtime-from-designtime
        with:
          target-env: DEV
          source-ref: develop
          package-id: my-package-001
          mode: deploy
          iflow-deploy: 'true'
          btp-api-user: ${{ secrets.BTP_API_USER }}
          btp-tec-user: ${{ secrets.BTP_TEC_USER }}
          btp-token-url: ${{ secrets.BTP_TOKEN_URL }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
          BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}

  undeploy-artifacts:
    runs-on: ubuntu-latest
    steps:
      - name: Undeploy Package from Runtime
        uses: ./.github/actions/update-runtime-from-designtime
        with:
          target-env: TST
          source-ref: main
          package-id: my-package-001
          mode: undeploy
          btp-api-user: ${{ secrets.BTP_API_USER }}
          btp-tec-user: ${{ secrets.BTP_TEC_USER }}
          btp-token-url: ${{ secrets.BTP_TOKEN_URL }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
          BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}

  promote-to-production:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy Release to Production
        uses: ./.github/actions/update-runtime-from-designtime
        with:
          target-env: PRD
          source-ref: v1.2.3
          package-id: my-package-001
          mode: deploy
          iflow-deploy: 'false'
          btp-api-user: ${{ secrets.BTP_PROD_API_USER }}
          btp-tec-user: ${{ secrets.BTP_PROD_TEC_USER }}
          btp-token-url: ${{ secrets.BTP_PROD_TOKEN_URL }}
          btp-api-url: ${{ secrets.BTP_PROD_API_URL }}
          BTP_API_PASSWORD: ${{ secrets.BTP_PROD_API_PASSWORD }}
          BTP_TEC_PASSWORD: ${{ secrets.BTP_PROD_TEC_PASSWORD }}

  multi-artifact-deployment:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy All Artifact Types
        uses: ./.github/actions/update-runtime-from-designtime
        with:
          target-env: TST
          source-ref: develop
          package-id: my-package-001
          mode: deploy
          iflow-deploy: 'true'
          btp-api-user: ${{ secrets.BTP_API_USER }}
          btp-tec-user: ${{ secrets.BTP_TEC_USER }}
          btp-token-url: ${{ secrets.BTP_TOKEN_URL }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
          BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}

  environment-promotion-chain:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Dev
        uses: ./.github/actions/update-runtime-from-designtime
        with:
          target-env: DEV
          source-ref: develop
          package-id: my-package-001
          mode: deploy
          iflow-deploy: 'true'
          btp-api-user: ${{ secrets.BTP_API_USER }}
          btp-tec-user: ${{ secrets.BTP_TEC_USER }}
          btp-token-url: ${{ secrets.BTP_TOKEN_URL }}
          btp-api-url: https://dev-tenant.it-cpitrial01.cfapps.sap.hana.ondemand.com
          BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
          BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}
      
      - name: Deploy to Test
        uses: ./.github/actions/update-runtime-from-designtime
        with:
          target-env: TST
          source-ref: main
          package-id: my-package-001
          mode: deploy
          iflow-deploy: 'true'
          btp-api-user: ${{ secrets.BTP_API_USER }}
          btp-tec-user: ${{ secrets.BTP_TEC_USER }}
          btp-token-url: ${{ secrets.BTP_TOKEN_URL }}
          btp-api-url: https://tst-tenant.it-cpitrial01.cfapps.sap.hana.ondemand.com
          BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
          BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}
      
      - name: Deploy to Production
        uses: ./.github/actions/update-runtime-from-designtime
        with:
          target-env: PRD
          source-ref: main
          package-id: my-package-001
          mode: deploy
          iflow-deploy: 'false'
          btp-api-user: ${{ secrets.BTP_API_USER }}
          btp-tec-user: ${{ secrets.BTP_TEC_USER }}
          btp-token-url: ${{ secrets.BTP_TOKEN_URL }}
          btp-api-url: https://prod-tenant.it-cpitrial01.cfapps.sap.hana.ondemand.com
          BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
          BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}
```

---

## 📂 Outputs

This action has no explicit outputs. It orchestrates multiple sub-actions to perform deployment operations.

**Operation Summary:**

**Deploy with iFlow Configuration:**
1. Checks out repository from specified Git reference
2. Authenticates with BTP OAuth
3. Discovers Integration Flows, Message Mappings, Script Collections, and Value Mappings
4. Reads iFlow deployment configuration from `Deployment_INTEGRATION_FLOW.json`
5. Merges all artifact IDs into consolidated deployment task
6. Validates deployment task file has content
7. Deploys all artifacts to runtime with environment-specific parameters

**Deploy without iFlow Configuration (Auto-Deploy):**
1-6. Same as above, but skips iFlow configuration file step and auto-deploys all discovered iFlows

**Undeploy:**
1. Checks out repository from specified Git reference
2. Authenticates with BTP OAuth
3. Discovers all artifact types using BTP APIs (ignores local configuration)
4. Merges all artifact IDs into consolidated undeployment task
5. Validates deployment task file has content
6. Undeploys all artifacts from runtime

---

## 💡 Tips & Troubleshooting

- **Operation Modes**: Choose between `deploy` or `undeploy`:
  - `deploy`: Deploys all discovered artifacts to runtime with optional configuration file control for iFlows
  - `undeploy`: Removes all discovered artifacts from runtime

- **iFlow Deployment Control**: The `iflow-deploy` parameter works differently based on mode:
  - Deploy mode: `true` = use `Deployment_INTEGRATION_FLOW.json` for selective iFlow deployment; `false` = auto-deploy all discovered iFlows
  - Undeploy mode: `iflow-deploy` is ignored; all discovered iFlows are included in undeploy

- **Multi-Artifact Types**: This action discovers and manages:
  - Integration Flows (iFlows)
  - Message Mappings
  - Script Collections
  - Value Mappings
  All artifact types are collected and deployed/undeployed together.

- **Orchestration Flow**: The action orchestrates these sub-actions in sequence:
  1. Git checkout
  2. OAuth token acquisition
  3. Get object IDs for each artifact type (4 parallel conceptually)
  4. Merge IDs into deployment tasks (4 calls)
  5. Add iFlows from configuration (if deploy with iflow-deploy=true)
  6. Validate deployment task file
  7. Deploy or undeploy artifacts

- **Configuration File**: For `iflow-deploy: 'true'` in deploy mode, the action looks for `Deployment_INTEGRATION_FLOW.json` in the package's Configuration directory. This file determines which iFlows are deployed.

- **No Configuration Scenario**: For `iflow-deploy: 'false'` in deploy mode or for undeploy mode, all discovered iFlows from BTP are automatically included.

- **Empty Artifact Sets**: If no artifacts of a certain type are found (e.g., no Script Collections), the action continues gracefully. An artifact type with zero items contributes nothing to the deployment task.

- **Deployment Task Validation**: Before execution, the action validates that:
  1. The deployment task file exists
  2. The file contains valid JSON
  3. The `deploytasks` array is not empty
  If validation fails, no deployment/undeployment occurs.

- **Git Reference**: The `source-ref` can be:
  - Branch name (e.g., `main`, `develop`)
  - Tag name (e.g., `v1.0.0`)
  - Commit SHA (full or abbreviated)
  Used for version-based and branch-based automated promotion

- **Environment-Specific Parameters**: The `target-env` is passed to iFlow deployment step and used for selecting parameter values from configuration files (if applicable).

- **Target Environment Naming**: Use consistent naming (DEV, TST, STAGING, PRD, PROD) matching your configuration structure and parameter files.

- **Multi-Tenancy Support**: Deploy to different BTP tenants by providing different API URLs and credentials for each target environment.

- **Token Expiration**: For workflows deploying to multiple environments sequentially, ensure OAuth token doesn't expire between operations.

- **Network Requirements**: Runner must have network access to:
  - Git repository (for checkout)
  - BTP token endpoint (for authentication)
  - BTP API URL (for artifact discovery and deployment)

- **Error Propagation**: If any sub-action fails (artifact discovery, ID merging, deployment), the orchestration stops and reports the error. Check logs for specific failure point.

- **Concurrent Artifact Discovery**: While the action sequentially calls each artifact type discovery step, BTP API handles the discovery in parallel for performance.

- **Partial Deployment**: If deployment fails for some artifacts but succeeds for others, the action continues. Check the deployment logs in BTP for which artifacts succeeded.

- **Idempotent Operation**: Deploying the same package multiple times is safe. Artifacts are replaced/updated, not duplicated.

- **Undeploy Verification**: After undeployment, artifacts are removed from the runtime. Verify in BTP console if needed.

- **Credential Security**: Store all credentials as GitHub secrets. Never hardcode credentials in workflow files.

- **Production Safety**: For production deployments, consider:
  - Using branch protection on main branch
  - Requiring approvals for production deployments
  - Testing in lower environments first (DEV → TST → PRD)

- **Monitoring and Logging**: The action provides detailed logs from each orchestrated step:
  - Git checkout confirmation
  - OAuth token acquisition
  - Artifact discovery results (IFlow count, Mapping count, etc.)
  - ID merging progress
  - Deployment task validation
  - Final deployment/undeployment execution logs

- **Debugging Failed Deployments**:
  1. Check Git checkout succeeded (correct reference)
  2. Verify OAuth token was acquired
  3. Confirm artifact discovery found expected types
  4. Validate deployment task file contains expected artifacts
  5. Check BTP API connectivity and permissions

- **Integration with Other Actions**: This composite action calls several documented sub-actions:
  - `get-oauth-token` - For authentication
  - `get-object-ids-of-package` - For artifact discovery
  - `merge-ids-for-deployment` - For ID consolidation
  - `add-iflows-for-deployment` - For iFlow configuration
  - `deploy-package-artifacts` - For actual deployment/undeployment

- **Selective Deployment**: To deploy only certain artifact types:
  - Modify the action locally to skip certain artifact discovery steps
  - Or use the JSON configuration file to exclude iFlows

- **Deployment Sequence**: Artifacts are deployed in the order they appear in the consolidated task file:
  1. All Message Mappings
  2. All Script Collections
  3. All Value Mappings
  4. All Integration Flows (if included)

- **Version-Based Deployments**: Use Git tags (e.g., `v1.2.3`) as `source-ref` for version-based release management and production deployments.

---

## 📄 License

This project is licensed under the Apache License 2.0.