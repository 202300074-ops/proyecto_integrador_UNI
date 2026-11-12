---
name: pbr-materials-texturing
description: Use when creating cohesive PBR materials, textures, roughness values, and glTF-compatible shading for the bee, jobón, foliage, and environment.
compatibility: opencode
metadata:
  project: melipona-webar
  domain: 3d
---

# PBR Materials and Texturing Specialist

## Principles
- Use a consistent material language across the bee, jobón, foliage, and environment.
- Prefer readable color blocking and controlled roughness over noisy realism.
- Use metallic only where physically justified; honey and wax should not automatically be treated as metal.
- Pack textures efficiently and avoid unnecessary unique materials.
- Use texture atlases or shared materials when they reduce draw calls without harming quality.

## WebAR constraints
- Prefer glTF-compatible Principled BSDF workflows.
- Check texture color spaces and image packing.
- Keep texture resolution proportional to on-screen size.
- Verify material appearance after GLB export in a browser viewer.
