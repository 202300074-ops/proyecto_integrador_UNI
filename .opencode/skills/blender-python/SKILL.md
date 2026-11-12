---
name: blender-python
description: Use when writing or debugging Blender automation with bpy for repeatable modeling, materials, cameras, rendering, reports, and GLB export tasks.
compatibility: opencode
metadata:
  project: melipona-webar
  domain: 3d
---

# Blender Python Automation Specialist

## Requirements
- Use Blender's bundled Python API (`bpy`) and verify API calls against the installed Blender version.
- Prefer small, focused scripts with clear functions and comments.
- Make scripts idempotent where practical: rerunning should not create uncontrolled duplicates.
- Use explicit collection and object names; avoid relying on selection state when possible.
- Include error handling, informative console output, and safe file paths.
- Save backups before destructive operations.

## Typical tasks
- Create named collections and primitive blockouts.
- Set transforms, origins, modifiers, cameras, lights, and materials.
- Batch-check scenes and export selected collections to GLB.
- Generate asset reports: object names, polygon counts, materials, texture dimensions, and file size.

## Safety
Do not overwrite the only project file. Ask before deleting assets or applying destructive changes. Test scripts on a copy first.
