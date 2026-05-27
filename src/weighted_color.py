"""
weighted_color.py

Conductance-weighted color mixing helpers.

This module is inspired by the circuit weighted-average formula:

    V = (E1/R1 + E2/R2 + E3/R3) / (1/R1 + 1/R2 + 1/R3)

For color, apply the same idea per channel. This is not a full color-science
model; it is a useful weighted blending primitive for experiments.
"""

from __future__ import annotations

from typing import Iterable, Sequence, Tuple

RGB = Tuple[float, float, float]


def conductance_weighted_average(values: Sequence[float], resistances: Sequence[float]) -> float:
    """Return a conductance-weighted average.

    Args:
        values: scalar signal values.
        resistances: positive resistance-like weights. Lower resistance means stronger influence.

    Returns:
        Weighted scalar value.
    """
    if len(values) != len(resistances):
        raise ValueError("values and resistances must have the same length")
    if not values:
        raise ValueError("at least one value is required")

    conductances = []
    for r in resistances:
        if r <= 0:
            raise ValueError("resistances must be positive")
        conductances.append(1.0 / r)

    numerator = sum(v * g for v, g in zip(values, conductances))
    denominator = sum(conductances)
    return numerator / denominator


def mix_rgb(colors: Sequence[RGB], resistances: Sequence[float]) -> RGB:
    """Mix RGB colors using conductance-style weighting.

    Args:
        colors: RGB triples, normally in 0..1.
        resistances: positive resistance-like weights.

    Returns:
        Mixed RGB triple.
    """
    if len(colors) != len(resistances):
        raise ValueError("colors and resistances must have the same length")

    r = conductance_weighted_average([c[0] for c in colors], resistances)
    g = conductance_weighted_average([c[1] for c in colors], resistances)
    b = conductance_weighted_average([c[2] for c in colors], resistances)
    return (r, g, b)


def clamp_rgb(color: RGB, lo: float = 0.0, hi: float = 1.0) -> RGB:
    """Clamp an RGB triple."""
    return tuple(max(lo, min(hi, x)) for x in color)  # type: ignore[return-value]
