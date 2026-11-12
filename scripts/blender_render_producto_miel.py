"""Render de prueba del frasco de miel, estilo fotografia de producto.

Uso:
    "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" ^
      --background --python scripts/blender_render_producto_miel.py

Salidas:
    assets/models/producto-miel.blend
    docs/evidencias/2026-11-10/producto-miel-prueba.png
"""

import math
import os
import time
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "assets" / "models"
OUT = ROOT / "docs" / "evidencias" / "2026-11-10"
MODELS.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

BLEND = MODELS / "producto-miel.blend"
WIDTH = int(os.environ.get("PRODUCT_WIDTH", "760"))
HEIGHT = int(os.environ.get("PRODUCT_HEIGHT", "950"))
SAMPLES = int(os.environ.get("PRODUCT_SAMPLES", "32"))
RENDER = OUT / f"{os.environ.get('PRODUCT_NAME', 'producto-miel-prueba')}.png"


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def set_input(node, names, value):
    for name in names:
        if name in node.inputs:
            node.inputs[name].default_value = value
            return


def material(name, color, roughness=0.5, metallic=0.0, transmission=0.0, ior=1.45, coat=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.diffuse_color = (*color, 1.0)
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_input(bsdf, ("Base Color",), (*color, 1.0))
    set_input(bsdf, ("Roughness",), roughness)
    set_input(bsdf, ("Metallic",), metallic)
    set_input(bsdf, ("IOR",), ior)
    set_input(bsdf, ("Transmission Weight", "Transmission"), transmission)
    set_input(bsdf, ("Coat Weight", "Clearcoat"), coat)
    return mat


def add_material(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def smooth(obj):
    for poly in obj.data.polygons:
        poly.use_smooth = True


def bevel(obj, width, segments=3):
    mod = obj.modifiers.new("Bevel", "BEVEL")
    mod.width = width
    mod.segments = segments
    mod.limit_method = "ANGLE"
    mod.angle_limit = math.radians(35)
    return mod


def cylinder(name, radius, depth, location, mat, vertices=96, fill="NGON"):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        end_fill_type=fill,
        location=location,
    )
    obj = bpy.context.object
    obj.name = name
    add_material(obj, mat)
    smooth(obj)
    return obj


def text(name, body, size, location, mat, extrude=0.00015):
    curve = bpy.data.curves.new(name, type="FONT")
    curve.body = body
    curve.size = size
    curve.align_x = "CENTER"
    curve.align_y = "CENTER"
    curve.extrude = extrude
    curve.bevel_depth = 0.00004
    curve.bevel_resolution = 1
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (math.pi / 2, 0, 0)
    add_material(obj, mat)
    return obj


def make_cyclorama(mat):
    profile = [
        (-1.20, 0.0),
        (0.30, 0.0),
        (0.37, 0.005),
        (0.43, 0.020),
        (0.48, 0.045),
        (0.52, 0.080),
        (0.55, 0.130),
        (0.57, 0.190),
        (0.58, 0.260),
        (0.58, 1.20),
    ]
    xs = (-2.0, 2.0)
    verts = []
    for x in xs:
        for y, z in profile:
            verts.append((x, y, z))
    n = len(profile)
    faces = []
    for i in range(n - 1):
        faces.append((i, i + 1, n + i + 1, n + i))
    mesh = bpy.data.meshes.new("Ciclorama_Malla")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("Ciclorama", mesh)
    bpy.context.collection.objects.link(obj)
    add_material(obj, mat)
    return obj


def make_jar_shell(mat):
    profile = [
        (0.0550, 0.0000),
        (0.0550, 0.1320),
        (0.0548, 0.1380),
        (0.0532, 0.1440),
        (0.0498, 0.1490),
        (0.0458, 0.1535),
        (0.0435, 0.1575),
        (0.0435, 0.1600),
        (0.0450, 0.1615),
    ]
    segments = 96
    verts = []
    for radius, z in profile:
        for j in range(segments):
            angle = 2 * math.pi * j / segments
            verts.append((radius * math.cos(angle), radius * math.sin(angle), z))
    faces = []
    for i in range(len(profile) - 1):
        for j in range(segments):
            a = i * segments + j
            b = i * segments + (j + 1) % segments
            c = (i + 1) * segments + (j + 1) % segments
            d = (i + 1) * segments + j
            faces.append((a, b, c, d))
    mesh = bpy.data.meshes.new("Frasco_Malla")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("Frasco_Vidrio", mesh)
    bpy.context.collection.objects.link(obj)
    add_material(obj, mat)
    smooth(obj)
    solid = obj.modifiers.new("Grosor_Vidrio", "SOLIDIFY")
    solid.thickness = 0.003
    solid.offset = -1.0
    bevel(obj, 0.0012, 3)
    return obj


def make_label(mat):
    radius = 0.0567
    z0, z1 = 0.043, 0.116
    steps = 24
    start, end = math.radians(-62), math.radians(62)
    verts = []
    for i in range(steps + 1):
        a = start + (end - start) * i / steps
        x = radius * math.sin(a)
        y = -radius * math.cos(a)
        verts.append((x, y, z0))
        verts.append((x, y, z1))
    faces = []
    for i in range(steps):
        a = i * 2
        faces.append((a, a + 1, a + 3, a + 2))
    mesh = bpy.data.meshes.new("Etiqueta_Malla")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("Etiqueta", mesh)
    bpy.context.collection.objects.link(obj)
    add_material(obj, mat)
    solid = obj.modifiers.new("Grosor", "SOLIDIFY")
    solid.thickness = 0.0007
    solid.offset = 1.0
    return obj


def make_honey_dipper(wood, honey_mat):
    handle = cylinder(
        "Cuchara_Miel_Mango",
        0.0042,
        0.205,
        (0.083, -0.018, 0.1025),
        wood,
        vertices=32,
    )
    handle.rotation_euler = (0, math.radians(12), 0)
    bevel(handle, 0.0012, 2)
    lean = math.radians(12)
    for i in range(6):
        z = 0.145 + i * 0.008
        bpy.ops.mesh.primitive_torus_add(
            major_radius=0.0082 - i * 0.00035,
            minor_radius=0.00175,
            major_segments=32,
            minor_segments=8,
            location=(0.083 + math.sin(lean) * (z - 0.1025), -0.018, z),
            rotation=(0, lean, 0),
        )
        ring = bpy.context.object
        ring.name = f"Cuchara_Miel_Anillo_{i + 1}"
        add_material(ring, wood)
        smooth(ring)
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=32,
        ring_count=16,
        radius=0.0085,
        location=(0.083 + math.sin(lean) * (0.1945 - 0.1025), -0.018, 0.1945),
    )
    tip = bpy.context.object
    tip.name = "Cuchara_Miel_Punta"
    tip.scale = (1.0, 0.85, 0.55)
    add_material(tip, honey_mat)
    smooth(tip)


def build_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.name = "SakPoKaab_Producto_Miel"
    scene.unit_settings.system = "METRIC"
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = SAMPLES
    scene.cycles.use_denoising = True
    try:
        scene.cycles.denoiser = "OPENIMAGEDENOISE"
    except Exception:
        pass
    scene.cycles.max_bounces = 8
    scene.cycles.glossy_bounces = 4
    scene.cycles.transmission_bounces = 10
    scene.cycles.transparent_max_bounces = 10
    scene.render.resolution_x = WIDTH
    scene.render.resolution_y = HEIGHT
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.film_transparent = False
    scene.view_settings.view_transform = "AgX"
    try:
        scene.view_settings.look = "AgX - Medium High Contrast"
    except Exception:
        scene.view_settings.look = "None"
    scene.view_settings.exposure = -0.65

    world = bpy.data.worlds.new("Estudio")
    scene.world = world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    nodes.clear()
    bg = nodes.new("ShaderNodeBackground")
    bg.inputs["Color"].default_value = (0.82, 0.74, 0.60, 1.0)
    bg.inputs["Strength"].default_value = 0.18
    out = nodes.new("ShaderNodeOutputWorld")
    world.node_tree.links.new(bg.outputs["Background"], out.inputs["Surface"])

    cream = material("Crema_Estudio", (0.66, 0.56, 0.42), roughness=0.80)
    paper = material("Papel_Etiqueta", (0.61, 0.49, 0.29), roughness=0.62)
    ink = material("Tinta_Verde", (0.006, 0.022, 0.012), roughness=0.45)
    brass = material("Latón_Tapa", (0.38, 0.17, 0.035), roughness=0.30, metallic=1.0)
    glass = material("Vidrio_Frasco", (0.86, 0.93, 0.89), roughness=0.020, transmission=1.0, ior=1.45, coat=0.15)
    honey = material("Miel_Ambar", (0.27, 0.058, 0.0016), roughness=0.075, transmission=0.0, ior=1.49, coat=0.35)
    wood = material("Madera_Cuchara", (0.18, 0.065, 0.022), roughness=0.48)

    make_cyclorama(cream)

    make_jar_shell(glass)

    base = cylinder("Fondo_Vidrio", 0.0525, 0.004, (0, 0, 0.002), glass, fill="NGON")
    bevel(base, 0.0010, 2)

    liquid = cylinder("Miel", 0.0505, 0.128, (0, 0, 0.069), honey, fill="NGON")
    bevel(liquid, 0.0020, 2)

    label = make_label(paper)

    mark = cylinder("Marca_Panal", 0.0050, 0.0008, (0, -0.0580, 0.1085), brass, vertices=6, fill="NGON")
    mark.rotation_euler = (math.pi / 2, 0, 0)
    bevel(mark, 0.0003, 2)

    text("Etiqueta_Marca", "SAK P'O' KAAB", 0.0064, (0, -0.0585, 0.0995), ink)
    text("Etiqueta_Producto", "MIEL DE MELIPONA", 0.0038, (0, -0.0585, 0.0890), ink)
    text("Etiqueta_Especie", "MELIPONA BEECHEII", 0.0028, (0, -0.0585, 0.0825), ink)
    text("Etiqueta_Peso", "250 g", 0.0036, (0, -0.0585, 0.0715), ink)

    bpy.ops.mesh.primitive_cube_add(location=(0, -0.0586, 0.0938))
    line = bpy.context.object
    line.name = "Etiqueta_Linea"
    line.scale = (0.036, 0.0003, 0.00045)
    add_material(line, brass)

    lid = cylinder("Tapa_Latón", 0.0475, 0.020, (0, 0, 0.1695), brass, fill="NGON")
    bevel(lid, 0.0025, 4)

    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.0450,
        minor_radius=0.0013,
        major_segments=96,
        minor_segments=10,
        location=(0, 0, 0.1595),
    )
    rim = bpy.context.object
    rim.name = "Aro_Tapa"
    add_material(rim, brass)
    smooth(rim)

    bpy.ops.mesh.primitive_plane_add(size=0.9, location=(0, -0.20, 0.0002))
    floor = bpy.context.object
    floor.name = "Piso_Sombra"
    add_material(floor, cream)

    def area(name, location, energy, size, color, target=(0, 0, 0.09), shape="RECTANGLE"):
        bpy.ops.object.light_add(type="AREA", location=location)
        light = bpy.context.object
        light.name = name
        light.data.energy = energy
        light.data.shape = shape
        light.data.size = size
        light.data.size_y = size * 0.72
        light.data.color = color
        look_at(light, target)
        return light

    area("Luz_Clave", (-0.38, -0.34, 0.62), 34, 0.62, (1.0, 0.90, 0.78))
    area("Luz_Relleno", (0.42, -0.18, 0.34), 14, 0.52, (0.72, 0.84, 1.0))
    area("Luz_Rim", (0.18, 0.34, 0.48), 24, 0.42, (1.0, 0.72, 0.43))
    area("Luz_Fondo", (0.00, 0.34, 0.22), 10, 0.80, (0.85, 0.78, 0.64), target=(0, 0.2, 0.2))

    bpy.ops.object.camera_add(location=(0.17, -0.56, 0.175))
    camera = bpy.context.object
    camera.name = "Camara_Producto"
    camera.data.lens = 85
    camera.data.sensor_width = 36
    camera.data.dof.use_dof = True
    camera.data.dof.focus_distance = 0.56
    camera.data.dof.aperture_fstop = 6.3
    look_at(camera, (0, 0, 0.095))
    scene.camera = camera

    bpy.ops.object.empty_add(location=(0, -0.02, 0.092))
    focus = bpy.context.object
    focus.name = "Foco_Producto"
    camera.data.dof.focus_object = focus

    scene.render.filepath = str(RENDER)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
    return scene


def main():
    start = time.time()
    scene = build_scene()
    bpy.ops.render.render(write_still=True)
    print("PRODUCT_RENDER_OK", str(RENDER), f"{time.time() - start:.1f}s", bpy.app.version_string)


if __name__ == "__main__":
    main()
