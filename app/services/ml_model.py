"""
Load a trained estimator from a ``.pkl`` file using ``joblib``.

Expected default location: ``<project root>/model.pkl``.
Copy your trained file there, or pass another path to :func:`load_model_once`.
"""

from __future__ import annotations

from pathlib import Path
from threading import Lock
from typing import Any

import joblib

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL_PATH = PROJECT_ROOT / "model.pkl"

_model: Any | None = None
_load_error: str | None = None
_lock = Lock()


def get_default_model_path() -> Path:
    """Where the app looks for the trained model by default."""
    return DEFAULT_MODEL_PATH


def load_model_once(model_path: Path | None = None) -> tuple[Any | None, str | None]:
    """
    Load and cache the model the first time this is called.

    Returns ``(model, None)`` on success, or ``(None, message)`` if the file is
    missing or cannot be read. Later calls reuse the same result without reloading.
    """
    global _model, _load_error

    path = model_path or DEFAULT_MODEL_PATH

    with _lock:
        if _model is not None:
            return _model, None
        if _load_error is not None:
            return None, _load_error

        if not path.is_file():
            _load_error = (
                f"Model file not found: {path}. "
                "Add your trained .pkl file to that location (or pass a custom path)."
            )
            return None, _load_error

        try:
            _model = joblib.load(path)
        except Exception as exc:  # noqa: BLE001 - surface any load error as a safe message
            _load_error = f"Could not load model from {path}: {exc}"
            return None, _load_error

    return _model, None
