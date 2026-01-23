# 🚀 Process CSV with Regex GitHub Action

Processes a CSV file, applies a regex to each item, and returns the result as a CSV string.

---

## ✨ Overview

This action reads a CSV file, applies a regular expression pattern to each comma-separated item, extracts the matched groups, and returns the processed results as a new CSV string. The original file is also updated with the processed values. This is useful for extracting specific parts of IDs or transforming CSV data.

---

## ⚙️ Inputs

| Name     | Required | Description                          |
|----------|----------|--------------------------------------|
| csv_file | ✅        | Path to the CSV file to process      |
| regex    | ✅        | Regex pattern to apply to each item  |

---

## 📝 Usage Example

```yaml
jobs:
  process-csv:
    runs-on: ubuntu-latest
    steps:
      - name: Process CSV with Regex
        id: process
        uses: ./.github/actions/process-csv-with-regex
        with:
          csv_file: './package-ids.csv'
          regex: '^.*~(.*)$'
      - name: Display result
        run: echo "Processed IDs: ${{ steps.process.outputs.result }}"
```

---

## 🪵 Example Logs

```
::group::CSV Input
Input CSV file: ./package-ids.csv
Input CSV content: Partner_Integration~PKG001,System_Config~PKG002,Data_Flow~PKG003
Regex pattern: ^.*~(.*)$
::endgroup::

Processing items with regex...

::group::CSV Output
Output CSV string: PKG001,PKG002,PKG003
::endgroup::

Result written back to file: ./package-ids.csv
```
_These are example logs you may encounter when running this action. Actual logs may vary depending on configuration and runtime conditions._

---

## 📂 Outputs

| Name   | Description              |
|--------|--------------------------|
| result | Processed CSV string     |

---

## 💡 Tips & Troubleshooting

- The regex pattern should include a capture group `()` to extract the desired part.
- The first capture group `${BASH_REMATCH[1]}` is used as the extracted value.
- If an item doesn't match the regex, an empty value is preserved in that position.
- The action modifies the input CSV file in-place with the processed results.
- Common use case: Extracting package IDs from directory names (e.g., `Name~ID` → `ID`).
- Ensure the regex pattern is properly escaped for bash.
- The action uses grouped logging for better visibility in GitHub Actions.

---

## 📚 References

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/CLOUD_INTEGRATION)
- [Bash Regular Expressions](https://www.gnu.org/software/bash/manual/html_node/Pattern-Matching.html)