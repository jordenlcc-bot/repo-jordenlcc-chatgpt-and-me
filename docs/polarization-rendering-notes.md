# Polarization notes for Dragonfly-360

## Why this belongs

The new material on polarization fits the rendering idea very well.

Polarization gives a clean mathematical language for:

- horizontal / vertical components,
- phase difference,
- circular rotation,
- elliptical motion,
- left/right handedness,
- filtering and gating by direction.

This is directly useful for the 360 compound-eye contraction model.

## Core physical facts

For an electromagnetic wave in free space:

```text
E field ⟂ B field
E field ⟂ propagation direction
B field ⟂ propagation direction
```

Conventionally, the polarization direction of an electromagnetic wave refers to the electric-field direction.

The main polarization types:

```text
linear polarization   -> field tip traces a line
circular polarization -> field tip traces a circle
elliptical polarization -> field tip traces an ellipse
```

Circular and elliptical polarization can be divided into right-handed and left-handed forms.

## Project mapping

```text
linear polarization
→ one clean axis / stripe mask / barcode-like sampling

circular polarization
→ rotating cell / compound-eye sweep / 360 phase sampling

elliptical polarization
→ anisotropic focus / stretched lens / non-uniform scale contraction

left/right handedness
→ yin-yang channel / north-south chart / clockwise-counterclockwise gate

polarizer
→ directional filter / logic gate / refine-or-skip selector

Poincare sphere
→ compact sphere representation for polarization state
```

## Rendering interpretation

In the Dragonfly-360 model, polarization can become an extra feature channel:

```text
cell = {
    color_rgb,
    luminance,
    direction,
    phase,
    polarization_state,
    reaction_score,
}
```

This can help decide:

- which cell should refine,
- which cell should be suppressed,
- which direction has stronger light reaction,
- whether a local signal is line-like, circle-like, or ellipse-like.

## Connection to the user's dream sketch

The dream sketch includes stripes, circular rings, a globe, wave motion, and a vertical contraction axis.

Polarization connects these cleanly:

```text
stripe mask       -> linear polarization / directional filter
circular rings    -> circular or radial response
ellipse diagram   -> anisotropic contraction
vertical axis     -> propagation / time / phase axis
left-right motion -> handedness / phase rotation
```

## Important boundary

Polarization is real physics. The use here is an architecture analogy and feature design.

It does not prove that AI rendering is literally an electromagnetic wave. It provides a useful way to represent direction, phase, and filtering.
