"""Render an original, didactic 2D melipona-harvest animation with FFmpeg."""

from __future__ import annotations

import math
import shutil
import subprocess
import tempfile
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from audio_bed import write_original_music
from subtitle_utils import build_srt


ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "assets" / "audio" / "narracion-cosecha.wav"
OUTPUT = ROOT / "assets" / "video" / "cosecha-melipona-recreacion.mp4"
OUTPUT_MOBILE = ROOT / "assets" / "video" / "cosecha-melipona-recreacion-mobile.mp4"
OUTPUT_SOCIAL = ROOT / "assets" / "video" / "cosecha-melipona-recreacion-social-vertical.mp4"
SUBTITLES = ROOT / "assets" / "video" / "cosecha-melipona-recreacion.srt"
AUDIO_BED = ROOT / "assets" / "audio" / "cama-sonora-original.wav"
POSTER = ROOT / "assets" / "video" / "cosecha-poster.png"
WIDTH, HEIGHT, FPS = 1280, 720, 24

BG_TOP = (13, 38, 28)
BG_BOTTOM = (33, 68, 45)
PANEL = (21, 53, 38)
PANEL_EDGE = (67, 103, 68)
CREAM = (247, 239, 216)
MUTED = (206, 208, 183)
AMBER = (226, 166, 58)
HONEY = (244, 194, 78)
HONEY_LIGHT = (255, 224, 139)
INK = (31, 36, 28)
WOOD = (120, 79, 48)
WOOD_LIGHT = (166, 117, 72)
LEAF = (81, 125, 65)
LEAF_LIGHT = (117, 151, 79)
RED = (198, 95, 67)

FONT_DIR = Path(r"C:\Windows\Fonts")
FONT_REGULAR = FONT_DIR / "segoeui.ttf"
FONT_BOLD = FONT_DIR / "segoeuib.ttf"
FONT_SERIF = FONT_DIR / "georgia.ttf"
FONT_SERIF_BOLD = FONT_DIR / "georgiab.ttf"

SCENES = [
    {
        "kicker": "01 · COLONIA",
        "title": "La colonia y\nel jobón",
        "body": "En Yucatán, algunas familias cuidan a la Xunáan Kaab en jobones: troncos huecos que protegen la colonia y sus reservas.",
        "caption": "El jobón resguarda abejas, cría y alimento.",
        "weight": 19,
        "art": "colony",
    },
    {
        "kicker": "02 · PREPARACIÓN",
        "title": "Preparar el\nespacio",
        "body": "Antes de cosechar, preparan un espacio limpio y revisan el nido con paciencia.",
        "caption": "Área, recipientes y herramientas limpios.",
        "weight": 13,
        "art": "prepare",
    },
    {
        "kicker": "03 · REVISIÓN",
        "title": "Abrir con\ncuidado",
        "body": "Abren el jobón con cuidado para localizar los potes de miel, polen y cría.",
        "caption": "Identificar los potes antes de recolectar.",
        "weight": 13,
        "art": "inspect",
    },
    {
        "kicker": "04 · RECOLECCIÓN",
        "title": "Escurrir por\ngravedad",
        "body": "En este ejemplo, perforan algunos potes maduros e inclinan el jobón. La miel escurre por gravedad; no se centrifuga.",
        "caption": "Se recolecta una parte; se conservan reservas.",
        "weight": 18,
        "art": "drain",
    },
    {
        "kicker": "05 · FILTRADO",
        "title": "Filtrar y\nenvasar",
        "body": "La miel se filtra con malla limpia y se envasa. Después, limpian y vuelven a sellar el jobón.",
        "caption": "Malla limpia · recipiente limpio · cierre cuidadoso.",
        "weight": 17,
        "art": "filter",
    },
    {
        "kicker": "06 · CUIDADO",
        "title": "Dejar reservas\na la colonia",
        "body": "Se dejan potes intactos como reserva. Las prácticas varían entre comunidades.",
        "caption": "Recreación didáctica · no es metraje documental.",
        "weight": 18,
        "art": "care",
    },
]


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


F_EYEBROW = font(FONT_BOLD, 17)
F_HEADER = font(FONT_BOLD, 23)
F_TITLE = font(FONT_SERIF_BOLD, 50)
F_BODY = font(FONT_REGULAR, 23)
F_CAPTION = font(FONT_BOLD, 21)
F_SMALL = font(FONT_REGULAR, 15)
F_TINY = font(FONT_REGULAR, 12)
F_LABEL = font(FONT_BOLD, 16)
F_NUMBER = font(FONT_SERIF_BOLD, 25)


def mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    t = max(0.0, min(1.0, t))
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def make_background() -> Image.Image:
    image = Image.new("RGBA", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    for y in range(HEIGHT):
        color = mix(BG_TOP, BG_BOTTOM, y / (HEIGHT - 1))
        draw.line((0, y, WIDTH, y), fill=(*color, 255))

    # Low-contrast honeycomb texture keeps the visual language consistent with
    # the printed label without distracting from the instructions.
    for row in range(-1, 7):
        cy = 70 + row * 122
        offset = 0 if row % 2 == 0 else 74
        for col in range(-1, 12):
            cx = 45 + col * 148 + offset
            points = hex_points(cx, cy, 36)
            draw.line(points + [points[0]], fill=(34, 63, 43, 255), width=1)

    draw.ellipse((1035, -90, 1305, 180), fill=(27, 57, 39, 255))
    draw.ellipse((-190, 590, 110, 890), fill=(28, 60, 39, 255))
    return image


def hex_points(cx: float, cy: float, radius: float) -> list[tuple[int, int]]:
    return [
        (round(cx + math.cos(math.radians(angle)) * radius), round(cy + math.sin(math.radians(angle)) * radius))
        for angle in (0, 60, 120, 180, 240, 300)
    ]


BACKGROUND = make_background()


def wrap_lines(draw: ImageDraw.ImageDraw, text: str, used_font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=used_font)[2] <= max_width or not line:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_paragraph(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    used_font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    max_width: int,
    line_gap: int = 10,
) -> int:
    x, y = xy
    line_height = used_font.size + line_gap
    for line in wrap_lines(draw, text, used_font, max_width):
        draw.text((x, y), line, font=used_font, fill=fill)
        y += line_height
    return y


def draw_bee(draw: ImageDraw.ImageDraw, cx: float, cy: float, scale: float = 1.0, phase: float = 0.0) -> None:
    flap = 0.82 + 0.18 * math.sin(phase * 18)
    wing_w = 39 * scale * flap
    wing_h = 17 * scale * (1.15 - flap * 0.25)
    body_w = 23 * scale
    body_h = 34 * scale

    draw.ellipse((cx - body_w * 1.8 - wing_w, cy - wing_h * 1.4, cx - body_w * 0.15, cy + wing_h * 0.6),
                 fill=(247, 239, 216, 235), outline=INK, width=max(1, round(2 * scale)))
    draw.ellipse((cx + body_w * 0.15, cy - wing_h * 1.4, cx + body_w * 1.8 + wing_w, cy + wing_h * 0.6),
                 fill=(247, 239, 216, 235), outline=INK, width=max(1, round(2 * scale)))
    draw.ellipse((cx - body_w / 2, cy - body_h / 2, cx + body_w / 2, cy + body_h / 2),
                 fill=AMBER, outline=INK, width=max(1, round(2 * scale)))
    for offset in (-0.25, 0.25):
        y = cy + body_h * offset
        draw.arc((cx - body_w / 2, y - 5 * scale, cx + body_w / 2, y + 9 * scale), 0, 180,
                 fill=INK, width=max(2, round(4 * scale)))
    head_r = 9 * scale
    draw.ellipse((cx - head_r, cy - body_h / 2 - head_r * 1.45, cx + head_r, cy - body_h / 2 + head_r * 0.45),
                 fill=INK)
    draw.line((cx - 4 * scale, cy - body_h / 2 - 11 * scale, cx - 10 * scale, cy - body_h / 2 - 18 * scale),
              fill=INK, width=max(1, round(2 * scale)))
    draw.line((cx + 4 * scale, cy - body_h / 2 - 11 * scale, cx + 10 * scale, cy - body_h / 2 - 18 * scale),
              fill=INK, width=max(1, round(2 * scale)))


def draw_jobon_layer(opened: bool = True, sealed: bool = False) -> Image.Image:
    layer = Image.new("RGBA", (540, 300), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # Shadow and hollow log.
    d.ellipse((66, 221, 477, 274), fill=(6, 20, 12, 65))
    d.rounded_rectangle((82, 92, 458, 222), radius=56, fill=WOOD, outline=INK, width=7)
    d.rounded_rectangle((113, 103, 429, 211), radius=47, fill=WOOD_LIGHT, outline=(83, 53, 35), width=4)
    for y in (125, 154, 184, 202):
        d.arc((128, y - 24, 421, y + 28), 190, 348, fill=(102, 66, 42), width=3)
    # Left wooden end.
    d.ellipse((60, 91, 151, 222), fill=(94, 61, 42), outline=INK, width=6)
    d.ellipse((76, 107, 135, 207), outline=(173, 124, 78), width=4)
    # Right opening, with stylized honey pots or its clay stopper.
    d.ellipse((393, 77, 505, 235), fill=(82, 55, 37), outline=INK, width=7)
    if sealed:
        d.ellipse((410, 93, 489, 218), fill=(144, 104, 68), outline=(73, 49, 34), width=5)
        d.arc((399, 82, 499, 229), 205, 335, fill=(162, 105, 66), width=13)
        d.arc((399, 82, 499, 229), 25, 155, fill=(162, 105, 66), width=13)
    elif opened:
        d.ellipse((410, 94, 489, 217), fill=(36, 42, 30), outline=CREAM, width=3)
        for x, y, color in [
            (429, 122, HONEY), (463, 123, HONEY_LIGHT), (444, 153, AMBER),
            (425, 184, HONEY_LIGHT), (463, 185, HONEY),
        ]:
            r = 12
            d.polygon(hex_points(x, y, r), fill=color, outline=(72, 52, 32))
            d.ellipse((x - 3, y - 6, x + 1, y - 2), fill=(255, 241, 199))
        if sealed:
            pass
    else:
        d.ellipse((411, 94, 488, 218), fill=(123, 83, 52), outline=(55, 39, 28), width=4)
        d.arc((420, 106, 480, 206), 0, 360, fill=(177, 128, 82), width=3)
    return layer


def paste_rotated_center(image: Image.Image, layer: Image.Image, center: tuple[int, int], scale: float, angle: float = 0) -> None:
    rotated = layer.rotate(angle, resample=Image.Resampling.BICUBIC, expand=False)
    size = (max(1, round(rotated.width * scale)), max(1, round(rotated.height * scale)))
    resized = rotated.resize(size, Image.Resampling.LANCZOS)
    image.alpha_composite(resized, (round(center[0] - size[0] / 2), round(center[1] - size[1] / 2)))


def draw_jar(draw: ImageDraw.ImageDraw, cx: int, bottom: int, scale: float = 1.0, fill: float = 0.65) -> None:
    width, height = round(112 * scale), round(158 * scale)
    left, right = cx - width // 2, cx + width // 2
    top = bottom - height
    neck_h = round(20 * scale)
    cap_h = round(23 * scale)
    fill_y = bottom - round((height - 18 * scale) * fill)
    draw.rounded_rectangle((left, top + neck_h + cap_h, right, bottom), radius=round(17 * scale),
                           fill=(245, 239, 218), outline=CREAM, width=max(2, round(3 * scale)))
    draw.rectangle((left + 5 * scale, fill_y, right - 5 * scale, bottom - 4 * scale), fill=HONEY)
    draw.rounded_rectangle((left, top + neck_h + cap_h, right, bottom), radius=round(17 * scale),
                           outline=CREAM, width=max(2, round(3 * scale)))
    draw.rectangle((cx - round(27 * scale), top + cap_h, cx + round(27 * scale), top + cap_h + neck_h),
                   fill=(245, 239, 218), outline=CREAM, width=max(2, round(3 * scale)))
    draw.rounded_rectangle((cx - round(34 * scale), top, cx + round(34 * scale), top + cap_h),
                           radius=round(5 * scale), fill=AMBER, outline=INK, width=max(1, round(2 * scale)))
    draw.line((left + 18 * scale, top + 64 * scale, left + 18 * scale, bottom - 22 * scale),
              fill=(255, 255, 255), width=max(2, round(4 * scale)))


def draw_filter(draw: ImageDraw.ImageDraw, cx: int, top: int, scale: float = 1.0) -> None:
    width = round(156 * scale)
    height = round(112 * scale)
    left, right = cx - width // 2, cx + width // 2
    bottom = top + height
    draw.line((left, top, right, top), fill=CREAM, width=max(4, round(7 * scale)))
    draw.line((left, top, cx - round(26 * scale), bottom), fill=CREAM, width=max(3, round(5 * scale)))
    draw.line((right, top, cx + round(26 * scale), bottom), fill=CREAM, width=max(3, round(5 * scale)))
    for y in range(top + round(15 * scale), bottom, max(6, round(12 * scale))):
        d = (y - top) / max(1, height)
        x1 = round(left + (cx - 26 * scale - left) * d)
        x2 = round(right + (cx + 26 * scale - right) * d)
        draw.line((x1, y, x2, y), fill=(193, 207, 169), width=max(1, round(1 * scale)))
    draw.line((cx - 26 * scale, bottom, cx + 26 * scale, bottom), fill=CREAM, width=max(3, round(5 * scale)))


def draw_sparkle(draw: ImageDraw.ImageDraw, cx: int, cy: int, size: int, color=HONEY_LIGHT) -> None:
    draw.line((cx - size, cy, cx + size, cy), fill=color, width=3)
    draw.line((cx, cy - size, cx, cy + size), fill=color, width=3)
    draw.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=color)


def draw_arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color=AMBER, width: int = 6) -> None:
    draw.line((start, end), fill=color, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    length = 17
    for sign in (-1, 1):
        a = angle + math.pi + sign * math.radians(28)
        tip = (round(end[0] + math.cos(a) * length), round(end[1] + math.sin(a) * length))
        draw.line((end, tip), fill=color, width=width)


def draw_flowers(draw: ImageDraw.ImageDraw, positions: list[tuple[int, int]], time_s: float) -> None:
    colors = [(239, 199, 215), (245, 227, 160), (220, 204, 239), (247, 240, 216)]
    for i, (x, y) in enumerate(positions):
        sway = math.sin(time_s * 1.7 + i) * 3
        x += round(sway)
        color = colors[i % len(colors)]
        draw.line((x, y + 38, x, y), fill=LEAF, width=5)
        draw.ellipse((x - 21, y + 15, x + 2, y + 27), fill=LEAF_LIGHT)
        draw.ellipse((x - 4, y + 17, x + 18, y + 29), fill=LEAF)
        for angle in range(0, 360, 60):
            px = x + math.cos(math.radians(angle)) * 14
            py = y + math.sin(math.radians(angle)) * 10
            draw.ellipse((px - 8, py - 5, px + 8, py + 5), fill=color)
        draw.ellipse((x - 5, y - 4, x + 5, y + 5), fill=AMBER)


def draw_meliponary(image: Image.Image, time_s: float, simplified: bool = False) -> None:
    d = ImageDraw.Draw(image, "RGBA")
    # Pale ground disc and small shelter.
    d.ellipse((687, 435, 1178, 528), fill=(15, 33, 24, 95), outline=(132, 153, 99, 100), width=2)
    d.polygon([(780, 244), (914, 170), (1048, 244)], fill=(120, 79, 48), outline=CREAM)
    d.line((780, 243, 1048, 243), fill=CREAM, width=5)
    for x in (804, 1025):
        d.rectangle((x, 242, x + 13, 426), fill=WOOD_LIGHT)
    d.line((804, 294, 1037, 294), fill=(178, 132, 84), width=4)
    paste_rotated_center(image, draw_jobon_layer(opened=False, sealed=True), (920, 361), 0.72)
    draw_flowers(d, [(746, 406), (1090, 405), (850, 427)], time_s)
    draw_bee(d, 790 + round(90 * math.sin(time_s * 1.2)), 269 + round(22 * math.sin(time_s * 2)), 1.05, time_s)
    draw_bee(d, 1030 + round(45 * math.sin(time_s * 1.4 + 1)), 324 + round(17 * math.cos(time_s * 1.8)), 0.75, time_s + 1)


def draw_preparation(image: Image.Image, time_s: float) -> None:
    d = ImageDraw.Draw(image, "RGBA")
    # Work surface.
    d.rounded_rectangle((690, 416, 1165, 477), radius=18, fill=(89, 66, 43), outline=CREAM, width=3)
    d.rectangle((722, 474, 739, 515), fill=WOOD_LIGHT)
    d.rectangle((1098, 474, 1115, 515), fill=WOOD_LIGHT)
    # Folded cloth and clean utensils.
    d.rounded_rectangle((732, 365, 884, 418), radius=12, fill=(242, 239, 215), outline=CREAM, width=3)
    d.line((750, 390, 862, 390), fill=(193, 207, 169), width=3)
    draw_filter(d, 1008, 284, 0.72)
    draw_jar(d, 1008, 454, 0.7, 0.1)
    d.line((798, 302, 844, 363), fill=(204, 212, 184), width=8)
    d.ellipse((785, 288, 808, 311), fill=(204, 212, 184))
    for x, y in ((756, 328), (883, 300), (1097, 341), (950, 245)):
        draw_sparkle(d, x, y, 10)
    draw_bee(d, 1133, 248 + round(9 * math.sin(time_s * 2)), 0.62, time_s)


def draw_inspection(image: Image.Image, time_s: float) -> None:
    d = ImageDraw.Draw(image, "RGBA")
    d.ellipse((690, 169, 1168, 521), fill=(10, 30, 20, 80), outline=(88, 120, 79), width=3)
    paste_rotated_center(image, draw_jobon_layer(opened=True), (930, 348), 0.84, angle=0)
    # Leaders distinguish honey from pollen/brood without implying that all nests
    # arrange the pots identically.
    d.line((1085, 291, 1147, 250), fill=HONEY_LIGHT, width=3)
    d.rounded_rectangle((1070, 212, 1177, 250), radius=15, fill=(13, 38, 28), outline=AMBER, width=2)
    d.text((1082, 221), "MIEL", font=F_LABEL, fill=HONEY_LIGHT)
    d.line((1082, 408, 1145, 442), fill=(206, 208, 183), width=3)
    d.rounded_rectangle((1050, 441, 1184, 480), radius=15, fill=(13, 38, 28), outline=(143, 162, 125), width=2)
    d.text((1060, 450), "POLEN / CRÍA", font=F_TINY, fill=CREAM)
    draw_sparkle(d, 752, 223, 9)
    draw_bee(d, 1090, 181 + round(8 * math.sin(time_s * 1.6)), 0.56, time_s + 2)


def draw_drain(image: Image.Image, time_s: float, progress: float) -> None:
    d = ImageDraw.Draw(image, "RGBA")
    d.ellipse((690, 447, 1170, 523), fill=(11, 29, 20, 100), outline=(85, 113, 70), width=2)
    paste_rotated_center(image, draw_jobon_layer(opened=True), (852, 303), 0.74, angle=-13)
    # Receiving bowl with mesh above it.
    d.ellipse((947, 397, 1125, 452), fill=(71, 56, 39), outline=CREAM, width=4)
    d.arc((949, 374, 1124, 449), 0, 180, fill=CREAM, width=4)
    # Flow advances down toward the bowl.
    flow = max(0.0, min(1.0, (progress - 0.14) / 0.66))
    stream_top = (906, 306)
    stream_bottom = (1033, round(370 + 68 * flow))
    if flow > 0:
        d.line((stream_top, stream_bottom), fill=HONEY, width=8)
        for i in range(4):
            t = (i + 1) / 5
            y = stream_top[1] + (stream_bottom[1] - stream_top[1]) * t
            x = stream_top[0] + (stream_bottom[0] - stream_top[0]) * t
            offset = (time_s * 68 + i * 37) % 66
            d.ellipse((x - 6, y + offset - 7, x + 6, y + offset + 7), fill=HONEY_LIGHT)
    draw_arrow(d, (978, 273), (1041, 360), HONEY_LIGHT, 4)
    d.rounded_rectangle((1022, 268, 1162, 306), radius=16, fill=(13, 38, 28), outline=AMBER, width=2)
    d.text((1034, 276), "GRAVEDAD", font=F_LABEL, fill=HONEY_LIGHT)


def draw_filtering(image: Image.Image, time_s: float, progress: float) -> None:
    d = ImageDraw.Draw(image, "RGBA")
    d.ellipse((691, 453, 1170, 520), fill=(11, 29, 20, 100), outline=(85, 113, 70), width=2)
    # Container at left, mesh/funnel above the jar.
    draw_jar(d, 843, 458, 1.08, fill=0.38 + 0.4 * max(0.0, min(1.0, progress)))
    draw_filter(d, 843, 250, 1.08)
    d.ellipse((815, 351, 871, 369), fill=HONEY, outline=CREAM, width=2)
    stream_bottom = 383 + round(34 * max(0, min(1, progress)))
    d.line((843, 365, 843, stream_bottom), fill=HONEY, width=7)
    for i in range(3):
        y = 372 + ((time_s * 50 + i * 22) % max(30, stream_bottom - 365))
        d.ellipse((838, y - 5, 848, y + 6), fill=HONEY_LIGHT)
    draw_sparkle(d, 1051, 283, 12)
    draw_sparkle(d, 1110, 347, 9)
    d.rounded_rectangle((977, 394, 1157, 434), radius=18, fill=(13, 38, 28), outline=AMBER, width=2)
    d.text((994, 402), "MALLA LIMPIA", font=F_LABEL, fill=CREAM)


def draw_care(image: Image.Image, time_s: float, progress: float) -> None:
    d = ImageDraw.Draw(image, "RGBA")
    d.ellipse((690, 448, 1170, 520), fill=(11, 29, 20, 95), outline=(85, 113, 70), width=2)
    paste_rotated_center(image, draw_jobon_layer(opened=False, sealed=True), (887, 358), 0.82)
    # Show a few intact pots as food reserves.
    d.rounded_rectangle((1012, 220, 1162, 378), radius=22, fill=(13, 38, 28), outline=(99, 129, 82), width=3)
    for row in range(3):
        for col in range(2):
            cx, cy = 1054 + col * 64, 264 + row * 42
            pts = hex_points(cx, cy, 20)
            d.polygon(pts, fill=(179, 130, 67), outline=CREAM)
            d.arc((cx - 10, cy - 9, cx + 10, cy + 10), 190, 330, fill=(255, 224, 139), width=2)
    d.rounded_rectangle((1004, 389, 1171, 431), radius=17, fill=(13, 38, 28), outline=AMBER, width=2)
    d.text((1021, 398), "RESERVAS", font=F_LABEL, fill=HONEY_LIGHT)
    draw_flowers(d, [(720, 422), (1130, 423)], time_s)
    draw_bee(d, 756 + round(78 * math.sin(time_s * 1.4)), 254 + round(16 * math.sin(time_s * 2)), 0.85, time_s)
    draw_bee(d, 972 + round(50 * math.cos(time_s * 1.1)), 303 + round(15 * math.sin(time_s * 1.6)), 0.66, time_s + 1.5)
    if progress > 0.76:
        d.rounded_rectangle((710, 187, 1170, 230), radius=18, fill=(13, 38, 28), outline=(99, 129, 82), width=2)
        d.text((733, 196), "PRÁCTICAS DISTINTAS EN CADA COMUNIDAD", font=F_SMALL, fill=CREAM)


def draw_visual(image: Image.Image, art: str, time_s: float, progress: float) -> None:
    d = ImageDraw.Draw(image, "RGBA")
    d.rounded_rectangle((637, 139, 1206, 527), radius=30, fill=(12, 35, 24, 168), outline=PANEL_EDGE, width=2)
    if art == "colony":
        draw_meliponary(image, time_s)
    elif art == "prepare":
        draw_preparation(image, time_s)
    elif art == "inspect":
        draw_inspection(image, time_s)
    elif art == "drain":
        draw_drain(image, time_s, progress)
    elif art == "filter":
        draw_filtering(image, time_s, progress)
    else:
        draw_care(image, time_s, progress)


def draw_frame(scene_index: int, local_time: float, scene_duration: float, overall_progress: float) -> Image.Image:
    image = BACKGROUND.copy()
    d = ImageDraw.Draw(image, "RGBA")
    scene = SCENES[scene_index]
    progress = max(0.0, min(1.0, local_time / max(0.01, scene_duration)))

    # Persistent brand and progress header.
    d.text((74, 37), "SAK P'O' KAAB", font=F_HEADER, fill=AMBER)
    d.text((74, 69), "ANIMACIÓN ORIGINAL · COSECHA MELIPONA", font=F_SMALL, fill=MUTED)
    d.rounded_rectangle((842, 53, 1190, 64), radius=5, fill=(69, 91, 62))
    d.rounded_rectangle((842, 53, 842 + round(348 * overall_progress), 64), radius=5, fill=AMBER)
    d.text((1192, 43), f"{scene_index + 1:02d}/06", font=F_LABEL, fill=CREAM, anchor="ra")

    # Left text panel.
    d.text((78, 131), scene["kicker"], font=F_EYEBROW, fill=HONEY_LIGHT)
    title_lines = scene["title"].split("\n")
    y = 166
    for line in title_lines:
        d.text((76, y), line, font=F_TITLE, fill=CREAM)
        y += 57
    draw_paragraph(d, (80, y + 21), scene["body"], F_BODY, MUTED, 490, line_gap=11)

    # Short practice cue.
    pill_y = 445
    d.rounded_rectangle((78, pill_y, 560, pill_y + 45), radius=22, fill=(27, 68, 46, 210), outline=(87, 128, 77), width=2)
    d.ellipse((95, pill_y + 15, 110, pill_y + 30), fill=AMBER)
    d.text((123, pill_y + 9), scene["caption"], font=F_SMALL, fill=CREAM)

    draw_visual(image, scene["art"], local_time, progress)

    # Lower narration subtitle and persistent didactic notice.
    d.rounded_rectangle((74, 558, 1206, 650), radius=24, fill=(8, 27, 18, 223), outline=(85, 113, 70), width=2)
    subtitle = [
        "Jobones tradicionales: troncos huecos que resguardan a la colonia.",
        "Un espacio limpio ayuda a proteger el producto.",
        "Cada pote puede guardar miel, polen o cría.",
        "La gravedad permite recolectar miel en este ejemplo tradicional.",
        "Malla limpia y envase limpio para el producto.",
        "Se conservan reservas; las prácticas varían por comunidad.",
    ][scene_index]
    d.text((101, 576), subtitle, font=F_CAPTION, fill=CREAM)
    d.text((101, 615), "RECREACIÓN DIDÁCTICA · NO ES METRAJE DOCUMENTAL", font=F_TINY, fill=HONEY_LIGHT)

    # Source line appears on the final scene.
    if scene_index == len(SCENES) - 1 and progress > 0.35:
        d.text((1202, 687), "Fuentes: The Nature Conservancy México · SEMARNAT (2023)",
               font=F_TINY, fill=(202, 206, 177), anchor="ra")
    else:
        d.text((1202, 687), "Las prácticas varían entre comunidades meliponicultoras.",
               font=F_TINY, fill=(202, 206, 177), anchor="ra")

    return image.convert("RGB")


def audio_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as wav:
        return wav.getnframes() / wav.getframerate()


def main() -> None:
    if not AUDIO.is_file():
        raise SystemExit(
            "Falta la narración. Ejecuta primero: "
            "powershell -ExecutionPolicy Bypass -File scripts/generate_harvest_narration.ps1"
        )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    audio_seconds = audio_duration(AUDIO)
    hold_seconds = 2.5
    video_seconds = audio_seconds + hold_seconds
    weight_sum = sum(scene["weight"] for scene in SCENES)
    scene_durations = [audio_seconds * scene["weight"] / weight_sum for scene in SCENES]
    scene_durations[-1] += hold_seconds
    frame_count = math.ceil(video_seconds * FPS)
    subtitle_texts = [scene["body"] for scene in SCENES]
    subtitle_texts[-1] = (
        f"{subtitle_texts[-1]} Esta animación es una recreación didáctica, "
        "no metraje documental."
    )
    SUBTITLES.write_text(build_srt(subtitle_texts, scene_durations), encoding="utf-8")
    write_original_music(AUDIO_BED, video_seconds)

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit(
            f"Se generaron subtítulos en {SUBTITLES} y música original en {AUDIO_BED}, "
            "pero no se encontró ffmpeg en PATH. "
            "No se regeneraron los videos."
        )

    storyboard_path = ROOT / "docs" / "evidencias" / "2026-11-08" / "storyboard-cosecha.png"
    storyboard_path.parent.mkdir(parents=True, exist_ok=True)
    tile_width, tile_height = 384, 216
    storyboard = Image.new("RGB", (tile_width * 3, tile_height * 2), BG_TOP)
    storyboard_draw = ImageDraw.Draw(storyboard)
    elapsed = 0.0
    for index, duration in enumerate(scene_durations):
        preview_time = min(duration * 0.46, max(0.0, duration - 0.1))
        preview = draw_frame(index, preview_time, duration, elapsed / video_seconds)
        tile = preview.resize((tile_width, tile_height), Image.Resampling.LANCZOS)
        x = (index % 3) * tile_width
        y = (index // 3) * tile_height
        storyboard.paste(tile, (x, y))
        storyboard_draw.rounded_rectangle((x + 9, y + 8, x + 132, y + 34), radius=11, fill=(10, 27, 18))
        storyboard_draw.text((x + 18, y + 12), f"ESCENA {index + 1:02d}", font=F_TINY, fill=CREAM)
        elapsed += duration
    storyboard.save(storyboard_path, format="PNG", optimize=True)

    print(f"Narración: {audio_seconds:.1f}s; video: {video_seconds:.1f}s; frames: {frame_count}")
    print(f"Salida: {OUTPUT}")

    with tempfile.TemporaryDirectory(prefix="sakpokaab-video-") as temp_dir:
        silent_video = Path(temp_dir) / "cosecha-sin-audio.mp4"
        command = [
            ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-video_size", f"{WIDTH}x{HEIGHT}",
            "-framerate", str(FPS), "-i", "-", "-an",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-profile:v", "baseline", "-level:v", "3.1",
            "-g", str(FPS * 2), "-keyint_min", str(FPS), "-sc_threshold", "0",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(silent_video),
        ]
        process = subprocess.Popen(command, stdin=subprocess.PIPE)
        try:
            for frame_number in range(frame_count):
                time_s = frame_number / FPS
                elapsed = 0.0
                scene_index = len(SCENES) - 1
                local_time = 0.0
                for index, duration in enumerate(scene_durations):
                    if time_s < elapsed + duration or index == len(scene_durations) - 1:
                        scene_index = index
                        local_time = time_s - elapsed
                        break
                    elapsed += duration

                image = draw_frame(scene_index, local_time, scene_durations[scene_index], time_s / video_seconds)
                if frame_number == 0:
                    image.save(POSTER, format="PNG", optimize=True)
                assert process.stdin is not None
                process.stdin.write(image.tobytes())
                if frame_number % (FPS * 5) == 0:
                    print(f"Render {time_s:5.1f}/{video_seconds:5.1f}s")
        finally:
            if process.stdin:
                process.stdin.close()
        result = process.wait()
        if result != 0:
            raise SystemExit(f"FFmpeg falló al codificar frames (código {result}).")

        mux_command = [
            ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(silent_video), "-i", str(AUDIO), "-i", str(AUDIO_BED), "-i", str(SUBTITLES),
            "-filter_complex",
            "[1:a]loudnorm=I=-16:TP=-1.5:LRA=11[voice];"
            "[2:a]volume=0.3[music];"
            "[voice][music]amix=inputs=2:duration=longest:dropout_transition=2,"
            "loudnorm=I=-16:TP=-1.5:LRA=11[a]",
            "-map", "0:v:0", "-map", "[a]", "-map", "3:0", "-c:v", "copy", "-c:a", "aac",
            "-c:s", "mov_text",
            "-b:a", "160k", "-ar", "48000", "-shortest", "-movflags", "+faststart", str(OUTPUT),
        ]
        subprocess.run(mux_command, check=True)

        mobile_command = [
            ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(silent_video), "-i", str(AUDIO), "-i", str(AUDIO_BED), "-i", str(SUBTITLES),
            "-filter_complex",
            "[0:v]scale=640:360:flags=bicubic[v];"
            "[1:a]loudnorm=I=-16:TP=-1.5:LRA=11[voice];"
            "[2:a]volume=0.3[music];"
            "[voice][music]amix=inputs=2:duration=longest:dropout_transition=2,"
            "loudnorm=I=-16:TP=-1.5:LRA=11[a]",
            "-map", "[v]", "-map", "[a]", "-map", "3:0", "-c:v", "libx264", "-preset", "veryfast",
            "-crf", "23", "-profile:v", "baseline", "-level:v", "3.0",
            "-g", str(FPS * 2), "-keyint_min", str(FPS), "-sc_threshold", "0",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k", "-ar", "48000", "-c:s", "mov_text",
            "-shortest", "-movflags", "+faststart", str(OUTPUT_MOBILE),
        ]
        subprocess.run(mobile_command, check=True)

        social_command = [
            ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(OUTPUT),
            "-filter_complex",
            "[0:v]split=2[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,boxblur=30:10,eq=brightness=-0.18[background];"
            "[fg]scale=1080:608:force_original_aspect_ratio=decrease[foreground];"
            "[background][foreground]overlay=(W-w)/2:(H-h)/2,format=yuv420p[video]",
            "-map", "[video]", "-map", "0:a:0", "-map", "0:s:0",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
            "-profile:v", "baseline", "-level:v", "4.0", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-c:s", "mov_text",
            "-shortest", "-movflags", "+faststart", str(OUTPUT_SOCIAL),
        ]
        subprocess.run(social_command, check=True)

    print(f"VIDEO_OK: {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)")
    print(f"VIDEO_MOBILE_OK: {OUTPUT_MOBILE} ({OUTPUT_MOBILE.stat().st_size:,} bytes)")
    print(f"VIDEO_SOCIAL_OK: {OUTPUT_SOCIAL} ({OUTPUT_SOCIAL.stat().st_size:,} bytes)")
    print(f"SUBTITLES_OK: {SUBTITLES}")
    print(f"MUSIC_BED_OK: {AUDIO_BED} ({AUDIO_BED.stat().st_size:,} bytes)")
    print(f"POSTER_OK: {POSTER}")
    print(f"STORYBOARD_OK: {storyboard_path}")


if __name__ == "__main__":
    main()
