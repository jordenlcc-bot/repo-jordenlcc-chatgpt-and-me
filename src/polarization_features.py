"""
polarization_features.py

Small helpers for polarization-inspired rendering features.

These functions are not a full electromagnetic simulator. They provide a compact
way to represent line/circle/ellipse-like local signals for Dragonfly-360.
"""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class PolarizationState:
    """A simple polarization-inspired feature state.

    orientation: major-axis angle in radians.
    ellipticity: -1..1, where 0 is linear-like, +1/-1 are circular-like handed states.
    phase: phase angle in radians.
    strength: signal strength.
    """

    orientation: float
    ellipticity: float
    phase: float
    strength: float = 1.0


def classify_polarization(ex: float, ey: float, phase_delta: float) -> str:
    """Classify a simple two-component oscillation."""
    ax = abs(ex)
    ay = abs(ey)
    phase = ((phase_delta + math.pi) % (2.0 * math.pi)) - math.pi

    if abs(math.sin(phase)) < 1e-3:
        return "linear"
    if abs(ax - ay) < 1e-3 and abs(abs(phase) - math.pi / 2.0) < 1e-3:
        return "circular"
    return "elliptical"


def handedness(phase_delta: float) -> str:
    """Return a left/right handed label from phase sign.

    This is a convention for feature channels, not a universal optical convention.
    """
    phase = ((phase_delta + math.pi) % (2.0 * math.pi)) - math.pi
    if phase > 0:
        return "left"
    if phase < 0:
        return "right"
    return "none"


def ellipse_strength(ex: float, ey: float) -> float:
    """Return a simple amplitude magnitude for two components."""
    return math.sqrt(ex * ex + ey * ey)


def make_state(ex: float, ey: float, phase_delta: float) -> PolarizationState:
    """Build a simple polarization-inspired state from two components."""
    orientation = math.atan2(ey, ex)
    strength = ellipse_strength(ex, ey)
    if strength == 0:
        ellipticity = 0.0
    else:
        ellipticity = max(
            -1.0,
            min(1.0, math.sin(phase_delta) * min(abs(ex), abs(ey)) / max(abs(ex), abs(ey), 1e-9)),
        )
    return PolarizationState(
        orientation=orientation,
        ellipticity=ellipticity,
        phase=phase_delta,
        strength=strength,
    )


def gate_from_polarization(state: PolarizationState, target_orientation: float, sharpness: float = 8.0) -> float:
    """Directional soft gate based on orientation alignment."""
    diff = abs(((state.orientation - target_orientation + math.pi) % (2.0 * math.pi)) - math.pi)
    alignment = math.cos(diff)
    return 1.0 / (1.0 + math.exp(-sharpness * alignment))
