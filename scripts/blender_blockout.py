"""Blockout low-poly de la abeja melipona y el jobón.

Este script genera una base para trabajar en Blender. No es el modelo final:
sirve para fijar proporciones, materiales y escala. El refinado manual, las
texturas y la animación se hacen en Blender y se documentan como autoría propia.

Uso:
    "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" ^
      --background --python scripts/blender_blockout.py

Salidas:
    assets/models/blockout.blend
    assets/models/abeja.glb
    assets/models/jobon.glb
    docs/evidencias/2026-11-04/blockout-escena.png
    docs/evidencias/2026-11-04/blockout-abeja.png
    docs/evidencias/2026-11-04/blockout-jobon.png
"""

import math
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "assets" / "models"
EVIDENCIA = ROOT / "docs" / "evidencias" / "2026-11-04"
MODELS.mkdir(parents=True, exist_ok=True)
EVIDENCIA.mkdir(parents=True, exist_ok=True)


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.display.shading.light = "STUDIO"
    scene.display.shading.color_type = "MATERIAL"
    scene.display.shading.show_shadows = True
    scene.display.shading.show_cavity = True
    scene.display.shading.cavity_type = "BOTH"
    scene.display.shading.background_type = "VIEWPORT"
    scene.display.shading.background_color = (0.96, 0.93, 0.86)
    scene.render.resolution_x = 900
    scene.render.resolution_y = 700
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    return scene


def make_material(name, color, roughness=0.5, alpha=1.0):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, alpha)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    if "Alpha" in bsdf.inputs:
        bsdf.inputs["Alpha"].default_value = alpha
    if alpha < 1.0:
        if hasattr(mat, "blend_method"):
            mat.blend_method = "BLEND"
        if hasattr(mat, "surface_render_method"):
            mat.surface_render_method = "DITHERED"
    return mat


def set_material(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def apply_transforms(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.select_set(False)


def sphere(name, loc, scale, mat, segments=20, rings=12, smooth=True):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments, ring_count=rings, radius=1.0, location=loc
    )
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    apply_transforms(obj)
    set_material(obj, mat)
    if smooth:
        bpy.ops.object.shade_smooth()
    return obj


def cylinder(
    name,
    loc,
    radius,
    depth,
    mat,
    vertices=16,
    rotation=(0, 0, 0),
    smooth=False,
    end_fill="NGON",
):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        end_fill_type=end_fill,
        location=loc,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    apply_transforms(obj)
    set_material(obj, mat)
    if smooth:
        bpy.ops.object.shade_smooth()
    return obj


def cube(name, loc, scale, mat):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    apply_transforms(obj)
    set_material(obj, mat)
    return obj


def cylinder_between(name, p1, p2, radius, mat, vertices=10):
    p1 = Vector(p1)
    p2 = Vector(p2)
    direction = p2 - p1
    length = direction.length
    midpoint = (p1 + p2) / 2
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices, radius=radius, depth=length, location=midpoint
    )
    obj = bpy.context.object
    obj.name = name
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = direction.to_track_quat("Z", "Y")
    apply_transforms(obj)
    set_material(obj, mat)
    return obj


def torus(name, loc, major_radius, minor_radius, mat, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major_radius,
        minor_radius=minor_radius,
        major_segments=20,
        minor_segments=8,
        location=loc,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    apply_transforms(obj)
    set_material(obj, mat)
    bpy.ops.object.shade_smooth()
    return obj


def parent_keep(obj, parent):
    obj.parent = parent
    obj.matrix_parent_inverse = parent.matrix_world.inverted()


def select_hierarchy(root):
    bpy.ops.object.select_all(action="DESELECT")
    root.select_set(True)
    for child in root.children_recursive:
        child.select_set(True)
    bpy.context.view_layer.objects.active = root


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def render(scene, path, camera, target):
    look_at(camera, target)
    scene.camera = camera
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


def build_bee():
    empty = bpy.data.objects.new("Abeja", None)
    bpy.context.collection.objects.link(empty)
    empty.empty_display_type = "PLAIN_AXES"
    empty.empty_display_size = 0.02
    empty["descripcion"] = (
        "Blockout low-poly de Melipona beecheii. Refinar, texturizar y animar "
        "manualmente en Blender."
    )

    ambar = make_material("Abeja_Ambar", (0.82, 0.48, 0.10), 0.45)
    franja = make_material("Abeja_Franja", (0.16, 0.08, 0.04), 0.6)
    torax = make_material("Abeja_Torax", (0.70, 0.42, 0.10), 0.7)
    cabeza = make_material("Abeja_Cabeza", (0.20, 0.10, 0.05), 0.6)
    ojo = make_material("Abeja_Ojo", (0.02, 0.02, 0.02), 0.2)
    ala = make_material("Abeja_Ala", (0.95, 0.90, 0.75), 0.25, alpha=0.45)
    pata = make_material("Abeja_Pata", (0.12, 0.06, 0.03), 0.7)

    parts = []

    parts.append(
        sphere("Abeja_Abdomen", (0, -0.030, 0.018), (0.025, 0.040, 0.028), ambar)
    )

    for i, y in enumerate((-0.055, -0.035, -0.015)):
        rel = (y - (-0.030)) / 0.040
        factor = math.sqrt(max(0.0, 1.0 - rel * rel))
        parts.append(
            sphere(
                f"Abeja_Franja_{i + 1}",
                (0, y, 0.018),
                (0.026 * factor, 0.005, 0.029 * factor),
                franja,
                segments=20,
                rings=8,
            )
        )

    parts.append(
        sphere("Abeja_Torax", (0, 0.020, 0.022), (0.022, 0.026, 0.024), torax)
    )
    parts.append(
        sphere("Abeja_Cabeza", (0, 0.058, 0.022), (0.018, 0.016, 0.018), cabeza)
    )

    for side in (-1, 1):
        parts.append(
            sphere(
                f"Abeja_Ojo_{'L' if side < 0 else 'R'}",
                (side * 0.012, 0.064, 0.028),
                (0.006, 0.005, 0.006),
                ojo,
                segments=12,
                rings=8,
            )
        )

    for side in (-1, 1):
        base = (side * 0.008, 0.068, 0.030)
        tip = (side * 0.018, 0.088, 0.046)
        parts.append(
            cylinder_between(
                f"Abeja_Antena_{'L' if side < 0 else 'R'}",
                base,
                tip,
                0.0012,
                pata,
                vertices=8,
            )
        )
        parts.append(
            sphere(
                f"Abeja_Antena_Punta_{'L' if side < 0 else 'R'}",
                tip,
                (0.002, 0.002, 0.002),
                pata,
                segments=8,
                rings=6,
            )
        )

    leg_defs = [
        ((0.012, 0.030, 0.010), (0.032, 0.045, -0.018)),
        ((0.014, 0.015, 0.010), (0.036, 0.012, -0.022)),
        ((0.014, -0.010, 0.010), (0.036, -0.030, -0.022)),
    ]
    for side in (-1, 1):
        for i, (a, b) in enumerate(leg_defs):
            parts.append(
                cylinder_between(
                    f"Abeja_Pata_{'L' if side < 0 else 'R'}_{i + 1}",
                    (side * a[0], a[1], a[2]),
                    (side * b[0], b[1], b[2]),
                    0.0015,
                    pata,
                    vertices=8,
                )
            )

    wing_defs = [
        ((0.030, -0.025, 0.042), (1.0, 1.5, 1.0), 28, 0.032),
        ((0.026, -0.045, 0.038), (0.7, 1.1, 1.0), 42, 0.024),
    ]
    for side in (-1, 1):
        for i, (loc, scale, angle, radius) in enumerate(wing_defs):
            bpy.ops.mesh.primitive_circle_add(
                vertices=16,
                radius=radius,
                fill_type="NGON",
                location=(side * loc[0], loc[1], loc[2]),
            )
            obj = bpy.context.object
            obj.name = f"Abeja_Ala_{'L' if side < 0 else 'R'}_{i + 1}"
            obj.scale = scale
            obj.rotation_euler = (math.radians(-8), 0, math.radians(side * angle))
            apply_transforms(obj)
            set_material(obj, ala)
            solid = obj.modifiers.new("Grosor", "SOLIDIFY")
            solid.thickness = 0.0008
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.modifier_apply(modifier=solid.name)
            parts.append(obj)

    for obj in parts:
        parent_keep(obj, empty)

    empty.location = (0.25, -0.05, 0.60)
    return empty


def build_jobon():
    empty = bpy.data.objects.new("Jobon", None)
    bpy.context.collection.objects.link(empty)
    empty.empty_display_type = "PLAIN_AXES"
    empty.empty_display_size = 0.2
    empty["descripcion"] = (
        "Blockout low-poly de un jobón maya: tronco hueco, panales y soportes. "
        "Refinar y texturizar manualmente en Blender."
    )

    madera = make_material("Jobon_Madera", (0.42, 0.24, 0.11), 0.65)
    madera_oscura = make_material("Jobon_Madera_Oscura", (0.28, 0.15, 0.07), 0.7)
    interior = make_material("Jobon_Interior", (0.18, 0.10, 0.05), 0.8)
    panal = make_material("Jobon_Panal", (0.92, 0.62, 0.10), 0.35)
    cera = make_material("Jobon_Cera", (0.70, 0.40, 0.06), 0.5)

    parts = []

    tronco = cylinder(
        "Jobon_Tronco",
        (0, 0, 0.35),
        0.22,
        1.20,
        madera,
        vertices=20,
        rotation=(0, math.pi / 2, 0),
        smooth=True,
        end_fill="NOTHING",
    )
    solid = tronco.modifiers.new("Grosor", "SOLIDIFY")
    solid.thickness = 0.03
    solid.offset = -1
    bpy.context.view_layer.objects.active = tronco
    bpy.ops.object.modifier_apply(modifier=solid.name)
    parts.append(tronco)

    parts.append(
        cylinder(
            "Jobon_Interior_Tronco",
            (0, 0, 0.35),
            0.185,
            1.18,
            interior,
            vertices=20,
            rotation=(0, math.pi / 2, 0),
            smooth=True,
            end_fill="NOTHING",
        )
    )

    for x in (-0.60, 0.60):
        parts.append(
            torus(
                f"Jobon_Borde_{'A' if x < 0 else 'B'}",
                (x, 0, 0.35),
                0.205,
                0.020,
                madera_oscura,
                rotation=(0, math.pi / 2, 0),
            )
        )

    for i, x in enumerate((-0.25, 0.10, 0.48)):
        parts.append(
            cylinder(
                f"Jobon_Panal_Base_{i + 1}",
                (x, 0, 0.35),
                0.17,
                0.012,
                cera,
                vertices=20,
                rotation=(0, math.pi / 2, 0),
                smooth=False,
                end_fill="NGON",
            )
        )
        positions = [(0, 0)]
        for ring in range(1, 3):
            for k in range(6):
                angle = math.radians(60 * k)
                positions.append(
                    (0.045 * ring * math.cos(angle), 0.045 * ring * math.sin(angle))
                )
        for j, (dy, dz) in enumerate(positions):
            parts.append(
                cylinder(
                    f"Jobon_Celda_{i + 1}_{j + 1}",
                    (x + 0.008, dy, 0.35 + dz),
                    0.025,
                    0.010,
                    panal,
                    vertices=6,
                    rotation=(0, math.pi / 2, 0),
                    smooth=False,
                    end_fill="NGON",
                )
            )

    for x in (-0.40, 0.40):
        parts.append(
            cube(
                f"Jobon_Soporte_{'A' if x < 0 else 'B'}",
                (x, 0, 0.065),
                (0.12, 0.34, 0.13),
                madera_oscura,
            )
        )

    for obj in parts:
        parent_keep(obj, empty)

    return empty


def setup_scene():
    scene = reset_scene()
    jobon = build_jobon()
    bee = build_bee()

    bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, 0))
    floor = bpy.context.object
    floor.name = "Piso_Estudio"
    set_material(floor, make_material("Piso", (0.88, 0.84, 0.76), 0.8))

    bpy.ops.object.camera_add(location=(1.6, -1.8, 1.2))
    camera = bpy.context.object
    camera.name = "Camara"
    camera.data.lens = 55
    scene.camera = camera

    bpy.ops.object.light_add(type="AREA", location=(1.5, -1.5, 2.5))
    key = bpy.context.object
    key.name = "Luz_Principal"
    key.data.energy = 300
    key.data.size = 2.0
    look_at(key, (0, 0, 0.4))

    bpy.ops.object.light_add(type="AREA", location=(-1.5, 1.0, 1.5))
    fill = bpy.context.object
    fill.name = "Luz_Relleno"
    fill.data.energy = 120
    fill.data.size = 2.0
    look_at(fill, (0, 0, 0.4))

    bpy.ops.object.light_add(type="SUN", location=(0, 0, 4))
    sun = bpy.context.object
    sun.name = "Sol"
    sun.data.energy = 2.0
    sun.rotation_euler = (math.radians(30), 0, math.radians(20))

    return scene, jobon, bee, camera


def main():
    scene, jobon, bee, camera = setup_scene()

    camera.location = (1.6, -1.8, 1.2)
    camera.data.lens = 55
    render(scene, EVIDENCIA / "blockout-escena.png", camera, (0, 0, 0.35))

    camera.location = (0.55, 0.22, 0.82)
    camera.data.lens = 55
    render(scene, EVIDENCIA / "blockout-abeja.png", camera, (0.25, -0.05, 0.60))

    camera.location = (1.45, -1.65, 0.95)
    camera.data.lens = 50
    render(scene, EVIDENCIA / "blockout-jobon.png", camera, (0, 0, 0.35))

    bpy.ops.wm.save_as_mainfile(filepath=str(MODELS / "blockout.blend"))

    bee.location = (0, 0, 0)
    select_hierarchy(bee)
    bpy.ops.export_scene.gltf(
        filepath=str(MODELS / "abeja.glb"),
        export_format="GLB",
        use_selection=True,
        export_apply=True,
    )
    bee.location = (0.25, -0.05, 0.60)

    select_hierarchy(jobon)
    bpy.ops.export_scene.gltf(
        filepath=str(MODELS / "jobon.glb"),
        export_format="GLB",
        use_selection=True,
        export_apply=True,
    )

    print("BLENDER_VERSION", bpy.app.version_string)
    print("MODELOS", str(MODELS))
    print("EVIDENCIA", str(EVIDENCIA))
    print("ABEJA_OBJETOS", len(bee.children_recursive) + 1)
    print("JOBON_OBJETOS", len(jobon.children_recursive) + 1)


if __name__ == "__main__":
    main()
