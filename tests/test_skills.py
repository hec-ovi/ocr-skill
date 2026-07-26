from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "skills" / "ocr" / "SKILL.md"
REFS = ROOT / "skills" / "ocr" / "references"


def _parse_skill() -> tuple[dict, str]:
    text = SKILL_PATH.read_text(encoding="utf-8")
    assert text.startswith("---\n"), "SKILL.md must start with YAML frontmatter"
    _, fm, body = text.split("---", 2)
    meta = yaml.safe_load(fm)
    return meta, body


def test_skill_frontmatter_agentskills_spec() -> None:
    """Level-1 metadata constraints from agentskills.io specification (2025-12)."""
    meta, _ = _parse_skill()
    name = meta["name"]
    desc = meta["description"]

    assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name), name
    assert len(name) <= 64
    assert name == SKILL_PATH.parent.name

    assert isinstance(desc, str) and desc.strip()
    assert 1 <= len(desc) <= 1024, f"description length {len(desc)} exceeds 1024"

    # Discovery: what + when + trigger keywords
    lower = desc.lower()
    for needle in ("pdf", "image", "markdown", "ocr", "extract"):
        assert needle in lower, f"description missing trigger keyword: {needle}"

    if "compatibility" in meta and meta["compatibility"]:
        assert len(str(meta["compatibility"])) <= 500


def test_skill_body_has_standing_procedure() -> None:
    _, body = _parse_skill()
    # Standing rules / security / anti-patterns: research-skill style load-bearing sections
    for heading in (
        "Standing rules",
        "When to use",
        "When NOT to use",
        "Mode selection",
        "Workflow",
        "Security",
        "Anti-patterns",
    ):
        assert heading in body, f"missing section: {heading}"

    assert "UNTRUSTED-OCR-CONTENT" in body
    assert "ocr extract" in body
    assert "ocr open" in body
    assert "has_more" in body
    assert "Never invent" in body or "never invent" in body.lower()


def test_skill_under_size_budget() -> None:
    """Level-2 budget: keep body lean; details in references/."""
    text = SKILL_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    assert len(lines) <= 500, f"SKILL.md has {len(lines)} lines; split into references/"
    # Rough token proxy: ~4 chars/token
    assert len(text) <= 5000 * 4, f"SKILL.md ~{len(text)//4} tokens; prefer <5000"


def test_skill_references_exist_and_linked() -> None:
    _, body = _parse_skill()
    for name in ("modes.md", "env.md", "envelope.md"):
        path = REFS / name
        assert path.is_file(), path
        assert f"references/{name}" in body, f"SKILL.md should link {name}"


def test_skill_modes_match_engine() -> None:
    from ocrskill.layer2_ocr.modes import DEEPSEEK_PROMPTS, MODES

    modes_ref = (REFS / "modes.md").read_text(encoding="utf-8")
    for mode in MODES:
        assert mode in modes_ref
        assert mode in DEEPSEEK_PROMPTS
    # Official grounding tag present for layout modes
    assert "<|grounding|>" in DEEPSEEK_PROMPTS["markdown"]
    assert "Free OCR" in DEEPSEEK_PROMPTS["free"]
    assert "Parse the figure" in DEEPSEEK_PROMPTS["figure"]


def test_description_prefers_ocr_over_guessing() -> None:
    meta, _ = _parse_skill()
    desc = meta["description"].lower()
    assert "prefer" in desc or "exact" in desc or "thumbnail" in desc or "vision" in desc


def test_install_docs_and_plugin_manifests() -> None:
    install = ROOT / "docs" / "INSTALL.md"
    assert install.is_file()
    text = install.read_text(encoding="utf-8")
    assert "npx skills add" in text
    assert "no mcp" in text.lower()
    assert "uv tool install" in text

    market = ROOT / ".claude-plugin" / "marketplace.json"
    plugin = ROOT / ".claude-plugin" / "plugin.json"
    assert market.is_file() and plugin.is_file()
    market_data = json.loads(market.read_text(encoding="utf-8"))
    assert market_data["plugins"][0]["name"] == "ocr"
    plugin_data = json.loads(plugin.read_text(encoding="utf-8"))
    assert plugin_data["name"] == "ocr"

