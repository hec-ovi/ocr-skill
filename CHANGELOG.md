# Changelog

## 0.1.0

- Initial skill: `ocr extract` / `ocr open` / `ocr init` / `ocr doctor`
- Contract layers: ingest, OCR, format, agent I/O
- Backends: `mock` (tests) and `deepseek` (DeepSeek-OCR-2, optional extra)
- Modes: `markdown`, `free`, `figure`, `ocr` (official DeepSeek prompt family)
- Portable `skills/ocr/SKILL.md` with progressive disclosure (`references/`)
- Multi-CLI install docs and Claude plugin manifests (no MCP)
- Envelope JSON output, untrusted OCR fence, on-disk document store for pagination
- Skill-quality tests (Agent Skills frontmatter limits, standing rules, mode lockstep)
