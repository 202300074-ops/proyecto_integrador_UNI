---
name: webar-gltf-pipeline
description: Use when exporting and validating Blender assets as GLB for browser-based augmented reality with A-Frame, MindAR, or WebXR.
compatibility: opencode
metadata:
  project: melipona-webar
  domain: 3d
---

# WebAR and glTF Pipeline Specialist

## Goal
Deliver compact, reliable `.glb` assets from Blender for a browser-based AR experience.

## Pipeline
1. Create a dedicated export collection per asset.
2. Confirm transforms, origins, normals, animation actions, and material compatibility.
3. Remove cameras/lights/helpers unless explicitly required.
4. Export glTF 2.0 binary (`.glb`) with only required objects.
5. Validate the file in a GLB viewer and in the target WebAR implementation.
6. Test on a real mobile browser with camera permissions and realistic network conditions.

## Compatibility
- Prefer standard glTF features and avoid Blender-only shader nodes.
- Check animation clips, texture embedding, transparency, and backface behavior.
- For image tracking, ensure the target image is prepared and tested independently of the 3D model.
- Keep a fallback non-AR preview for devices where AR is unavailable.

## Reporting
Provide file size, object count, triangle count, material count, texture dimensions, and known limitations. Never assume export success means WebAR compatibility.
