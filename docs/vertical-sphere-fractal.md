# Vertical sphere fractal model

## Purpose

This document defines a first version of the vertical sphere / compound-eye contraction model.

The model is inspired by the user's celestial-sphere sketch:

```text
outer 360° sky field
→ directional east/west counter-motion
→ recursive contraction
→ focused human-eye output
```

## Main concept

The model uses two visual regimes:

1. **Compound-eye regime**
   - wide 360° coverage,
   - low resolution,
   - many small cells,
   - cheap global reaction detection.

2. **Human-eye regime**
   - narrow focus,
   - high resolution,
   - central refined output,
   - expensive compute only where useful.

The bridge between them is a contraction operator:

```text
large sphere field S
→ scale / gate / fold
→ compact focused field F
```

## Direction convention

The user uses celestial motion as a visual analogy:

- Earth rotates west-to-east.
- The apparent sky motion is seen east-to-west.

In the model this becomes a two-channel direction convention:

```text
inner field  : west → east
outer field  : east → west
```

This does not need to be physically exact for rendering. It is a coordinate convention for opposing flow directions.

## Riemann sphere link

The Riemann sphere offers a clean geometry for two-chart thinking:

```text
south chart : local / small / 0 side
north chart : infinity / far / ∞ side
equator     : transition boundary
```

This can be used to split a 360° field into two complementary maps before recombining them.

## Pascal / Yanghui link

Yanghui triangle modulo 2 gives a binary fractal mask.

Project use:

```text
odd  -> open / refine / yang channel
even -> skip / damp / yin channel
```

This is symbolic naming. The actual useful part is the binary fractal gate.

## Lévy C curve link

Lévy C curve gives a recursive 45°/90° folding path.

Project use:

```text
path recursion
→ multi-scale sampling order
→ progressive refinement
```

## Miller feedback link

Miller-style feedback is used for stability:

```text
small coupling + gain -> large effective reaction
large reaction -> clamp / compensate
```

## Minimal algorithm sketch

```text
1. Build a 360° spherical grid.
2. Compute cheap reaction signals for each cell.
3. Apply binary/fractal gate mask.
4. Apply direction convention: inner west→east, outer east→west.
5. Contract selected cells toward output focus.
6. Stabilize contraction with feedback compensation.
7. Render focused high-resolution output.
```

## Important warning

This is an architecture hypothesis. The correctness must be tested with experiments.
