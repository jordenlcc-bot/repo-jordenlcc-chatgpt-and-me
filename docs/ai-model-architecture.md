# Dragonfly-360 AI Model Architecture

## Positioning

Dragonfly-360 is a testable architecture / coordinate model for an in-sphere real-time generative renderer.

The user is not outside looking at a sphere. The user is inside the visual field. When the user types, speaks, sends an image, or changes a parameter, the surrounding 360° space should react immediately.

## Core pipeline

```text
input text / image / sound / signal
→ sphere block field
→ Riemann sphere coordinate encoding
→ block embedding
→ phase interference gate
→ vertical render layers
→ in-sphere response output
```

Compact formula:

```text
Output = InSphereRender(VerticalRender(InterferenceGate(Embed(RiemannSphereBlocks(Input)))))
```

## MVP scope

The first version should not train a huge Transformer from scratch.

It should implement:

```text
1. build a 360° sphere / dome block grid
2. encode each block using pi-angle and Riemann sphere coordinates
3. create a small block embedding
4. apply phase / polarization-inspired gates
5. run vertical render layers from global field to local detail
6. output an equirectangular / cubemap / dome preview map
```

## Success criteria

The model is worth continuing only if it beats a simple procedural baseline on at least one of these:

```text
spatial coherence
latency
prompt-to-visual controllability
reduction of seams / distortion
stable 360° reaction behavior
```

## Experimental baseline

Compare:

```text
A. plain sin/cos sphere position encoding
B. Riemann sphere coordinate encoding
C. Riemann sphere encoding + phase interference gate
D. later: Transformer / attention block
```

## Engineering boundary

This is not yet a proven physical law. It is a testable rendering architecture.
