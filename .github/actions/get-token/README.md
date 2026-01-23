# 🔐 Get OAuth Token GitHub Action

Request and retrieve an OAuth bearer token from SAP BTP for authenticating API calls in subsequent workflow steps.

---

## ✨ Overview

This action authenticates with the SAP BTP OAuth token endpoint using a two-credential authentication flow. It combines an API service account (client ID and secret) for basic authentication with a technical user's credentials (username and password) for the password grant type. The action returns a valid OAuth bearer token that can be used in subsequent API calls to SAP BTP Integration Suite and other services. This is typically the first action in CI/CD workflows that need to interact with BTP APIs.

---

## ⚙️ Inputs

| Name           | Required | Description                                                          |
|----------------|----------|----------------------------------------------------------------------|
| btp-api-user   | ✅ Yes   | BTP Service Key Client ID for basic authentication.                  |
| btp-tec-user   | ✅ Yes   | Technical user username with Integration Suite access permissions.   |
| btp-token-url  | ✅ Yes   | OAuth token endpoint URL (e.g., `https://tenant.authentication.sap.hana.ondemand.com/oauth/token`) |
| BTP_API_PASSWORD | ✅ Yes | Client Secret for the API user/service account.                      |
| BTP_TEC_PASSWORD | ✅ Yes | Password for the technical user.                                     |

---

## 📝 Usage Example

```yaml
jobs:
  authenticate-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Get OAuth Token
        id: auth
        uses: ./.github/actions/get-oauth-token
        with:
          btp-api-user: ${{ secrets.BTP_API_USER }}
          btp-tec-user: ${{ secrets.BTP_TEC_USER }}
          btp-token-url: ${{ secrets.BTP_TOKEN_URL }}
          BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
          BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}
      
      - name: Deploy Package
        uses: ./.github/actions/deploy-zip-to-cpi
        with:
          bearer-token: ${{ steps.auth.outputs.token }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          zip-location: my-package.zip

  get-token-and-export:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Authenticate with BTP
        id: oauth
        uses: ./.github/actions/get-oauth-token
        with:
          btp-api-user: ${{ secrets.BTP_API_USER }}
          btp-tec-user: ${{ secrets.BTP_TEC_USER }}
          btp-token-url: ${{ secrets.BTP_TOKEN_URL }}
          BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
          BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}
      
      - name: Export Integration Flows
        id: export
        uses: ./.github/actions/get-object-ids-of-package
        with:
          bearer-token: ${{ steps.oauth.outputs.token }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          object-type: Integration
      
      - name: Get Parameters
        uses: ./.github/actions/get-external-parameters
        with:
          bearer-token: ${{ steps.oauth.outputs.token }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          package-name: my-package
          file: ${{ steps.export.outputs.file }}

  multi-step-workflow:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Get Token
        id: token
        uses: ./.github/actions/get-oauth-token
        with:
          btp-api-user: ${{ secrets.BTP_API_USER }}
          btp-tec-user: ${{ secrets.BTP_TEC_USER }}
          btp-token-url: ${{ secrets.BTP_TOKEN_URL }}
          BTP_API_PASSWORD: ${{ secrets.BTP_API_PASSWORD }}
          BTP_TEC_PASSWORD: ${{ secrets.BTP_TEC_PASSWORD }}
      
      - name: Prepare Repository
        uses: ./.github/actions/prepare-repo
        with:
          bearer-token: ${{ steps.token.outputs.token }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          package-name: my-package
      
      - name: Download Package
        id: download
        uses: ./.github/actions/get-cpi-package-as-zip
        with:
          bearer-token: ${{ steps.token.outputs.token }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
          package-name: my-package
      
      - name: Extract Package
        uses: ./.github/actions/unzip-package-into-repo
        with:
          location-zip: ${{ steps.download.outputs.location }}
```

---

## 📂 Outputs

| Name  | Description                                    |
|-------|------------------------------------------------|
| token | OAuth bearer token for API authentication      |

**Output Format:**
The token is returned in the format `Bearer {access_token}`, ready to be used directly in HTTP Authorization headers.

Example: `Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImtleTEiLCJ0eXAiOiJKV1QifQ...`

---

## 💡 Tips & Troubleshooting

- **Credential Storage**: All credentials should be stored as GitHub secrets:
  - `BTP_API_USER`: Service account client ID
  - `BTP_API_PASSWORD`: Service account client secret
  - `BTP_TEC_USER`: Technical user username
  - `BTP_TEC_PASSWORD`: Technical user password
  - `BTP_TOKEN_URL`: OAuth token endpoint URL

- **Environment Variable Handling**: The action uses environment variables for credential handling to safely manage special characters (like `$` or `!`) that might cause shell interpretation issues. This is critical for credentials containing special characters.

- **Bearer Token Format**: The action automatically prepends `Bearer ` to the token. Pass the entire output directly to other actions without modification.

- **Token Lifetime**: OAuth tokens have limited lifetimes (typically 1-2 hours). For long-running workflows, you may need to request a new token mid-workflow if operations timeout.

- **OAuth Token Endpoint**: The token URL is specific to your BTP landscape. For SAP Cloud Platform, it typically follows the pattern: `https://{subdomain}.authentication.{region}.hana.ondemand.com/oauth/token`

- **Service Account Setup**: The API user (client ID) should be a service account created in the BTP subaccount with credentials (client secret) downloaded.

- **Technical User Permissions**: The technical user must have an IAM role or policy that grants access to Integration Suite services. Insufficient permissions will cause authentication failures.

- **HTTP 200 Response**: The action expects HTTP 200 for successful token retrieval. Any other status code (401, 403, 500, etc.) triggers an error.

- **Authentication Failures**: 
  - HTTP 401: Verify API user credentials (client ID/secret) are correct
  - HTTP 403: Verify technical user has sufficient permissions and is not locked
  - HTTP 400: Verify token endpoint URL is correct and token request parameters are valid

- **Missing Access Token**: If the response contains no `access_token` field or it's null, the action fails with a detailed error message showing the full response body for debugging.

- **Special Characters in Passwords**: The action uses environment variables and URL encoding to safely handle credentials with special characters. This prevents shell injection and interpretation issues.

- **Token Reuse**: You can reference the same token output in multiple subsequent actions within a single workflow run, avoiding redundant authentication calls.

- **Service Account vs Technical User**: This action uses a two-factor authentication approach:
  - API credentials (service account) for client authentication
  - Technical user credentials for user authentication with password grant type

- **Workflow Integration**: This action is typically the first step in CI/CD workflows, with its output token passed to all downstream actions that need BTP API access.

- **Error Diagnostics**: Failed authentication attempts display the full API response body in logs, which includes detailed error messages for troubleshooting.

- **Network Requirements**: Ensure the runner has network access to the BTP authentication/token endpoint. Firewall or network restrictions may cause connectivity errors.

---

## 📄 License

This project is licensed under the Apache License 2.0.