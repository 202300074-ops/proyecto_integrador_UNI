"""Modelo estilizado cinematografico de la abeja melipona y el jobon.

Genera la escena editable, los GLB para WebAR/VR y previews de verificacion.
El blockout de `blender_blockout.py` se conserva como respaldo historico.

Uso:
    "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" ^
      --background --python scripts/blender_model.py
"""

import math
import random
import struct
import json
from pathlib import Path

import bpy
import bmesh
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "assets" / "models"
EVIDENCIA = ROOT / "docs" / "evidencias" / "2026-11-04"
MODELS.mkdir(parents=True, exist_ok=True)
EVIDENCIA.mkdir(parents=True, exist_ok=True)

MODELO_BLEND = MODELS / "modelo.blend"
ABEJA_GLB = MODELS / "abeja.glb"
JOBON_GLB = MODELS / "jobon.glb"

BEE_POS = (0.35, -0.55, 0.58)
BEE_ROT_Z = 0.0


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.name = "SakPoKaab"
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.display.shading.light = "STUDIO"
    scene.display.shading.color_type = "MATERIAL"
    scene.display.shading.show_shadows = True
    scene.display.shading.show_cavity = True
    scene.display.shading.cavity_type = "BOTH"
    scene.display.shading.curvature_ridge_factor = 1.6
    scene.display.shading.curvature_valley_factor = 1.2
    scene.display.shading.background_type = "VIEWPORT"
    scene.display.shading.background_color = (0.98, 0.95, 0.88)
    if hasattr(scene.display, "render_aa"):
        scene.display.render_aa = "8"
    scene.render.resolution_x = 1100
    scene.render.resolution_y = 850
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.fps = 24
    scene.frame_start = 1
    scene.frame_end = 13
    scene.cursor.location = (0, 0, 0)
    try:
        scene.view_settings.view_transform = "Standard"
        scene.view_settings.look = "None"
    except Exception:
        pass
    return scene


def make_material(name, color, roughness=0.5, alpha=1.0, metallic=0.0):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, alpha)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = alpha
        if alpha < 1.0:
            for key in ("Transmission Weight", "Transmission"):
                if key in bsdf.inputs:
                    bsdf.inputs[key].default_value = 0.15
                    break
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


def shade_smooth(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()
    obj.select_set(False)


def sphere(name, loc, scale, mat, segments=24, rings=16, smooth=True, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments,
        ring_count=rings,
        radius=1.0,
        location=loc,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    apply_transforms(obj)
    set_material(obj, mat)
    if smooth:
        shade_smooth(obj)
    return obj


def cylinder(
    name,
    loc,
    radius,
    depth,
    mat,
    vertices=20,
    rotation=(0, 0, 0),
    smooth=False,
    end_fill="NGON",
    scale=(1, 1, 1),
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
    obj.scale = scale
    apply_transforms(obj)
    set_material(obj, mat)
    if smooth:
        shade_smooth(obj)
    return obj


def cone(name, loc, radius1, radius2, depth, mat, vertices=12, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(
        vertices=vertices,
        radius1=radius1,
        radius2=radius2,
        depth=depth,
        location=loc,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    apply_transforms(obj)
    set_material(obj, mat)
    return obj


def cube(name, loc, scale, mat):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    apply_transforms(obj)
    set_material(obj, mat)
    return obj


def cylinder_between(name, p1, p2, radius, mat, vertices=10, smooth=True):
    p1 = Vector(p1)
    p2 = Vector(p2)
    direction = p2 - p1
    length = direction.length
    if length <= 1e-9:
        return None
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
    if smooth:
        shade_smooth(obj)
    return obj


def torus(name, loc, major_radius, minor_radius, mat, rotation=(0, 0, 0), scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major_radius,
        minor_radius=minor_radius,
        major_segments=28,
        minor_segments=10,
        location=loc,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    apply_transforms(obj)
    set_material(obj, mat)
    shade_smooth(obj)
    return obj


def new_mesh_object(name, verts, faces, mat, smooth=True):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.validate()
    mesh.update()
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    set_material(obj, mat)
    for poly in mesh.polygons:
        poly.use_smooth = smooth
    return obj


def join_objects(objs, name):
    objs = [o for o in objs if o is not None]
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objs:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    obj = bpy.context.object
    obj.name = name
    bpy.context.scene.cursor.location = (0, 0, 0)
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    bpy.ops.object.select_all(action="DESELECT")
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


def render(scene, path, camera, target, lens=50):
    camera.data.lens = lens
    look_at(camera, target)
    scene.camera = camera
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


def set_hide(root, hidden):
    for obj in [root] + list(root.children_recursive):
        obj.hide_render = hidden


def hide_objects(objs, hidden):
    for obj in objs:
        obj.hide_render = hidden


def triangle_count(obj):
    return sum(max(0, len(poly.vertices) - 2) for poly in obj.data.polygons)


def hierarchy_bounds(root):
    mins = Vector((1e9, 1e9, 1e9))
    maxs = Vector((-1e9, -1e9, -1e9))
    for obj in [root] + list(root.children_recursive):
        if obj.type != "MESH":
            continue
        for corner in obj.bound_box:
            point = obj.matrix_world @ Vector(corner)
            for i in range(3):
                mins[i] = min(mins[i], point[i])
                maxs[i] = max(maxs[i], point[i])
    return maxs - mins


def glb_animation_names(path):
    data = Path(path).read_bytes()
    if len(data) < 20:
        return []
    magic, version, length = struct.unpack_from("<III", data, 0)
    if magic != 0x46546C67:
        return []
    offset = 12
    while offset + 8 <= len(data):
        chunk_length, chunk_type = struct.unpack_from("<II", data, offset)
        offset += 8
        if chunk_type == 0x4E4F534A:
            doc = json.loads(data[offset : offset + chunk_length].decode("utf-8"))
            return [anim.get("name", "") for anim in doc.get("animations", [])]
        offset += chunk_length
    return []


def add_fuzz(parts, name, center, scale, count, mat, seed, length):
    rng = random.Random(seed)
    for i in range(count):
        u = rng.uniform(-1.0, 1.0)
        theta = rng.uniform(0.0, math.tau)
        radius = math.sqrt(max(0.0, 1.0 - u * u))
        direction = Vector(
            (radius * math.cos(theta), radius * math.sin(theta), u)
        )
        point = Vector(
            (
                center[0] + direction.x * scale[0],
                center[1] + direction.y * scale[1],
                center[2] + direction.z * scale[2],
            )
        )
        normal = Vector(
            (
                direction.x / scale[0],
                direction.y / scale[1],
                direction.z / scale[2],
            )
        ).normalized()
        bpy.ops.mesh.primitive_cone_add(
            vertices=3,
            radius1=0.0008,
            radius2=0.0,
            depth=length,
            location=point + normal * length * 0.35,
        )
        obj = bpy.context.object
        obj.name = f"{name}_{i + 1:02d}"
        obj.rotation_mode = "QUATERNION"
        obj.rotation_quaternion = normal.to_track_quat("Z", "Y")
        apply_transforms(obj)
        set_material(obj, mat)
        parts.append(obj)


def pick_abdomen_band(y_norm):
    if y_norm < -0.66:
        return 0
    if y_norm < -0.33:
        return 1
    if y_norm < 0.0:
        return 0
    if y_norm < 0.33:
        return 2
    if y_norm < 0.66:
        return 0
    return 1


def build_wing(name, side, fore, root_loc, ala, vena):
    outline = [
        (0.000, 0.000),
        (0.010, 0.008),
        (0.028, 0.013),
        (0.050, 0.012),
        (0.070, 0.002),
        (0.080, -0.014),
        (0.076, -0.032),
        (0.060, -0.048),
        (0.040, -0.054),
        (0.022, -0.048),
        (0.008, -0.032),
        (0.000, -0.014),
    ]
    factor = 1.0 if fore else 0.62
    verts = [(side * x * factor, y * factor, 0.0) for x, y in outline]
    wing = new_mesh_object(name, verts, [list(range(len(verts)))], ala, smooth=True)
    wing.location = root_loc
    solid = wing.modifiers.new("Grosor", "SOLIDIFY")
    solid.thickness = 0.0008
    bpy.context.view_layer.objects.active = wing
    bpy.ops.object.modifier_apply(modifier=solid.name)

    targets = [(0.070, -0.010), (0.055, -0.032), (0.035, -0.045), (0.020, -0.018)]
    for idx, (tx, ty) in enumerate(targets):
        p1 = (
            root_loc[0] + side * 0.004,
            root_loc[1] - 0.001,
            root_loc[2] + 0.0008,
        )
        p2 = (
            root_loc[0] + side * tx * factor,
            root_loc[1] + ty * factor,
            root_loc[2] + 0.0008,
        )
        vein = cylinder_between(
            f"{name}_Vena_{idx + 1}", p1, p2, 0.0006, vena, vertices=6
        )
        if vein:
            parent_keep(vein, wing)

    base = math.radians(12.0) * side
    amplitude = math.radians(42.0 if fore else 28.0)
    wing.rotation_mode = "XYZ"
    for frame, angle in zip(
        (1, 4, 7, 10, 13),
        (base, base + side * amplitude, base, base - side * amplitude * 0.65, base),
    ):
        wing.rotation_euler = (0.0, angle, 0.0)
        wing.keyframe_insert(data_path="rotation_euler", frame=frame)
    return wing


def build_bee():
    root = bpy.data.objects.new("Abeja", None)
    bpy.context.collection.objects.link(root)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 0.02
    root["descripcion"] = (
        "Abeja melipona estilizada. Modelo de autoria propia refinado en Blender."
    )
    root["escala_exhibicion_m"] = 0.14

    ambar = make_material("Abeja_Ambar", (0.76, 0.40, 0.06), 0.48)
    ambar_claro = make_material("Abeja_Ambar_Claro", (0.90, 0.58, 0.12), 0.44)
    franja = make_material("Abeja_Franja", (0.08, 0.04, 0.02), 0.58)
    torax = make_material("Abeja_Torax", (0.52, 0.28, 0.07), 0.62)
    cabeza = make_material("Abeja_Cabeza", (0.10, 0.05, 0.02), 0.58)
    ojo = make_material("Abeja_Ojo", (0.03, 0.04, 0.05), 0.10)
    brillo = make_material("Abeja_Brillo", (1.0, 0.98, 0.90), 0.08)
    ala = make_material("Abeja_Ala", (0.94, 0.91, 0.82), 0.08, alpha=0.35)
    vena = make_material("Abeja_Vena", (0.40, 0.32, 0.18), 0.55)
    pata = make_material("Abeja_Pata", (0.07, 0.035, 0.015), 0.66)
    pelo = make_material("Abeja_Pelo", (0.90, 0.72, 0.38), 0.82)
    polen = make_material("Abeja_Polen", (0.92, 0.64, 0.08), 0.58)

    body_parts = []

    abdomen = sphere(
        "Abeja_Abdomen",
        (0.0, -0.035, 0.020),
        (0.030, 0.048, 0.034),
        franja,
        segments=28,
        rings=22,
    )
    abdomen.data.materials.clear()
    for mat in (franja, ambar, ambar_claro):
        abdomen.data.materials.append(mat)
    for poly in abdomen.data.polygons:
        y_norm = poly.center.y / 0.048
        poly.material_index = pick_abdomen_band(y_norm)
    body_parts.append(abdomen)

    body_parts.append(
        cone(
            "Abeja_Abdomen_Punta",
            (0.0, -0.082, 0.020),
            0.011,
            0.001,
            0.022,
            franja,
            vertices=12,
            rotation=(math.pi / 2.0, 0.0, 0.0),
        )
    )

    body_parts.append(
        sphere(
            "Abeja_Torax",
            (0.0, 0.022, 0.028),
            (0.028, 0.032, 0.031),
            torax,
            segments=24,
            rings=18,
        )
    )
    body_parts.append(
        sphere(
            "Abeja_Cabeza",
            (0.0, 0.068, 0.028),
            (0.022, 0.020, 0.022),
            cabeza,
            segments=22,
            rings=16,
        )
    )

    for side in (-1, 1):
        body_parts.append(
            sphere(
                f"Abeja_Ojo_{'L' if side < 0 else 'R'}",
                (side * 0.014, 0.072, 0.030),
                (0.006, 0.009, 0.010),
                ojo,
                segments=18,
                rings=12,
                rotation=(0.0, 0.0, math.radians(side * 10.0)),
            )
        )
        body_parts.append(
            sphere(
                f"Abeja_Brillo_{'L' if side < 0 else 'R'}",
                (side * 0.017, 0.078, 0.035),
                (0.0015, 0.0015, 0.0015),
                brillo,
                segments=8,
                rings=6,
            )
        )

    for idx, (x, y, z) in enumerate(
        ((0.0, 0.084, 0.044), (-0.006, 0.080, 0.043), (0.006, 0.080, 0.043))
    ):
        body_parts.append(
            sphere(
                f"Abeja_Ocelo_{idx + 1}",
                (x, y, z),
                (0.0025, 0.0025, 0.0025),
                ojo,
                segments=10,
                rings=8,
            )
        )

    for side in (-1, 1):
        body_parts.append(
            cylinder_between(
                f"Abeja_Mandibula_{'L' if side < 0 else 'R'}",
                (side * 0.006, 0.084, 0.020),
                (side * 0.009, 0.092, 0.012),
                0.0015,
                cabeza,
                vertices=8,
            )
        )

    antenna_points = [
        (0.008, 0.082, 0.034),
        (0.012, 0.092, 0.042),
        (0.014, 0.100, 0.046),
        (0.018, 0.108, 0.044),
        (0.022, 0.114, 0.040),
        (0.025, 0.118, 0.036),
    ]
    for side in (-1, 1):
        points = [(side * x, y, z) for x, y, z in antenna_points]
        for idx in range(len(points) - 1):
            radius = 0.0012 if idx == 0 else 0.0010
            body_parts.append(
                cylinder_between(
                    f"Abeja_Antena_{'L' if side < 0 else 'R'}_{idx + 1}",
                    points[idx],
                    points[idx + 1],
                    radius,
                    pata,
                    vertices=8,
                )
            )
            body_parts.append(
                sphere(
                    f"Abeja_Antena_Union_{'L' if side < 0 else 'R'}_{idx + 1}",
                    points[idx + 1],
                    (0.0018, 0.0018, 0.0018),
                    pata,
                    segments=8,
                    rings=6,
                )
            )

    leg_defs = [
        ((0.014, 0.040, 0.018), (0.030, 0.058, 0.006), (0.040, 0.074, -0.008), (0.045, 0.086, -0.012)),
        ((0.016, 0.024, 0.016), (0.036, 0.026, 0.000), (0.048, 0.020, -0.014), (0.052, 0.014, -0.018)),
        ((0.016, 0.008, 0.016), (0.038, -0.004, 0.000), (0.052, -0.020, -0.014), (0.058, -0.034, -0.018)),
    ]
    for side in (-1, 1):
        for leg_idx, points in enumerate(leg_defs):
            mirrored = [(side * x, y, z) for x, y, z in points]
            for seg_idx in range(3):
                radius = (0.0024, 0.0019, 0.0012)[seg_idx]
                body_parts.append(
                    cylinder_between(
                        f"Abeja_Pata_{'L' if side < 0 else 'R'}_{leg_idx + 1}_{seg_idx + 1}",
                        mirrored[seg_idx],
                        mirrored[seg_idx + 1],
                        radius,
                        pata,
                        vertices=8,
                    )
                )
            for joint_idx in range(1, 4):
                radius = (0.0022, 0.0018, 0.0012)[joint_idx - 1]
                body_parts.append(
                    sphere(
                        f"Abeja_Pata_Union_{'L' if side < 0 else 'R'}_{leg_idx + 1}_{joint_idx}",
                        mirrored[joint_idx],
                        (radius, radius, radius),
                        pata,
                        segments=10,
                        rings=8,
                    )
                )
            if leg_idx == 2:
                tibia_mid = (
                    (mirrored[1][0] + mirrored[2][0]) / 2.0,
                    (mirrored[1][1] + mirrored[2][1]) / 2.0,
                    (mirrored[1][2] + mirrored[2][2]) / 2.0,
                )
                body_parts.append(
                    sphere(
                        f"Abeja_Polen_{'L' if side < 0 else 'R'}",
                        tibia_mid,
                        (0.0050, 0.0065, 0.0050),
                        polen,
                        segments=14,
                        rings=10,
                    )
                )

    add_fuzz(
        body_parts,
        "Abeja_Pelo_Torax",
        (0.0, 0.022, 0.028),
        (0.028, 0.032, 0.031),
        130,
        pelo,
        seed=11,
        length=0.0025,
    )
    add_fuzz(
        body_parts,
        "Abeja_Pelo_Abdomen",
        (0.0, -0.050, 0.020),
        (0.024, 0.030, 0.026),
        40,
        pelo,
        seed=29,
        length=0.0018,
    )

    body = join_objects(body_parts, "Abeja_Cuerpo")
    body.parent = root
    body.matrix_parent_inverse = root.matrix_world.inverted()

    wings = []
    for side in (-1, 1):
        for wing_idx, fore in enumerate((True, False)):
            root_loc = (
                side * (0.018 if fore else 0.016),
                0.030 if fore else 0.008,
                0.052 if fore else 0.049,
            )
            wing = build_wing(
                f"Abeja_Ala_{'L' if side < 0 else 'R'}_{wing_idx + 1}",
                side,
                fore,
                root_loc,
                ala,
                vena,
            )
            wing.parent = root
            wing.matrix_parent_inverse = root.matrix_world.inverted()
            wings.append(wing)

    root.location = BEE_POS
    root.rotation_euler = (0.0, 0.0, BEE_ROT_Z)
    return root


def honeycomb_positions(step=0.048):
    positions = [(0.0, 0.0)]
    for ring in range(1, 3):
        count = 6 * ring
        for k in range(count):
            angle = math.tau * k / count + (math.pi / 6.0 if ring % 2 else 0.0)
            positions.append((step * ring * math.cos(angle), step * ring * math.sin(angle)))
    return positions


def build_log_shell(name, length, radius, segments, rings, bark, interior):
    verts = []
    faces = []
    for i in range(rings + 1):
        x = -length / 2.0 + length * i / rings
        t = i / rings
        for j in range(segments):
            angle = math.tau * j / segments
            r = (
                radius
                + 0.008 * math.sin(9.0 * angle + 2.5 * math.tau * t)
                + 0.005 * math.sin(17.0 * angle - 4.0 * math.tau * t)
                + 0.003 * math.sin(29.0 * angle + 7.0 * math.tau * t)
                + 0.004 * math.sin(5.0 * angle + 1.5 * math.sin(3.0 * math.tau * t))
            )
            verts.append((x, r * math.cos(angle), 0.38 + r * math.sin(angle)))
    for i in range(rings):
        for j in range(segments):
            a = i * segments + j
            b = i * segments + (j + 1) % segments
            c = (i + 1) * segments + (j + 1) % segments
            d = (i + 1) * segments + j
            faces.append((a, b, c, d))
    obj = new_mesh_object(name, verts, faces, bark, smooth=True)
    obj.data.materials.append(interior)
    solid = obj.modifiers.new("Grosor", "SOLIDIFY")
    solid.thickness = 0.035
    solid.offset = -1.0
    solid.material_offset = 1
    solid.material_offset_rim = 0
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=solid.name)
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(35.0))
    for modifier in list(obj.modifiers):
        bpy.ops.object.modifier_apply(modifier=modifier.name)
    return obj


def build_jobon():
    root = bpy.data.objects.new("Jobon", None)
    bpy.context.collection.objects.link(root)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 0.2
    root["descripcion"] = (
        "Jobon maya estilizado de autoria propia, con tronco hueco, panales y soportes."
    )
    root["escala_real_m"] = 1.24

    madera = make_material("Jobon_Madera", (0.42, 0.24, 0.11), 0.72)
    madera_oscura = make_material("Jobon_Madera_Oscura", (0.25, 0.13, 0.06), 0.78)
    corte = make_material("Jobon_Corte", (0.62, 0.42, 0.20), 0.62)
    interior = make_material("Jobon_Interior", (0.12, 0.07, 0.03), 0.85)
    cera = make_material("Jobon_Cera", (0.90, 0.62, 0.16), 0.40)
    panal = make_material("Jobon_Panal", (0.98, 0.72, 0.16), 0.32)
    miel = make_material("Jobon_Miel", (0.99, 0.60, 0.02), 0.16)

    parts = []

    parts.append(
        build_log_shell(
            "Jobon_Tronco",
            length=1.20,
            radius=0.22,
            segments=64,
            rings=22,
            bark=madera,
            interior=interior,
        )
    )

    parts.append(
        sphere(
            "Jobon_Nudo_A",
            (-0.35, -0.225, 0.42),
            (0.045, 0.015, 0.030),
            madera_oscura,
            segments=18,
            rings=12,
        )
    )
    parts.append(
        sphere(
            "Jobon_Nudo_B",
            (0.08, -0.228, 0.33),
            (0.035, 0.012, 0.024),
            madera_oscura,
            segments=18,
            rings=12,
        )
    )

    parts.append(
        cylinder(
            "Jobon_Tapa_Fondo",
            (-0.60, 0.0, 0.38),
            0.225,
            0.030,
            corte,
            vertices=40,
            rotation=(0.0, math.pi / 2.0, 0.0),
            smooth=False,
            end_fill="NGON",
        )
    )
    parts.append(
        torus(
            "Jobon_Borde_Fondo",
            (-0.60, 0.0, 0.38),
            0.208,
            0.016,
            corte,
            rotation=(0.0, math.pi / 2.0, 0.0),
        )
    )
    parts.append(
        torus(
            "Jobon_Borde_Boca",
            (0.60, 0.0, 0.38),
            0.208,
            0.018,
            corte,
            rotation=(0.0, math.pi / 2.0, 0.0),
        )
    )

    for disc_idx, x in enumerate((0.15, 0.32, 0.49)):
        parts.append(
            cylinder(
                f"Jobon_Cera_Disco_{disc_idx + 1}",
                (x, 0.0, 0.38),
                0.150,
                0.012,
                cera,
                vertices=36,
                rotation=(0.0, math.pi / 2.0, 0.0),
                smooth=False,
                end_fill="NGON",
            )
        )
        parts.append(
            torus(
                f"Jobon_Cera_Borde_{disc_idx + 1}",
                (x, 0.0, 0.38),
                0.150,
                0.008,
                cera,
                rotation=(0.0, math.pi / 2.0, 0.0),
            )
        )
        for cell_idx, (dy, dz) in enumerate(honeycomb_positions()):
            parts.append(
                cylinder(
                    f"Jobon_Celda_{disc_idx + 1}_{cell_idx + 1}",
                    (x + 0.008, dy, 0.38 + dz),
                    0.024,
                    0.008,
                    panal,
                    vertices=6,
                    rotation=(0.0, math.pi / 2.0, 0.0),
                    smooth=False,
                    end_fill="NGON",
                )
            )
            if cell_idx % 3 == 0:
                parts.append(
                    cylinder(
                        f"Jobon_Miel_Celda_{disc_idx + 1}_{cell_idx + 1}",
                        (x + 0.013, dy, 0.38 + dz),
                        0.017,
                        0.006,
                        miel,
                        vertices=6,
                        rotation=(0.0, math.pi / 2.0, 0.0),
                        smooth=False,
                        end_fill="NGON",
                    )
                )
        for drop_idx, dy in enumerate((-0.10, 0.0, 0.10)):
            parts.append(
                sphere(
                    f"Jobon_Gota_{disc_idx + 1}_{drop_idx + 1}",
                    (x + 0.016, dy, 0.235),
                    (0.007, 0.010, 0.017),
                    miel,
                    segments=12,
                    rings=8,
                )
            )

    parts.append(
        cylinder(
            "Jobon_Piquera_Placa",
            (0.28, -0.226, 0.44),
            0.062,
            0.012,
            corte,
            vertices=28,
            rotation=(math.pi / 2.0, 0.0, 0.0),
            smooth=False,
            end_fill="NGON",
            scale=(0.65, 1.12, 1.0),
        )
    )
    parts.append(
        sphere(
            "Jobon_Piquera",
            (0.28, -0.233, 0.44),
            (0.032, 0.006, 0.050),
            interior,
            segments=20,
            rings=14,
        )
    )
    parts.append(
        cylinder(
            "Jobon_Piquera_Plataforma",
            (0.28, -0.255, 0.375),
            0.050,
            0.008,
            corte,
            vertices=20,
            smooth=False,
            end_fill="NGON",
        )
    )

    for side, x in (("A", -0.38), ("B", 0.38)):
        parts.append(
            cylinder(
                f"Jobon_Soporte_{side}_Base",
                (x, 0.0, 0.025),
                0.160,
                0.050,
                madera_oscura,
                vertices=12,
                smooth=False,
                end_fill="NGON",
                scale=(0.80, 1.40, 1.0),
            )
        )
        parts.append(
            cylinder(
                f"Jobon_Soporte_{side}_Poste",
                (x, 0.0, 0.110),
                0.055,
                0.200,
                madera_oscura,
                vertices=12,
                smooth=True,
            )
        )
        parts.append(
            cylinder_between(
                f"Jobon_Soporte_{side}_Cuna_A",
                (x, -0.18, 0.18),
                (x, -0.08, 0.15),
                0.022,
                corte,
                vertices=10,
            )
        )
        parts.append(
            cylinder_between(
                f"Jobon_Soporte_{side}_Cuna_B",
                (x, 0.18, 0.18),
                (x, 0.08, 0.15),
                0.022,
                corte,
                vertices=10,
            )
        )

    parts.append(
        cylinder(
            "Jobon_Tapa_Suelta",
            (-0.62, 0.40, 0.19),
            0.185,
            0.032,
            corte,
            vertices=36,
            rotation=(math.radians(78.0), 0.0, math.radians(-18.0)),
            smooth=False,
            end_fill="NGON",
        )
    )
    parts.append(
        torus(
            "Jobon_Tapa_Asa",
            (-0.62, 0.425, 0.19),
            0.040,
            0.008,
            madera_oscura,
            rotation=(math.radians(78.0), 0.0, math.radians(-18.0)),
        )
    )

    jobon = join_objects(parts, "Jobon_Estructura")
    jobon.parent = root
    jobon.matrix_parent_inverse = root.matrix_world.inverted()
    return root


def build_flower(name, loc, stem_mat, petal_mat, center_mat, leaf_mat):
    x, y, z = loc
    parts = [
        cylinder_between(
            f"{name}_Tallo",
            (x, y, z),
            (x, y, z + 0.28),
            0.006,
            stem_mat,
            vertices=8,
        )
    ]
    for idx in range(5):
        angle = math.tau * idx / 5.0
        parts.append(
            sphere(
                f"{name}_Petalo_{idx + 1}",
                (x + 0.030 * math.cos(angle), y + 0.030 * math.sin(angle), z + 0.28),
                (0.032, 0.016, 0.007),
                petal_mat,
                segments=16,
                rings=10,
                rotation=(0.0, 0.0, angle),
            )
        )
    parts.append(
        sphere(
            f"{name}_Centro",
            (x, y, z + 0.285),
            (0.014, 0.014, 0.009),
            center_mat,
            segments=14,
            rings=10,
        )
    )
    parts.append(
        sphere(
            f"{name}_Hoja",
            (x + 0.022, y, z + 0.13),
            (0.045, 0.016, 0.005),
            leaf_mat,
            segments=14,
            rings=8,
            rotation=(0.0, 0.0, math.radians(25.0)),
        )
    )
    return parts


def setup_scene():
    scene = reset_scene()
    jobon = build_jobon()
    bee = build_bee()

    floor_mat = make_material("Piso_Estudio", (0.80, 0.72, 0.60), 0.90)
    bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, 0))
    floor = bpy.context.object
    floor.name = "Piso_Estudio"
    set_material(floor, floor_mat)

    stem_mat = make_material("Flor_Tallo", (0.18, 0.35, 0.10), 0.7)
    petal_mat = make_material("Flor_Petalo", (0.98, 0.86, 0.55), 0.55)
    center_mat = make_material("Flor_Centro", (0.90, 0.55, 0.06), 0.5)
    leaf_mat = make_material("Flor_Hoja", (0.22, 0.42, 0.12), 0.7)
    flowers = []
    flowers += build_flower("Flor_A", (-0.55, -0.80, 0.0), stem_mat, petal_mat, center_mat, leaf_mat)
    flowers += build_flower("Flor_B", (0.70, -1.00, 0.0), stem_mat, petal_mat, center_mat, leaf_mat)

    bpy.ops.object.camera_add(location=(1.55, -1.95, 1.15))
    camera = bpy.context.object
    camera.name = "Camara"
    camera.data.lens = 50

    bpy.ops.object.light_add(type="AREA", location=(1.5, -1.5, 2.5))
    key = bpy.context.object
    key.name = "Luz_Principal"
    key.data.energy = 350
    key.data.size = 2.0
    look_at(key, (0.0, 0.0, 0.4))

    bpy.ops.object.light_add(type="AREA", location=(-1.5, 1.0, 1.5))
    fill = bpy.context.object
    fill.name = "Luz_Relleno"
    fill.data.energy = 130
    fill.data.size = 2.0
    look_at(fill, (0.0, 0.0, 0.4))

    bpy.ops.object.light_add(type="SUN", location=(0.0, 0.0, 4.0))
    sun = bpy.context.object
    sun.name = "Sol"
    sun.data.energy = 2.0
    sun.rotation_euler = (math.radians(30.0), 0.0, math.radians(20.0))

    return scene, jobon, bee, camera, flowers


def main():
    scene, jobon, bee, camera, flowers = setup_scene()

    camera.location = (1.40, -1.80, 1.05)
    render(
        scene,
        EVIDENCIA / "modelo-escena.png",
        camera,
        (0.10, 0.0, 0.40),
        lens=55,
    )

    set_hide(jobon, True)
    hide_objects(flowers, True)
    bee.location = (0.30, -0.90, 0.55)
    bee.rotation_euler = (0.0, 0.0, math.radians(180.0))
    camera.location = (0.30, -1.40, 0.68)
    render(
        scene,
        EVIDENCIA / "modelo-abeja.png",
        camera,
        (0.30, -0.90, 0.55),
        lens=65,
    )
    bee.location = BEE_POS
    bee.rotation_euler = (0.0, 0.0, BEE_ROT_Z)
    set_hide(jobon, False)
    hide_objects(flowers, False)

    camera.location = (1.30, -1.50, 0.85)
    render(
        scene,
        EVIDENCIA / "modelo-jobon.png",
        camera,
        (0.20, 0.0, 0.40),
        lens=55,
    )

    set_hide(bee, True)
    camera.location = (1.05, -0.60, 0.55)
    render(
        scene,
        EVIDENCIA / "modelo-interior.png",
        camera,
        (0.30, 0.0, 0.40),
        lens=50,
    )
    set_hide(bee, False)

    camera.location = (1.40, -1.80, 1.05)
    render(
        scene,
        EVIDENCIA / "modelo-escena.png",
        camera,
        (0.10, 0.0, 0.40),
        lens=55,
    )

    bpy.ops.wm.save_as_mainfile(filepath=str(MODELO_BLEND))

    bee.location = (0.0, 0.0, 0.0)
    bee.rotation_euler = (0.0, 0.0, 0.0)
    select_hierarchy(bee)
    bpy.ops.export_scene.gltf(
        filepath=str(ABEJA_GLB),
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_animations=True,
        export_animation_mode="SCENE",
        export_anim_scene_split_object=False,
        export_frame_range=True,
    )
    bee.location = BEE_POS
    bee.rotation_euler = (0.0, 0.0, BEE_ROT_Z)

    select_hierarchy(jobon)
    bpy.ops.export_scene.gltf(
        filepath=str(JOBON_GLB),
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_animations=False,
    )

    bee_bounds = hierarchy_bounds(bee)
    jobon_bounds = hierarchy_bounds(jobon)
    bee_tris = sum(triangle_count(o) for o in [bee] + list(bee.children_recursive) if o.type == "MESH")
    jobon_tris = sum(
        triangle_count(o) for o in [jobon] + list(jobon.children_recursive) if o.type == "MESH"
    )

    print("BLENDER_VERSION", bpy.app.version_string)
    print("MODELO_BLEND", str(MODELO_BLEND))
    print("ABEJA_GLB", str(ABEJA_GLB), ABEJA_GLB.stat().st_size)
    print("JOBON_GLB", str(JOBON_GLB), JOBON_GLB.stat().st_size)
    print("ABEJA_TRIANGULOS", bee_tris)
    print("JOBON_TRIANGULOS", jobon_tris)
    print("ABEJA_DIMENSIONES_M", tuple(round(v, 4) for v in bee_bounds))
    print("JOBON_DIMENSIONES_M", tuple(round(v, 4) for v in jobon_bounds))
    print("ABEJA_ANIMACIONES", glb_animation_names(ABEJA_GLB))
    print("JOBON_ANIMACIONES", glb_animation_names(JOBON_GLB))


if __name__ == "__main__":
    main()
