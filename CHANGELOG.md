# Changelog

## 0.1.0

- Initial skill: `ocr extract` / `ocr open` / `ocr init` / `ocr doctor`
- Contract layers: ingest, OCR, format, agent I/O
- Backends: `mock` (tests) and `deepseek` (DeepSeek-OCR-2, optional extra)
- Portable `skills/ocr/SKILL.md` (stdio, no MCP)
- Envelope JSON output, untrusted OCR fence, on-disk document store for pagination
