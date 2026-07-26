from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_skill_md_exists_and_mentions_extract() -> None:
    skill = ROOT / "skills" / "ocr" / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    assert "name: ocr" in text
    assert "ocr extract" in text
    assert "UNTRUSTED-OCR-CONTENT" in text
    assert "Not MCP" in text or "not MCP" in text or "No MCP" in text or "stdio" in text.lower()
