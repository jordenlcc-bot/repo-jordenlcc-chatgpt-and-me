"""
Quark-inspired input encoder for Dragonfly-360.

Important boundary:
This module does NOT claim that text tokens are physical quarks.
It uses quark color-neutrality logic as a computational metaphor for:

- token id -> symbolic quark state
- color / anticolor -> complementary channels
- meson / baryon neutrality -> stable grouped input cells
- compound eye -> many low-cost local cells
- phase gate -> interference-style visual response

This is intended as one encoder option for the in-sphere renderer.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import blake2b
from math import cos, pi, sin
from typing import Iterable, List, Sequence, Tuple

COLORS = ("red", "green", "blue")
ANTICOLORS = ("antired", "antigreen", "antiblue")
FLAVORS = ("up", "down", "strange", "charm", "top", "bottom")


@dataclass(frozen=True)
class QuarkToken:
    token: str
    token_id: int
    flavor: str
    color: str
    anti: bool
    phase: float
    q: float
    qbar: float


@dataclass(frozen=True)
class CompoundEyeCell:
    index: int
    tokens: Tuple[QuarkToken, ...]
    neutral_score: float
    phase: float
    gate: float
    rgb: Tuple[float, float, float]
    vector: Tuple[float, ...]


def stable_id(text: str, modulo: int = 2**31 - 1) -> int:
    """Stable deterministic id for text."""
    digest = blake2b(text.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "big") % modulo


def tokenise(text: str) -> List[str]:
    """Very small tokenizer: whitespace if available, otherwise character-level."""
    parts = [p for p in text.strip().split() if p]
    if parts:
        return parts
    return [c for c in text.strip() if not c.isspace()]


def make_quark_token(token: str) -> QuarkToken:
    """Map one input token into a symbolic quark/anti-quark state."""
    tid = stable_id(token)
    flavor = FLAVORS[tid % len(FLAVORS)]
    anti = ((tid // 7) % 2) == 1
    color_index = (tid // 13) % 3
    color = ANTICOLORS[color_index] if anti else COLORS[color_index]
    phase = ((tid % 3600) / 3600.0) * 2.0 * pi

    # Q/Qbar are complementary computational channels, not physical charges.
    q = 0.5 + 0.5 * cos(phase)
    qbar = 1.0 - q

    return QuarkToken(
        token=token,
        token_id=tid,
        flavor=flavor,
        color=color,
        anti=anti,
        phase=phase,
        q=q,
        qbar=qbar,
    )


def pascal_row(n: int) -> List[int]:
    """Return row n of Pascal/Yanghui triangle."""
    if n < 0:
        raise ValueError("n must be non-negative")
    row = [1]
    for _ in range(n):
        row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]
    return row


def sierpinski_mask(n: int) -> List[int]:
    """Modulo-2 Pascal row; useful as a recursive gate mask."""
    return [v % 2 for v in pascal_row(n)]


def color_vector(color: str) -> Tuple[float, float, float]:
    """Symbolic RGB vector for quark color bookkeeping."""
    table = {
        "red": (1.0, 0.0, 0.0),
        "green": (0.0, 1.0, 0.0),
        "blue": (0.0, 0.0, 1.0),
        "antired": (-1.0, 0.0, 0.0),
        "antigreen": (0.0, -1.0, 0.0),
        "antiblue": (0.0, 0.0, -1.0),
    }
    return table[color]


def neutral_score(tokens: Sequence[QuarkToken]) -> float:
    """
    Score how close a group is to color-neutral.

    1.0 means perfectly neutral under this symbolic bookkeeping.
    """
    if not tokens:
        return 0.0
    r = g = b = 0.0
    for token in tokens:
        cr, cg, cb = color_vector(token.color)
        r += cr
        g += cg
        b += cb
    magnitude = (r * r + g * g + b * b) ** 0.5
    return 1.0 / (1.0 + magnitude)


def phase_gate(tokens: Sequence[QuarkToken], alpha: float = 3.0) -> float:
    """Interference-like gate from average phase coherence."""
    if not tokens:
        return 0.0
    c = sum(cos(t.phase) for t in tokens) / len(tokens)
    s = sum(sin(t.phase) for t in tokens) / len(tokens)
    coherence = (c * c + s * s) ** 0.5
    return 1.0 / (1.0 + pow(2.718281828459045, -alpha * (coherence - 0.5)))


def mix_rgb(tokens: Sequence[QuarkToken]) -> Tuple[float, float, float]:
    """Convert symbolic quark channels into a displayable visual color."""
    if not tokens:
        return (0.0, 0.0, 0.0)
    r = g = b = 0.0
    for token in tokens:
        cr, cg, cb = color_vector(token.color)
        # Anticolor contributes as complementary glow instead of negative light.
        if cr < 0:
            g += 0.5
            b += 0.5
        elif cg < 0:
            r += 0.5
            b += 0.5
        elif cb < 0:
            r += 0.5
            g += 0.5
        else:
            r += cr
            g += cg
            b += cb
    scale = max(r, g, b, 1.0)
    return (r / scale, g / scale, b / scale)


def build_compound_eye_cells(text: str, cell_size: int = 3) -> List[CompoundEyeCell]:
    """
    Build low-cost compound-eye cells from user input.

    cell_size=2 behaves like a meson-like pair.
    cell_size=3 behaves like a baryon-like triplet.
    """
    if cell_size <= 0:
        raise ValueError("cell_size must be positive")

    qtokens = [make_quark_token(t) for t in tokenise(text)]
    cells: List[CompoundEyeCell] = []

    for index in range(0, len(qtokens), cell_size):
        group = tuple(qtokens[index : index + cell_size])
        if not group:
            continue

        score = neutral_score(group)
        gate = phase_gate(group) * score
        phase = sum(t.phase for t in group) / len(group)
        rgb = mix_rgb(group)
        q_mean = sum(t.q for t in group) / len(group)
        qbar_mean = sum(t.qbar for t in group) / len(group)
        row = pascal_row(min(index // cell_size + 1, 6))
        row_sum = float(sum(row))
        binomial_features = tuple(v / row_sum for v in row)

        vector = (
            score,
            gate,
            cos(phase),
            sin(phase),
            q_mean,
            qbar_mean,
            *rgb,
            *binomial_features,
        )

        cells.append(
            CompoundEyeCell(
                index=index // cell_size,
                tokens=group,
                neutral_score=score,
                phase=phase,
                gate=gate,
                rgb=rgb,
                vector=vector,
            )
        )

    return cells


def encode_user_input(text: str, cell_size: int = 3) -> List[Tuple[float, ...]]:
    """Return vectors ready for a renderer or model input layer."""
    return [cell.vector for cell in build_compound_eye_cells(text, cell_size=cell_size)]


if __name__ == "__main__":
    sample = "red north burst equator interference dragonfly compound eye"
    for cell in build_compound_eye_cells(sample):
        print(cell)
