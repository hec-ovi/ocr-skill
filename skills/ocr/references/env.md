# Environment and install

Load when `init`/`doctor` is not ready or the user asks how to install.

## Agent skill pack (no hand install)

After `/skills add` or `npx skills add`, the pack includes `./ocr` (and `bin/ocr`). First run:

1. Finds `uv` (or installs a skill-local copy under `.tools/` if curl works)
2. `uv sync --no-dev` into the pack's `.venv`
3. Runs `.venv/bin/ocr`

Agents should only call that launcher. Do not `pip install` into the system Python.

## Variables

| Variable | Default | Meaning |
|---|---|---|
| `OCR_BACKEND` | `auto` | `auto`, `llamacpp`, `deepseek`, or `mock` |
| `OCR_LLAMA_URL` | `http://127.0.0.1:8090` | llama-server (Vulkan GGUF) base URL |
| `OCR_LLAMA_MODEL` | `ocr` | Alias on that server |
| `OCR_LLAMA_TIMEOUT_S` | `300` | HTTP timeout for one page |
| `OCR_MODEL_ID` | `deepseek-ai/DeepSeek-OCR-2` | HF id (torch path only) |
| `OCR_MODEL_PATH` | unset | Local torch checkpoint path |
| `OCR_DEVICE` | `auto` | torch: `auto`, `cuda`, or `cpu` |
| `OCR_CACHE_DIR` | `$XDG_CACHE_HOME/ocr-skill` or `~/.cache/ocr-skill` | Work dirs + document store |

## Real OCR (recommended: Vulkan)

Same host pattern as `llama-vulkan-strix`. Full steps: `docker/README.md` and `docs/INSTALL.md`.

```bash
mkdir -p ~/models/gguf/DeepSeek-OCR-2
uvx --from 'huggingface_hub[cli]' hf download sabafallah/DeepSeek-OCR-2-GGUF \
  deepseek-ocr-2-q8_0.gguf mmproj-deepseek-ocr-2-q8_0.gguf \
  --local-dir ~/models/gguf/DeepSeek-OCR-2

cp docker/.env.example docker/.env
# set MODELS_DIR in docker/.env to that directory
docker compose -f docker/docker-compose.yml --env-file docker/.env up -d
export OCR_BACKEND=llamacpp OCR_LLAMA_URL=http://127.0.0.1:8090
ocr doctor
```

Torch path (optional): `uv sync --extra deepseek` and `OCR_BACKEND=deepseek`.

## Doctor vs init

- `ocr init` - capability snapshot for the session (`ready`, `backend`, `next_actions`)
- `ocr doctor` - per-check detail (pillow, pypdfium2, mock, backends)

Both accept `--json` and `--quick`.
