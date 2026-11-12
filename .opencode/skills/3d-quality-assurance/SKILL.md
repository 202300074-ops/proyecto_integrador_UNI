---
name: 3d-quality-assurance
description: Use when reviewing 3D assets and scenes before presentation, GLB export, or WebAR integration, with a measurable pass/fail checklist.
compatibility: opencode
metadata:
  project: melipona-webar
  domain: 3d
---

# 3D Quality Assurance

## Review checklist
- [ ] Asset matches the approved visual direction and reference.
- [ ] Silhouette and proportions read clearly at phone size.
- [ ] Object names, collections, origins, and transforms are clean.
- [ ] Normals and topology are checked.
- [ ] Materials use supported glTF-compatible properties.
- [ ] No missing textures or external dependencies.
- [ ] Animation starts correctly and has sensible timing.
- [ ] GLB opens in an independent viewer.
- [ ] Asset tested in the actual WebAR page on a mobile device.
- [ ] File size and geometry are appropriate for the target device.
- [ ] Student can explain the modeling, material, animation, and export decisions.

## Review output
Return: blockers, warnings, measured stats, recommended fixes, and a clear pass/fail decision. Do not mark pass when a required test was not performed.
