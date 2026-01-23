# 📛 Get CPI Package Name GitHub Action

Retrieve the package name for a specific package ID from SAP BTP Integration Suite Design Time.

---

## ✨ Overview

This action queries the SAP BTP Integration Suite API to fetch package metadata and extracts the package name. It automatically normalizes the package name by replacing spaces with underscores, making it suitable for use as a filename or directory name in downstream operations. Useful for dynamic workflows where you have a package ID but need to discover the associated package name for display, logging, or file operations.

---

## ⚙️ Inputs

| Name         | Required | Description                                           |
|--------------|----------|-------------------------------------------------------|
| bearer-token | ✅ Yes   | Bearer token to authenticate with SAP BTP APIs.       |
| btp-api-url  | ✅ Yes   | Base URL for the SAP BTP Integration Suite APIs.      |
| package-id   | ✅ Yes   | The package ID to retrieve the name for.              |

---

## 📝 Usage Example

```yaml
jobs:
  discover-package-name:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Get Package Name
        id: get-name
        uses: ./.github/actions/get-package-name
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: my-package-001
      
      - name: Display Package Name
        run: |
          echo "Package name is: ${{ steps.get-name.outputs.name }}"

  dynamic-package-export:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Resolve Package Name from ID
        id: resolve
        uses: ./.github/actions/get-package-name
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: pkg-123-456
      
      - name: Export Package as ZIP
        uses: ./.github/actions/get-cpi-package-as-zip
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: pkg-123-456
          package-name: ${{ steps.resolve.outputs.name }}
      
      - name: Upload Backup
        uses: actions/upload-artifact@v3
        with:
          name: package-${{ steps.resolve.outputs.name }}
          path: ${{ runner.temp }}/pkg-123-456.zip

  multi-package-operations:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Get Names for Multiple Packages
        id: names
        run: |
          for pkg_id in pkg-001 pkg-002 pkg-003; do
            echo "Processing $pkg_id..."
          done
      
      - name: Get Package 1 Name
        id: pkg1
        uses: ./.github/actions/get-package-name
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: pkg-001
      
      - name: Get Package 2 Name
        id: pkg2
        uses: ./.github/actions/get-package-name
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: pkg-002
      
      - name: Get Package 3 Name
        id: pkg3
        uses: ./.github/actions/get-package-name
        with:
          bearer-token: ${{ secrets.BTP_BEARER_TOKEN }}
          btp-api-url: ${{ secrets.BTP_API_URL }}
          package-id: pkg-003
      
      - name: Generate Inventory Report
        run: |
          echo "=== Package Inventory ==="
          echo "pkg-001: ${{ steps.pkg1.outputs.name }}"
          echo "pkg-002: ${{ steps.pkg2.outputs.name }}"
          echo "pkg-003: ${{ steps.pkg3.outputs.name }}"
```

---

## 📂 Outputs

| Name | Description                                         |
|------|-----------------------------------------------------|
| name | The package name with spaces replaced by underscores |

**Output Format:**
The name is a string containing the normalized package name. Example: `my_integration_package`

**Normalization Details:**
- Original spaces are replaced with underscores (`_`)
- Suitable for use as filenames, directory names, or parameter values
- Other characters are preserved as returned from the API

**API Response Structure:**
The action extracts the Name field from the BTP API response:
```json
{
  "d": {
    "Id": "my-package-001",
    "Name": "my integration package",
    "Version": "1.0.0",
    "CreatedDate": "/Date(1640000000000)/",
    "ModifiedDate": "/Date(1640000000000)/"
  }
}
```

---

## 💡 Tips & Troubleshooting

- **Bearer Token**: Ensure your bearer token has read permissions for integration package metadata. Store as a GitHub secret and pass as `Bearer ${{ secrets.BTP_BEARER_TOKEN }}`.
- **Package ID**: Use the exact package ID from your BTP environment. IDs are typically alphanumeric strings.
- **HTTP 200 Response**: The action expects HTTP 200 for successful metadata retrieval. Any other status code triggers an error.
- **Authentication Failures**: If you receive HTTP 401, verify your bearer token is valid and not expired. Regenerate tokens in your BTP environment if needed.
- **Permission Issues**: If you receive HTTP 403, ensure your bearer token has read permissions for integration packages.
- **Package Not Found**: If you receive HTTP 404, verify the package ID is correct and the package exists in your BTP environment.
- **Null Package Name**: If the package exists but has no Name field or it's empty, the action fails with a clear error message. This indicates a data inconsistency in BTP.
- **Space Normalization**: All spaces in the package name are automatically replaced with underscores. This makes the output suitable for filenames and directory names. For example, "My Integration Package" becomes "My_Integration_Package".
- **Other Characters**: Characters other than spaces are preserved as-is from the API response. Special characters may be present in the output.
- **Dynamic Filename Generation**: Use the normalized output name for generating filenames or directory structures without manual manipulation.
- **API Endpoint**: The action queries the `IntegrationPackages` endpoint with the package ID as the primary key.
- **Idempotent Operation**: Running this action multiple times returns the same package name, making it safe for repeated calls.
- **Downstream Integration**: The package name can be passed to other actions like `get-cpi-package-as-zip` or `unzip-package-into-repo` for package-level operations.
- **Display and Logging**: Use this action to display human-readable package names in logs and reports when you only have package IDs.
- **Error Handling**: The action validates both HTTP response status and the presence of a valid Name field before returning results.
- **Package ID Format**: If you have a composite ID (package ID with version or other suffix), ensure you use only the base package ID without version information.

---

## 📄 License

This project is licensed under the Apache License 2.0.