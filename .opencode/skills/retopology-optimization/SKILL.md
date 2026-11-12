---
name: retopology-optimization
description: Use when preparing Blender meshes for efficient real-time mobile and WebAR rendering, including topology cleanup, polygon reduction, and export checks.
compatibility: opencode
metadata:
  project: melipona-webar
  domain: 3d
---

# Retopology and Optimization Specialist

## Target
Optimize stylized assets for mobile browser rendering while preserving their silhouette and visual identity.

## Workflow
1. Inspect topology, normals, non-manifold edges, and unnecessary internal faces.
2. Create a clean low-poly render mesh; preserve a high-poly source only when useful for baking.
3. Use weighted normals/bevels selectively and avoid excessive modifier stacks.
4. Bake high-frequency details into normal/AO maps when appropriate.
5. Reduce material slots, draw calls, texture dimensions, and mesh complexity.
6. Test on a representative phone/browser when possible.

## Export checks
- Apply scale and verify transforms.
- Check triangulation and face orientation.
- Remove hidden or unused objects from export.
- Report polygon counts, material count, texture sizes, and file size.
- Never claim a model is mobile-optimized without checking the exported asset.
