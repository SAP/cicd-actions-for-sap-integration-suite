# 🚀 Create CSV of Changed Files GitHub Action

Creates CSV files listing IDs to be deleted and uploaded based on Git diff.

---

## ✨ Overview

This action processes Git diff output to identify which Integration Packages or Partner Directory entries have changed between two Git references. It generates two CSV files: one for deletions (items in base but not in target) and one for uploads (items that changed and need to be uploaded).

---

## ⚙️ Inputs

| Name            | Required | Description                                                                  |
|-----------------|----------|------------------------------------------------------------------------------|
| diff-filename   | ✅        | Path to file that contains diff from get-compare-file                       |
| base-dir-file   | ✅        | Path to file that contains directory structure of base reference            |
| target_dir_file | ✅        | Path to file that contains directory structure of target reference          |
| mode            | ✅        | Mode IntegrationPackages/PartnerDirectory                                    |

---

## 📝 Usage Example

```yaml
jobs:
  create-csv:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      - name: Get Git Diff
        id: diff
        uses: ./.github/actions/get-compare-file
        with:
          base-ref: 'main'
          target-ref: 'develop'
          mode: 'IntegrationPackages'
      - name: Create CSV Files
        id: csv
        uses: ./.github/actions/create-csv-of-changed-files
        with:
          diff-filename: ${{ steps.diff.outputs.files_changed }}
          base-dir-file: ${{ steps.diff.outputs.base_dir_file }}
          target_dir_file: ${{ steps.diff.outputs.target_dir_file }}
          mode: 'IntegrationPackages'
      - name: Display CSVs
        run: |
          echo "Upload: ${{ steps.csv.outputs.upload-csv }}"
          echo "Delete: ${{ steps.csv.outputs.delete-csv }}"
```

---

## 🪵 Example Logs

```
📁 Extracting unique directories from diff...
📁 Building JSON array of changed directories...
📁 Generated DELETE_CSV from missing package IDs
DELETE CSV: PARTNER001,PARTNER002
📁 Filtering upload IDs (excluding deleted IDs)...
UPLOAD CSV: PARTNER003,PARTNER004,PARTNER005
```
_These are example logs you may encounter when running this action. Actual logs may vary depending on configuration and runtime conditions._

---

## 📂 Outputs

| Name       | Description                                  |
|------------|----------------------------------------------|
| upload-csv | Comma-separated list of IDs to be uploaded  |
| delete-csv | Comma-separated list of IDs to be deleted   |

---

## 💡 Tips & Troubleshooting

- The action extracts unique second-level directory names from the diff file.
- Delete CSV contains IDs present in base but missing in target (deletions).
- Upload CSV contains IDs that changed, excluding those marked for deletion.
- The mode parameter determines whether to process IntegrationPackages or PartnerDirectory.
- IDs are extracted from directory names (the part after the `~` separator).
- Empty CSV files are handled gracefully.
- The action uses `set +e` to continue processing even if individual files are missing or empty.
- Both output CSV files are created in `${{ runner.temp }}`, which is cleaned up after the workflow completes.

---

## 📚 References

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/CLOUD_INTEGRATION)