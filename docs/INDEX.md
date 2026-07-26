# Layer index

Map "what to change" to the one folder to open. Outsiders read contracts only.

| Want | Open |
|---|---|
| Image/PDF → page images | `src/ocrskill/layer1_ingest/` + `contracts/ingest.schema.json` |
| OCR engine / DeepSeek adapter | `src/ocrskill/layer2_ocr/` + `contracts/ocr.schema.json` |
| Fence, pagination, store | `src/ocrskill/layer3_format/` + `contracts/format.schema.json` |
| Agent extract/open face | `src/ocrskill/layer4_agentio/` + `contracts/agent-io.schema.json` |
| CLI flags / human output | `src/ocrskill/cli.py` |
| Doctor / init | `src/ocrskill/doctor/` |
| Portable skill instructions | `skills/ocr/SKILL.md` |
| Skill level-3 references | `skills/ocr/references/` |
| Skill design / progressive disclosure | `docs/SKILL_DESIGN.md` |
| Model research notes | `docs/DEEPSEEK_OCR_2.md` |
| Engine mode ↔ prompt map | `src/ocrskill/layer2_ocr/modes.py` |
| Envelope wrapper | `contracts/envelope.schema.json` + `src/ocrskill/envelope.py` |
