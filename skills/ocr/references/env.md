# Environment and install

Load when `init`/`doctor` is not ready or the user asks how to install.

## Variables

| Variable | Default | Meaning |
|---|---|---|
| `OCR_BACKEND` | `auto` | `auto`, `deepseek`, or `mock` |
| `OCR_MODEL_ID` | `deepseek-ai/DeepSeek-OCR-2` | Hugging Face id |
| `OCR_MODEL_PATH` | unset | Local checkpoint path (wins over id) |
| `OCR_DEVICE` | `auto` | `auto`, `cuda`, or `cpu` |
| `OCR_CACHE_DIR` | `$XDG_CACHE_HOME/ocr-skill` or `~/.cache/ocr-skill` | Work dirs + document store |

## Install

```bash
# from clone
uv sync
uv sync --extra deepseek   # real engine

# one-shot without clone
uvx ocr-skill doctor
```

Prefer a local model under the machine model tree if weights already exist; set `OCR_MODEL_PATH` instead of re-downloading.

## Doctor vs init

- `ocr init` — capability snapshot for the session (`ready`, `backend`, `next_actions`)
- `ocr doctor` — per-check detail (pillow, pypdfium2, mock, deepseek deps)

Both accept `--json` and `--quick`.
