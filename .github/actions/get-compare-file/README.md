# 🚀 Get Compare File GitHub Action

Gets list of changed files between two Git references using Git CLI.

---

## ✨ Overview

This action compares two Git references (branches or tags) and generates a detailed diff report showing which files have changed. It also creates directory listings for both references to identify structural changes. This is essential for determining which Integration Packages or Partner Directory entries need to be synchronized.

---

## ⚙️ Inputs

| Name       | Required | Description                                  |
|------------|----------|----------------------------------------------|
| base-ref   | ✅        | Source Git reference (branch or tag)         |
| target-ref | ✅        | Target Git reference (branch or tag)         |
| mode       | ✅        | Mode IntegrationPackages/PartnerDirectory    |

---

## 📝 Usage Example

```yaml
jobs:
  compare-refs:
    runs-on: ubuntu-latest
    steps:
      - name: Get Git Comparison
        id: compare
        uses: ./.github/actions/get-compare-file
        with:
          base-ref: 'main'
          target-ref: 'develop'
          mode: 'IntegrationPackages'
      - name: Display results
        run: |
          echo "Changed files: ${{ steps.compare.outputs.files_changed }}"
          echo "Base directory list: ${{ steps.compare.outputs.base_dir_file }}"
          echo "Target directory list: ${{ steps.compare.outputs.target_dir_file }}"
```

---

## 🪵 Example Logs

```
✅ Resolved base-ref: refs/heads/main
✅ Resolved target-ref: refs/heads/develop
🔍 Comparing refs/heads/main...refs/heads/develop
Fetching resolved refs into temporary local refs...
Running git diff for IntegrationPackages...
✅ Diff file created: /tmp/IntegrationPackages_gittdiff.txt
✅ Base directory listing created: /tmp/IntegrationPackages_base_dir.txt
✅ Target directory listing created: /tmp/IntegrationPackages_target_dir.txt
```
_These are example logs you may encounter when running this action. Actual logs may vary depending on configuration and runtime conditions._

---

## 📂 Outputs

| Name            | Description                                      |
|-----------------|--------------------------------------------------|
| files_changed   | Path to file containing list of changed files    |
| base_dir_file   | Path to file containing directory listing of base ref |
| target_dir_file | Path to file containing directory listing of target ref |

---

## 💡 Tips & Troubleshooting

- The action automatically detects whether the refs are branches or tags.
- Both references must exist in the remote repository.
- The action uses `fetch-depth: 0` to ensure all history is available for comparison.
- Rename detection threshold is increased (9999) to handle large repositories.
- The diff output includes file status codes (A=added, M=modified, D=deleted, R=renamed).
- Directory listings contain only first-level subdirectories (packages or partner IDs).
- If the mode directory doesn't exist in a reference, an empty directory listing is created.
- The action creates temporary files in `${{ runner.temp }}` with mode-specific prefixes.

---

## 📚 References

- [SAP BTP Integration Suite Documentation](https://help.sap.com/docs/CLOUD_INTEGRATION)
- [Git Diff Documentation](https://git-scm.com/docs/git-diff)