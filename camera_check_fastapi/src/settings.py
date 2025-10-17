"""Default analysis parameters for the camera check service."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class EdgeDetectionParams:
    """Parameter set for the Sobel/Canny based occlusion detection stage."""

    low: int = 50
    high: int = 150
    min_ratio: float = 0.02


@dataclass
class Settings:
    """Default thresholds used by :mod:`src.main` when no overrides are supplied."""

    current_threshold: int = 15
    edge_params: EdgeDetectionParams = field(default_factory=EdgeDetectionParams)


_DEFAULTS = Settings()

DEFAULT_CURRENT_THRESHOLD: int = _DEFAULTS.current_threshold
DEFAULT_EDGE_PARAMS: Dict[str, float] = {
    "low": _DEFAULTS.edge_params.low,
    "high": _DEFAULTS.edge_params.high,
    "min_ratio": _DEFAULTS.edge_params.min_ratio,
}

__all__ = [
    "EdgeDetectionParams",
    "Settings",
    "DEFAULT_CURRENT_THRESHOLD",
    "DEFAULT_EDGE_PARAMS",
]
