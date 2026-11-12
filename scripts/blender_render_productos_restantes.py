"""Renders de jabon, balsamo labial y vela con el mismo estudio que la miel.

Uso:
    "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" ^
      --background --python scripts/blender_render_productos_restantes.py

Variables opcionales:
    PRODUCTS=jabon,balsamo,vela
    PRODUCT_WIDTH=1600
    PRODUCT_HEIGHT=2000
    PRODUCT_SAMPLES=32
    PRODUCT_SUFFIX=-final

Salidas:
    docs/evidencias/2026-11-10/producto-<slug><sufijo>.png
    assets/models/producto-<slug>.blend
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

WIDTH = int(os.environ.get("PRODUCT_WIDTH", "760"))
HEIGHT = int(os.environ.get("PRODUCT_HEIGHT", "950"))
SAMPLES = int(os.environ.get("PRODUCT_SAMPLES", "16"))
SUFFIX = os.environ.get("PRODUCT_SUFFIX", "-prueba")
ONLY = {item.strip() for item in os.environ.get("PRODUCTS", "jabon,balsamo,vela").split(",")}


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


def add_bump(mat, scale=100, strength=0.08, distance=0.0006, detail=2.0):
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    noise = nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = scale
    noise.inputs["Detail"].default_value = detail
    bump = nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = strength
    bump.inputs["Distance"].default_value = distance
    links.new(noise.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])


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


def cylinder(name, radius, depth, location, mat, vertices=96, fill="NGON", rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        end_fill_type=fill,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    add_material(obj, mat)
    smooth(obj)
    return obj


def box(name, dimensions, location, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    add_material(obj, mat)
    return obj


def text(name, body, size, location, mat, rotation=(math.pi / 2, 0, 0), extrude=0.00012):
    curve = bpy.data.curves.new(name, type="FONT")
    curve.body = body
    curve.size = size
    curve.align_x = "CENTER"
    curve.align_y = "CENTER"
    curve.extrude = extrude
    curve.bevel_depth = 0.00003
    curve.bevel_resolution = 1
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = rotation
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
    verts = [(x, y, z) for x in xs for y, z in profile]
    n = len(profile)
    faces = [(i, i + 1, n + i + 1, n + i) for i in range(n - 1)]
    mesh = bpy.data.meshes.new("Ciclorama_Malla")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("Ciclorama", mesh)
    bpy.context.collection.objects.link(obj)
    add_material(obj, mat)
    return obj


def make_revolved(name, profile, mat, segments=96, thickness=0.003):
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
    mesh = bpy.data.meshes.new(name + "_Malla")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    add_material(obj, mat)
    smooth(obj)
    if thickness:
        solid = obj.modifiers.new("Grosor", "SOLIDIFY")
        solid.thickness = thickness
        solid.offset = -1.0
        bevel(obj, 0.0012, 3)
    return obj


def curved_label(name, radius, z0, z1, mat, start_deg=-62, end_deg=62, steps=24):
    start, end = math.radians(start_deg), math.radians(end_deg)
    verts = []
    for i in range(steps + 1):
        a = start + (end - start) * i / steps
        x = radius * math.sin(a)
        y = -radius * math.cos(a)
        verts.append((x, y, z0))
        verts.append((x, y, z1))
    faces = [(i * 2, i * 2 + 1, i * 2 + 3, i * 2 + 2) for i in range(steps)]
    mesh = bpy.data.meshes.new(name + "_Malla")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    add_material(obj, mat)
    solid = obj.modifiers.new("Grosor_Etiqueta", "SOLIDIFY")
    solid.thickness = 0.0007
    solid.offset = 1.0
    return obj


def studio(name):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.name = name
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

    mats = {
        "cream": material("Crema_Estudio", (0.66, 0.56, 0.42), roughness=0.80),
        "paper": material("Papel_Etiqueta", (0.48, 0.36, 0.18), roughness=0.66),
        "ink": material("Tinta_Verde", (0.006, 0.022, 0.012), roughness=0.45),
        "brass": material("Latón_Tapa", (0.38, 0.17, 0.035), roughness=0.30, metallic=1.0),
        "glass": material("Vidrio_Frasco", (0.86, 0.93, 0.89), roughness=0.020, transmission=1.0, ior=1.45, coat=0.15),
        "honey": material("Miel_Ambar", (0.27, 0.058, 0.0016), roughness=0.075, ior=1.49, coat=0.35),
        "soap_honey": material("Jabon_Miel", (0.32, 0.18, 0.060), roughness=0.58),
        "soap_cacao": material("Jabon_Cacao", (0.10, 0.038, 0.014), roughness=0.62),
        "kraft": material("Kraft_Tubo", (0.24, 0.13, 0.050), roughness=0.80),
        "green": material("Verde_Tapa", (0.020, 0.075, 0.045), roughness=0.35),
        "wax": material("Cera_Melipona", (0.50, 0.32, 0.105), roughness=0.38),
        "wick": material("Mecha_Algodon", (0.010, 0.009, 0.007), roughness=0.90),
    }

    add_bump(mats["soap_honey"], scale=120, strength=0.16, distance=0.0005)
    add_bump(mats["soap_cacao"], scale=120, strength=0.16, distance=0.0005)
    add_bump(mats["kraft"], scale=180, strength=0.10, distance=0.0004)
    add_bump(mats["wax"], scale=70, strength=0.06, distance=0.0004)
    add_bump(mats["paper"], scale=220, strength=0.035, distance=0.0002)

    make_cyclorama(mats["cream"])

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

    bpy.ops.mesh.primitive_plane_add(size=0.9, location=(0, -0.20, 0.0002))
    floor = bpy.context.object
    floor.name = "Piso_Sombra"
    add_material(floor, mats["cream"])
    return scene, mats


def setup_camera(location, target, lens=85, fstop=6.3):
    bpy.ops.object.camera_add(location=location)
    camera = bpy.context.object
    camera.name = "Camara_Producto"
    camera.data.lens = lens
    camera.data.sensor_width = 36
    camera.data.dof.use_dof = True
    camera.data.dof.focus_distance = (Vector(target) - Vector(location)).length
    camera.data.dof.aperture_fstop = fstop
    look_at(camera, target)
    bpy.context.scene.camera = camera
    bpy.ops.object.empty_add(location=target)
    focus = bpy.context.object
    focus.name = "Foco_Producto"
    camera.data.dof.focus_object = focus


def build_soap(mats):
    body = box("Jabon_Cuerpo", (0.095, 0.058, 0.032), (0, 0, 0.016), mats["soap_honey"])
    bevel(body, 0.010, 6)
    smooth(body)

    band_z = 0.016
    box("Banda_Frontal", (0.096, 0.0008, 0.012), (0, -0.0291, band_z), mats["paper"])
    box("Banda_Trasera", (0.096, 0.0008, 0.012), (0, 0.0291, band_z), mats["paper"])
    box("Banda_Izquierda", (0.0008, 0.058, 0.012), (-0.0478, 0, band_z), mats["paper"])
    box("Banda_Derecha", (0.0008, 0.058, 0.012), (0.0478, 0, band_z), mats["paper"])

    text("Jabon_Marca", "SAK P'O' KAAB", 0.0040, (0, -0.0302, 0.0192), mats["ink"])
    text("Jabon_Producto", "JABÓN DE MIEL", 0.0024, (0, -0.0302, 0.0132), mats["ink"])

    mark = cylinder("Jabon_Panal", 0.0032, 0.0008, (0, -0.0302, 0.0232), mats["brass"], vertices=6, fill="NGON")
    mark.rotation_euler = (math.pi / 2, 0, 0)

    setup_camera((0.11, -0.32, 0.12), (0, 0, 0.024), lens=90, fstop=6.3)


def build_balm(mats):
    tube = cylinder("Balsamo_Tubo", 0.0085, 0.060, (-0.014, 0, 0.030), mats["kraft"], vertices=64)
    bevel(tube, 0.0012, 3)
    cap = cylinder("Balsamo_Tapa", 0.0092, 0.016, (-0.014, 0, 0.068), mats["green"], vertices=64)
    bevel(cap, 0.0015, 3)

    label = curved_label("Balsamo_Etiqueta", 0.0088, 0.021, 0.049, mats["paper"], -78, 78, 18)
    label.location.x = -0.014
    text("Balsamo_Marca", "XUNÁN", 0.0020, (-0.014, -0.0090, 0.0385), mats["ink"])
    text("Balsamo_Producto", "BÁLSAMO LABIAL", 0.0011, (-0.014, -0.0090, 0.0325), mats["ink"])
    text("Balsamo_Peso", "10 g", 0.0013, (-0.014, -0.0090, 0.0270), mats["ink"])

    lying = cylinder(
        "Balsamo_Tubo_Acostado",
        0.0085,
        0.060,
        (0.008, -0.022, 0.009),
        mats["kraft"],
        vertices=64,
        rotation=(0, math.pi / 2, 0),
    )
    bevel(lying, 0.0012, 3)
    cylinder(
        "Balsamo_Tapa_Acostada",
        0.0092,
        0.016,
        (0.045, -0.022, 0.009),
        mats["green"],
        vertices=64,
        rotation=(0, math.pi / 2, 0),
    )

    setup_camera((0.095, -0.305, 0.135), (0.010, -0.004, 0.036), lens=102, fstop=7.1)


def build_candle(mats):
    profile = [
        (0.0600, 0.0000),
        (0.0600, 0.0780),
        (0.0592, 0.0850),
        (0.0560, 0.0910),
        (0.0518, 0.0960),
        (0.0480, 0.1000),
        (0.0460, 0.1030),
        (0.0460, 0.1050),
        (0.0472, 0.1065),
    ]
    make_revolved("Vela_Frasco", profile, mats["glass"], thickness=0.003)
    cylinder("Vela_Fondo", 0.0575, 0.004, (0, 0, 0.002), mats["glass"], fill="NGON")

    wax = cylinder("Vela_Cera", 0.0555, 0.078, (0, 0, 0.0405), mats["wax"], fill="NGON")
    bevel(wax, 0.0020, 2)
    cylinder("Vela_Mecha", 0.0009, 0.011, (0, 0, 0.0840), mats["wick"], vertices=16)

    curved_label("Vela_Etiqueta", 0.0618, 0.020, 0.056, mats["paper"], -58, 58, 24)
    text("Vela_Marca", "VELA JOBÓN", 0.0042, (0, -0.0630, 0.0445), mats["ink"])
    text("Vela_Producto", "CERA DE MELIPONA", 0.0023, (0, -0.0630, 0.0365), mats["ink"])
    text("Vela_Peso", "200 g", 0.0022, (0, -0.0630, 0.0290), mats["ink"])

    setup_camera((0.135, -0.425, 0.160), (0, 0, 0.055), lens=90, fstop=6.3)


JOBS = {
    "jabon": (build_soap, "producto-jabon"),
    "balsamo": (build_balm, "producto-balsamo"),
    "vela": (build_candle, "producto-vela"),
}


def main():
    for slug in ("jabon", "balsamo", "vela"):
        if slug not in ONLY:
            continue
        builder, prefix = JOBS[slug]
        start = time.time()
        scene, mats = studio("SakPoKaab_" + slug.title())
        builder(mats)
        output = OUT / f"{prefix}{SUFFIX}.png"
        blend = MODELS / f"{prefix}.blend"
        scene.render.filepath = str(output)
        bpy.ops.wm.save_as_mainfile(filepath=str(blend))
        bpy.ops.render.render(write_still=True)
        print("PRODUCT_RENDER_OK", slug, str(output), f"{time.time() - start:.1f}s")


if __name__ == "__main__":
    main()
