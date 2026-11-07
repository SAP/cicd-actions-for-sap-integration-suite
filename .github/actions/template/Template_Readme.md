# 🚀 [Action Name] GitHub Action

[Short description of what this action does.]

---

## ✨ Overview

[Explain the main purpose and functionality of the action.]

---

## ⚙️ Inputs

| Name         | Required | Description                                      |
|--------------|----------|--------------------------------------------------|
| [INPUT_1]    | ✅/❌     | [Description of input 1]                          |
| [INPUT_2]    | ✅/❌     | [Description of input 2]                          |
| ...          | ...      | ...                                              |

---

## 📝 Usage Example

```yaml
jobs:
  [job-name]:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v7
      - name: [Action step name]
        uses: ./.github/actions/[action-folder-name]
        with:
          [INPUT_1]: [value]
          [INPUT_2]: [value]
          ...
```

---

## 🪵 Example Logs

```
[INFO] Starting action...
[DEBUG] Input value: [INPUT_1]=[value]
[INFO] Processing completed successfully.
[ERROR] Failed to process input: [reason]
```
_These are example logs you may encounter when running this action. Actual logs may vary depending on configuration and runtime conditions._

---

## 📂 Outputs

| Name         | Description |
|--------------|-------------|
| [OUTPUT_1]   | [Description of output 1] |
| [OUTPUT_2]   | [Description of output 2] |
| ...          | ...                       |

---

## 💡 Tips & Troubleshooting

- [Add any useful tips, caveats, or troubleshooting steps here.]
- [Example: Ensure input file paths are correct and relative to repository root.]

---

## 📚 References

- [Link to related documentation or resources]