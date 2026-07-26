"""Layer 2: OCR engines."""

from __future__ import annotations

from .. import config, errors
from ..envelope import OcrSkillError
from .adapters.deepseek import DeepSeekEngine
from .adapters.mock import MockEngine
from .models import OCR_CONTRACT_VERSION, OcrPageResult
from .port import OCREngine

__all__ = [
    "OCR_CONTRACT_VERSION",
    "OCREngine",
    "OcrPageResult",
    "MockEngine",
    "DeepSeekEngine",
    "build_engine",
]


def build_engine(name: str | None = None) -> OCREngine:
    """Resolve OCR_BACKEND (or override) to an engine instance."""
    chosen = (name or config.backend_name()).strip().lower()
    if chosen == "mock":
        return MockEngine()
    if chosen == "deepseek":
        return DeepSeekEngine()
    if chosen == "auto":
        deep = DeepSeekEngine()
        ok, detail = deep.available()
        if ok:
            # Prefer deepseek when deps exist; model download can still fail later.
            try:
                import torch  # noqa: F401
                import transformers  # noqa: F401

                return deep
            except ImportError:
                pass
        # Fall through to mock only if explicitly testing would be wrong for prod.
        # auto without deepseek deps is an error so agents install the right extra.
        raise OcrSkillError(
            errors.ENGINE_UNAVAILABLE,
            "no OCR engine available (auto)",
            hint=(
                "Install the deepseek extra (`uv sync --extra deepseek`) and set "
                "OCR_MODEL_PATH if the weights are local, or set OCR_BACKEND=mock for tests. "
                f"Detail: {detail}"
            ),
        )
    raise OcrSkillError(
        errors.CONFIG_ERROR,
        f"unknown OCR_BACKEND: {chosen}",
        hint="Use auto, mock, or deepseek.",
    )
