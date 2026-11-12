"""Render final con EEVEE de las previews del modelo melipona.

Uso:
    "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" ^
      --background --python scripts/blender_render_eevee.py

Salidas:
    docs/evidencias/2026-11-04/final-escena.png
    docs/evidencias/2026-11-04/final-abeja.png
    docs/evidencias/2026-11-04/final-jobon.png
    docs/evidencias/2026-11-04/final-interior.png
"""

import math
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
BLEND = ROOT / "assets" / "models" / "modelo.blend"
OUT = ROOT / "docs" / "evidencias" / "2026-11-04"
OUT.mkdir(parents=True, exist_ok=True)

BEE_POS = (0.35, -0.55, 0.58)


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def set_hide(root, hidden):
    for obj in [root] + list(root.children_recursive):
        obj.hide_render = hidden


def hide_prefix(prefix, hidden):
    for obj in bpy.data.objects:
        if obj.name.startswith(prefix):
            obj.hide_render = hidden


def render(scene, path, camera, target, lens):
    camera.data.lens = lens
    look_at(camera, target)
    scene.camera = camera
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)
    print("RENDER", str(path))


def setup_eevee():
    bpy.ops.wm.open_mainfile(filepath=str(BLEND))
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.taa_render_samples = 16
    if hasattr(scene.eevee, "use_gtao"):
        scene.eevee.use_gtao = True
    scene.render.resolution_x = 960
    scene.render.resolution_y = 760
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False

    scene.view_settings.view_transform = "AgX"
    try:
        scene.view_settings.look = "AgX - Medium High Contrast"
    except Exception:
        scene.view_settings.look = "None"
    scene.view_settings.exposure = -0.40

    world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    world.color = (0.82, 0.79, 0.72)
    nodes = world.node_tree.nodes
    nodes.clear()
    background = nodes.new("ShaderNodeBackground")
    background.name = "Studio_Background"
    background.inputs["Color"].default_value = (0.82, 0.79, 0.72, 1.0)
    background.inputs["Strength"].default_value = 0.80
    output = nodes.new("ShaderNodeOutputWorld")
    world.node_tree.links.new(background.outputs["Background"], output.inputs["Surface"])

    floor = bpy.data.materials.get("Piso_Estudio")
    if floor and floor.use_nodes:
        bsdf = floor.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.58, 0.51, 0.42, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.90
    floor_obj = bpy.data.objects.get("Piso_Estudio")
    if floor_obj:
        floor_obj.scale = (100.0, 100.0, 100.0)

    key = bpy.data.objects.get("Luz_Principal")
    if key:
        key.data.energy = 35
        key.data.size = 2.5
        key.data.color = (1.0, 0.92, 0.82)
    fill = bpy.data.objects.get("Luz_Relleno")
    if fill:
        fill.data.energy = 10
        fill.data.size = 3.0
        fill.data.color = (0.82, 0.90, 1.0)
    sun = bpy.data.objects.get("Sol")
    if sun:
        sun.data.energy = 0.25
        sun.data.color = (1.0, 0.95, 0.85)

    bpy.ops.object.light_add(type="AREA", location=(-1.2, 1.4, 1.8))
    rim = bpy.context.object
    rim.name = "Luz_Rim"
    rim.data.energy = 18
    rim.data.size = 2.0
    rim.data.color = (1.0, 0.85, 0.65)
    look_at(rim, (0.0, 0.0, 0.4))

    bpy.ops.object.light_add(type="POINT", location=(0.35, 0.0, 0.40))
    inner = bpy.context.object
    inner.name = "Luz_Interior"
    inner.data.energy = 5
    inner.data.color = (1.0, 0.65, 0.25)
    inner.data.shadow_soft_size = 0.10

    return scene, inner


def main():
    scene, inner = setup_eevee()
    camera = bpy.data.objects.get("Camara")
    bee = bpy.data.objects.get("Abeja")
    jobon = bpy.data.objects.get("Jobon")

    # Acerca las flores al tronco y al eje de cámara para que aparezcan en la toma general.
    for obj in bpy.data.objects:
        if obj.name.startswith("Flor_A"):
            obj.location.x += 0.20
            obj.location.y += 0.35
        elif obj.name.startswith("Flor_B"):
            obj.location.x -= 0.20
            obj.location.y += 0.40

    camera.location = (1.40, -1.80, 1.05)
    render(scene, OUT / "final-escena.png", camera, (0.10, 0.0, 0.28), 55)

    set_hide(jobon, True)
    hide_prefix("Flor_", True)
    bee.location = (0.30, -0.90, 0.55)
    bee.rotation_euler = (0.0, 0.0, math.radians(180.0))
    camera.location = (0.30, -1.40, 0.68)
    render(scene, OUT / "final-abeja.png", camera, (0.30, -0.90, 0.55), 65)
    bee.location = BEE_POS
    bee.rotation_euler = (0.0, 0.0, 0.0)
    set_hide(jobon, False)
    hide_prefix("Flor_", False)

    camera.location = (1.30, -1.50, 0.85)
    render(scene, OUT / "final-jobon.png", camera, (0.20, 0.0, 0.40), 55)

    set_hide(bee, True)
    camera.location = (1.05, -0.60, 0.55)
    render(scene, OUT / "final-interior.png", camera, (0.30, 0.0, 0.40), 50)
    set_hide(bee, False)

    inner.data.energy = 0
    print("EEVEE_OK", bpy.app.version_string)


if __name__ == "__main__":
    main()
