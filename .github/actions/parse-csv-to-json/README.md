# 🚀 Parse CSV to JSON Arrays GitHub Action

Parses comma-separated strings, filters duplicates, and returns JSON arrays for deployment orchestration.

---

## ✨ Overview

This action converts comma-separated ID strings into JSON arrays, removes duplicates, and filters the delete list to exclude IDs that are also in the upload list. This is crucial for deployment orchestration to prevent conflicts where an ID would be both deleted and uploaded.

---

## ⚙️ Inputs

| Name                | Required | Description                                                                                              |
|---------------------|----------|----------------------------------------------------------------------------------------------------------|
| delete-ids          | ❌        | Comma-separated string of IDs to delete                                                                  |
| upload-ids          | ❌        | Comma-separated string of IDs to upload                                                                  |
| empty-array-default | ❌        | Default value to use in JSON arrays when empty (e.g., "skip" or "none"). If not provided, empty arrays remain as [] |

---

## 📝 Usage Example

```yaml
jobs:
  parse-ids:
    runs-on: ubuntu-latest
    steps:
      - name: Parse CSV to JSON
        id: parse
        uses: ./.github/actions/parse-csv-to-json
        with:
          delete-ids: 'PARTNER001,PARTNER002,PARTNER003'
          upload-ids: 'PARTNER003,PARTNER004,PARTNER005'
          empty-array-default: 'skip'
      - name: Display JSON Arrays
        run: |
          echo "To Delete: ${{ steps.parse.outputs.to_delete }}"
          echo "To Upload: ${{ steps.parse.outputs.to_upload }}"
          echo "All IDs: ${{ steps.parse.outputs.all_ids }}"
```

---

## 🪵 Example Logs

```
::group::Input Parameters
Delete IDs string: PARTNER001,PARTNER002,PARTNER003
Upload IDs string: PARTNER003,PARTNER004,PARTNER005
Empty array default value: skip
::endgroup::

::group::Parsing CSV Strings
  - Delete array count: 3
  - Delete IDs: PARTNER001 PARTNER002 PARTNER003
  - Upload array count: 3
  - Upload IDs: PARTNER003 PARTNER004 PARTNER005
::endgroup::

::group::Filtering Duplicates
Removing 'PARTNER003' from delete list (found in upload list)
Filtered delete array count: 2
Filtered delete IDs: PARTNER001 PARTNER002
::endgroup::

::group::Converting to JSON Arrays
to_delete: ["PARTNER001","PARTNER002"]
to_upload: ["PARTNER003","PARTNER004","PARTNER005"]
all_ids: ["PARTNER001","PARTNER002","PARTNER003","PARTNER004","PARTNER005"]
::endgroup::
```
_These are example logs you may encounter when running this action. Actual logs may vary depending on configuration and runtime conditions._

---

## 📂 Outputs

| Name      | Description                                                                |
|-----------|----------------------------------------------------------------------------|
| to_delete | JSON array of IDs to delete (filtered to exclude IDs also in upload)      |
| to_upload | JSON array of IDs to upload                                                |
| all_ids   | JSON array of all unique IDs (union of to_delete and to_upload)            |

---

## 💡 Tips & Troubleshooting

- The action automatically removes whitespace from IDs.
- IDs that appear in both delete and upload lists are removed from the delete list only.
- If `empty-array-default` is provided, empty arrays will contain that value instead of being empty.
- The `all_ids` output provides the complete set of unique IDs across both lists.
- Input strings can be empty or omitted (they default to empty strings).
- The action uses grouped logging for better readability in GitHub Actions.
- JSON arrays are properly formatted for use in matrix strategies or further processing.

---

## 📚 References

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/CLOUD_INTEGRATION)
- [GitHub Actions Matrix Strategy](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs)