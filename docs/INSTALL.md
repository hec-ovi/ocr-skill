# Install and harness setup

The only hard requirement is [uv](https://docs.astral.sh/uv/): it provides `uvx` and
downloads a compatible Python on first run. The tool is the same Python package on every
surface; harnesses differ only in where the skill files go.

Two facts that recur:

- The **distribution** is `ocr-skill`; the **command** is `ocr`. A second console script
  named `ocr-skill` is installed too, so `uvx ocr-skill <cmd>` resolves with no `--from`.
- **Not on PyPI yet.** Until it is, every install route uses the git URL. Once published,
  drop `--from git+...` and plain `uvx ocr-skill ...` works.

There is **no MCP server**. Agents drive the `ocr` CLI through their own shell; the skill
file tells them when and how. Whatever your harness, prefer `ocr init --quick` once per
session if you are unsure the engine is ready.

**Recommended real OCR on AMD Strix Halo:** Vulkan llama.cpp Docker
(`docker/`, same pattern as llama-vulkan-strix) + `OCR_BACKEND=llamacpp`.
Optional torch path: `deepseek` extra. `OCR_BACKEND=mock` is for tests only.

## Route summary

| You want | Do this |
|---|---|
| Run it once, no install | `uvx --from git+https://github.com/hec-ovi/ocr-skill ocr doctor` |
| The skill in your agent | `npx skills add hec-ovi/ocr-skill` |
| A Claude Code plugin | `/plugin marketplace add hec-ovi/ocr-skill` then `/plugin install ocr@ocr-skill` |
| Develop on it | `git clone ...` then `uv sync` |

## CLI, no install

```bash
uvx --from git+https://github.com/hec-ovi/ocr-skill ocr doctor --quick
uvx --from git+https://github.com/hec-ovi/ocr-skill ocr extract ./scan.png --json
```

`uvx` caches the build, so the second run is fast. Pin a ref with `@<tag>` or `@<sha>` on
the git URL for reproducibility. To put `ocr` on PATH permanently:

```bash
uv tool install git+https://github.com/hec-ovi/ocr-skill
ocr doctor --quick
```

For real OCR (Vulkan, recommended):

```bash
# 1) CLI on PATH (above)
# 2) GGUF + mmproj under MODELS_DIR (see docker/README.md)
# 3) server
cp docker/.env.example docker/.env
docker compose -f docker/docker-compose.yml --env-file docker/.env up -d
export OCR_BACKEND=llamacpp
export OCR_LLAMA_URL=http://127.0.0.1:8090
ocr doctor
ocr extract ./scan.png --json
```

Optional torch path: `uv tool install 'git+https://github.com/hec-ovi/ocr-skill[deepseek]'`
and `OCR_BACKEND=deepseek`.

## As an agent skill (npx skills add)

The [`skills`](https://www.npmjs.com/package/skills) CLI installs `skills/ocr/` into every
agent it detects (Claude Code, Codex, OpenCode, Cursor, Gemini, and others), so the same
`SKILL.md` works across all of them.

```bash
npx skills add hec-ovi/ocr-skill                 # all detected agents, project scope
npx skills add hec-ovi/ocr-skill -g              # global (your user dir)
npx skills add hec-ovi/ocr-skill -a claude-code -a codex -s ocr
npx skills add hec-ovi/ocr-skill --list
npx skills add hec-ovi/ocr-skill --copy -y       # copy instead of symlink (e.g. Windows)
```

The skill shells out to the `ocr` CLI. Install that too (`uv tool install` above) or the
commands in the skill will not resolve (the skill also documents `uvx` / `uv run` fallbacks).

## Claude Code

### Plugin

```text
/plugin marketplace add hec-ovi/ocr-skill
/plugin install ocr@ocr-skill
/reload-plugins
```

`.claude-plugin/marketplace.json` points at this repo (`source: "./"`), so
`skills/ocr/SKILL.md` is discovered.

### Manual

Skills: `npx skills add` above, or copy/symlink `skills/ocr` into `~/.claude/skills/ocr`.
CLI: `uv tool install` above.

## Codex CLI

```bash
npx skills add hec-ovi/ocr-skill -a codex
uv tool install git+https://github.com/hec-ovi/ocr-skill
```

## Grok / other Agent Skills hosts

Install the skill directory the same way your host expects (often
`~/.grok/skills/ocr` or project `.grok/skills/ocr`), or use `npx skills add` if it detects
that host. The body of `SKILL.md` is host-agnostic: shell out to `ocr`.

## Develop from a clone

```bash
git clone git@github.com:hec-ovi/ocr-skill.git
cd ocr-skill
uv sync
OCR_BACKEND=mock uv run pytest
OCR_BACKEND=mock uv run ocr extract ./some.png --json
```

## First session checklist

1. `ocr doctor --quick --json` (or `ocr init --quick --json`)
2. If `engine_llamacpp` is not ok: start `docker/` stack and set `OCR_BACKEND=llamacpp`
3. `ocr extract <abs-path> --json`
4. If `has_more`: `ocr open <handle> --page 2 --json`
