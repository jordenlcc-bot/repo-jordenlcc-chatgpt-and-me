# Dragonfly-360 Vertical Render

A research prototype for a reaction-first AI rendering idea:

> Use a 360° compound-eye style field to gather low-cost global information, then contract/scale the field into a tighter high-resolution human-eye output.

This repository stores the working notes, math analogies, and small Python modules for Jorden + ChatGPT research.

## Core idea

The current concept combines:

- **360 vector field**: sky-sphere / celestial-sphere style full-surround sampling.
- **East–west / west–east counter-motion**: an inner/outer direction contrast inspired by Earth rotation versus apparent sky motion.
- **Compound-eye capture**: many cheap low-resolution cells gather global context.
- **Human-eye output**: the model contracts useful information into a focused high-resolution result.
- **Feedback and gating**: Miller-style stabilization and soft logic gates decide what to refine.
- **Fractal / recursive paths**: Pascal/Yanghui parity, Lévy C curve, and recursive scale contraction guide sampling.

## Strict boundary

This is an engineering research notebook. Many ideas are analogies, not proofs.

- Riemann sphere, Pascal triangle, Lévy C curve, and Miller theorem are real mathematical/engineering objects.
- Yin-yang, north/south polarity, and quark up/down are used as symbolic or architectural metaphors.
- Any performance improvement must be tested by experiments.

## Project structure

```text
docs/       Research notes and theory sketches
src/        Small reusable Python modules
experiments/ Prototype scripts
```

## Current target

Build a minimal system that can:

1. sample a 360° field cheaply,
2. assign reaction scores,
3. gate or refine important regions,
4. contract the field into a focused output representation.
