"""Self-bootstrapping ./ocr launcher (agent skill pack entrypoint)."""

from __future__ import annotations

import os
import stat
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_launcher_scripts_exist_and_executable() -> None:
    for rel in ("ocr", "ocr-skill", "bin/ocr"):
        path = ROOT / rel
        assert path.is_file(), rel
        mode = path.stat().st_mode
        assert mode & stat.S_IXUSR, f"{rel} must be executable"


def test_launcher_runs_version() -> None:
    env = os.environ.copy()
    env["OCR_BACKEND"] = "mock"
    proc = subprocess.run(
        [str(ROOT / "ocr"), "--version"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )
    assert proc.returncode == 0, proc.stderr
    assert "ocr-skill" in proc.stdout
    assert "0.3.0" in proc.stdout


def test_launcher_doctor_quick() -> None:
    env = os.environ.copy()
    env["OCR_BACKEND"] = "mock"
    proc = subprocess.run(
        [str(ROOT / "ocr"), "doctor", "--quick", "--json"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert '"ok": true' in proc.stdout or '"ok":true' in proc.stdout
    assert "pillow" in proc.stdout


def test_skill_md_forbids_hand_pip() -> None:
    body = (ROOT / "skills" / "ocr" / "SKILL.md").read_text(encoding="utf-8").lower()
    assert "do not" in body and "pip" in body
    assert "resolve" in body
    assert ".noob/skills/ocr/ocr" in body
