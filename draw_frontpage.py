"""Drawing helpers for the 22 November 2026 front page.

Everything here is original flat art drawn with PIL primitives:
a Pentagon scene, a courtroom, a Gulf tanker, a three-flag summit,
a quake seismograph, a missile over Poland and a credit card.
No photos, no network, no external assets — only DejaVu fonts
already present on the system, with a built-in fallback.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024

PAPER = (248, 244, 233)
INK = (24, 24, 20)
RED = (178, 30, 30)
DARK_RED = (126, 18, 18)
NAVY = (20, 32, 52)
STEEL = (38, 66, 104)
GREY = (110, 108, 98)
RULE = (74, 70, 60)
PANEL = (234, 228, 211)
GOLD = (216, 166, 34)
SKY = (46, 74, 118)

SERIF_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load_font(path, size):
    """Open a TTF at `size`; fall back to PIL's bitmap font."""
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def fit_lines(text, fnt, width):
    """Split `text` into lines that fit `width` in font `fnt`."""
    out = []
    current = ""
    for word in text.split():
        candidate = word if not current else current + " " + word
        if fnt.getlength(candidate) <= width:
            current = candidate
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def text_block(draw, x, y, text, fnt, width, fill=INK, spacing=None):
    """Draw `text` wrapped to `width`; return y below the last line."""
    if spacing is None:
        spacing = int(fnt.size * 1.35)
    for line in fit_lines(text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += spacing
    return y


def hline(draw, x0, x1, y, weight=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=weight)


def double_hline(draw, x0, x1, y, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=3)
    draw.line([(x0, y + 5), (x1, y + 5)], fill=fill, width=1)


def burst(draw, cx, cy, radius, spikes=12, colour=(255, 142, 26)):
    """A starburst explosion centred on (cx, cy)."""
    points = []
    for i in range(spikes * 2):
        angle = math.pi * i / spikes
        r = radius if i % 2 == 0 else radius * 0.4
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=colour)
    draw.ellipse([cx - radius * 0.3, cy - radius * 0.3,
                  cx + radius * 0.3, cy + radius * 0.3],
                 fill=(255, 212, 64))


def _inside_polygon(px, py, poly):
    """Ray-casting point-in-polygon test."""
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > py) != (y2 > py):
            x_at = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if px < x_at:
                inside = not inside
    return inside


def _us_flag(draw, x, y, w, h):
    for i in range(7):
        colour = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                       fill=colour)
    draw.rectangle([x, y, x + int(w * 0.42), y + int(h * 0.57)],
                   fill=(30, 48, 96))
    for r in range(3):
        for c in range(4):
            sx = x + 6 + c * 12
            sy = y + 5 + r * 9
            draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))


def _canada_flag(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    draw.rectangle([x, y, x + w // 4, y + h], fill=(255, 0, 0))
    draw.rectangle([x + 3 * w // 4, y, x + w, y + h], fill=(255, 0, 0))
    cx, cy = x + w // 2, y + h // 2
    # a simple maple leaf: a diamond with side lobes
    draw.polygon([(cx, cy - h // 2 + 3), (cx + 7, cy - 6), (cx + 12, cy - 12),
                  (cx + 6, cy - 8), (cx + 10, cy - 2), (cx + 4, cy + 2),
                  (cx + 5, cy + 8), (cx + 2, cy + 6), (cx, cy + 12),
                  (cx - 2, cy + 6), (cx - 5, cy + 8), (cx - 4, cy + 2),
                  (cx - 10, cy - 2), (cx - 6, cy - 8), (cx - 12, cy - 12),
                  (cx - 7, cy - 6)], fill=(255, 0, 0))


def _china_flag(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    burst(draw, x + 13, y + 12, 7, spikes=5, colour=(255, 222, 0))
    burst(draw, x + 31, y + 7, 3, spikes=5, colour=(255, 222, 0))
    burst(draw, x + 35, y + 17, 3, spikes=5, colour=(255, 222, 0))


def _russia_flag(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h // 3], fill=(255, 255, 255))
    draw.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(213, 0, 50))


def draw_pentagon_scene(img, x, y, w, h):
    """The Pentagon at dusk, flanked by the US and Canadian flags,
    with a red barrier stripe cutting between them."""
    draw = ImageDraw.Draw(img)
    top = (30, 44, 80)
    bottom = (96, 108, 130)
    for i in range(h):
        t = i / max(h - 1, 1)
        colour = tuple(int(top[k] + (bottom[k] - top[k]) * t)
                       for k in range(3))
        draw.line([(x, y + i), (x + w, y + i)], fill=colour)
    rng = random.Random(7)
    for _ in range(20):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, int(h * 0.32))
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(232, 232, 214))
    ground = y + h - 30
    draw.rectangle([x, ground, x + w, y + h], fill=(52, 58, 52))
    # the Pentagon: a five-sided block with a courtyard
    cx = x + w // 2
    cy = ground - 62
    outer = []
    for k in range(5):
        ang = -math.pi / 2 + k * 2 * math.pi / 5
        outer.append((cx + 118 * math.cos(ang), cy + 52 * math.sin(ang) + 14))
    draw.polygon(outer, fill=(178, 172, 158), outline=INK)
    inner = []
    for k in range(5):
        ang = -math.pi / 2 + k * 2 * math.pi / 5
        inner.append((cx + 46 * math.cos(ang), cy + 20 * math.sin(ang) + 14))
    draw.polygon(inner, fill=(96, 104, 92), outline=INK)
    # lit windows along the front face, kept inside the pentagon
    rng = random.Random(13)
    placed = 0
    tries = 0
    while placed < 24 and tries < 200:
        tries += 1
        wx = cx - 104 + rng.randint(0, 208)
        wy = ground - 58 + rng.randint(0, 28)
        if _inside_polygon(wx + 2, wy + 3, outer):
            draw.rectangle([wx, wy, wx + 5, wy + 7], fill=(255, 198, 70))
            placed += 1
    # flag poles: US on the left, Canada on the right
    for px, flag in ((x + 52, _us_flag), (x + w - 52, _canada_flag)):
        draw.line([(px, y + 22), (px, ground)], fill=(216, 216, 206), width=4)
        flag(draw, px + 4, y + 24, 62, 38)
        draw.rectangle([px + 4, y + 24, px + 66, y + 62], outline=INK, width=1)
    # red barrier tape across the middle, between the flags
    draw.rectangle([x, ground - 12, x + w, ground - 2], fill=RED)
    for k in range(0, w, 44):
        draw.polygon([(x + k, ground - 2), (x + k + 22, ground - 12),
                      (x + k + 44, ground - 12), (x + k + 22, ground - 2)],
                     fill=(255, 255, 255))
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)


def draw_court_scene(img, x, y, w, h):
    """The World Court: tall columns, the scales of justice and a
    judge's bench with a gavel."""
    draw = ImageDraw.Draw(img)
    draw.rectangle([x, y, x + w, y + h], fill=(44, 56, 84))
    # marble columns
    for cx in (x + 34, x + w - 34):
        draw.rectangle([cx - 12, y + 8, cx + 12, y + h - 34],
                       fill=(214, 206, 188), outline=INK, width=1)
        draw.rectangle([cx - 18, y + 4, cx + 18, y + 12],
                       fill=(196, 188, 170))
        draw.rectangle([cx - 18, y + h - 42, cx + 18, y + h - 34],
                       fill=(196, 188, 170))
    # scales of justice, centred
    cx, cy = x + w // 2, y + 34
    draw.line([(cx, cy - 12), (cx, cy + 30)], fill=GOLD, width=3)
    draw.line([(cx - 34, cy - 6), (cx + 34, cy - 6)], fill=GOLD, width=3)
    for sx in (cx - 34, cx + 34):
        draw.line([(sx, cy - 6), (sx, cy + 16)], fill=GOLD, width=2)
        draw.pieslice([sx - 13, cy + 14, sx + 13, cy + 34],
                      start=0, end=180, fill=GOLD)
    # judge's bench
    draw.rectangle([x + 14, y + h - 34, x + w - 14, y + h - 6],
                   fill=(104, 70, 40))
    draw.rectangle([x + 14, y + h - 34, x + w - 14, y + h - 26],
                   fill=(136, 94, 56))
    # gavel resting on the bench
    draw.line([(x + 52, y + h - 18), (x + 92, y + h - 24)],
              fill=(60, 40, 24), width=5)
    draw.rectangle([x + 92, y + h - 32, x + 112, y + h - 16],
                   fill=(150, 110, 66))
    draw.ellipse([x + 46, y + h - 16, x + 76, y + h - 8],
                 fill=(170, 130, 80))
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)


def draw_gulf_scene(img, x, y, w, h):
    """A tanker in the Gulf at sunset, burning after a strike,
    with smoke rising and a second ship on the horizon."""
    draw = ImageDraw.Draw(img)
    top = (250, 164, 74)
    bottom = (70, 96, 138)
    for i in range(h):
        t = i / max(h - 1, 1)
        colour = tuple(int(top[k] + (bottom[k] - top[k]) * t)
                       for k in range(3))
        draw.line([(x, y + i), (x + w, y + i)], fill=colour)
    sea = y + int(h * 0.62)
    draw.rectangle([x, sea, x + w, y + h], fill=(24, 52, 88))
    for k in range(6):
        wx = x + 20 + k * 52
        draw.arc([wx, sea + 12, wx + 34, sea + 30], start=200, end=340,
                 fill=(120, 160, 200), width=2)
    # sun low on the horizon
    draw.ellipse([x + w - 78, y + 12, x + w - 34, y + 56],
                 fill=(255, 196, 66))
    # the tanker: hull, deck, bridge tower, funnel
    hx0, hx1 = x + 36, x + w - 60
    hy = sea + 22
    draw.polygon([(hx0, hy), (hx1, hy), (hx1 - 22, hy + 26),
                  (hx0 + 14, hy + 26)], fill=(120, 30, 30), outline=INK)
    draw.rectangle([hx0 + 30, hy - 22, hx0 + 150, hy], fill=(200, 190, 170),
                   outline=INK)
    draw.rectangle([hx1 - 66, hy - 46, hx1 - 22, hy - 22],
                   fill=(240, 240, 230), outline=INK)
    draw.rectangle([hx1 - 12, hy - 58, hx1 - 2, hy - 22],
                   fill=(30, 30, 30))
    # fire and smoke from the deck
    burst(draw, hx0 + 90, hy - 30, 22, colour=(255, 120, 30))
    burst(draw, hx0 + 130, hy - 22, 15, colour=(255, 150, 40))
    for cx, cy, r in [(hx0 + 96, hy - 52, 20), (hx0 + 120, hy - 62, 15)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 66, 72))
    # a second tanker on the horizon
    draw.rectangle([x + w - 120, sea - 8, x + w - 44, sea + 4],
                   fill=(60, 60, 70))
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)


def draw_summit_scene(img, x, y, w, h):
    """Three flags — US, China, Russia — over a summit table,
    with an atom emblem between them."""
    draw = ImageDraw.Draw(img)
    draw.rectangle([x, y, x + w, y + h], fill=(46, 58, 84))
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(100, 72, 46))
    draw.rectangle([x, y + h - 32, x + w, y + h - 26], fill=(154, 116, 72))
    fw, fh = 72, 42
    gap = (w - 3 * fw) // 4
    for i, flag in enumerate((_us_flag, _china_flag, _russia_flag)):
        fx = x + gap + i * (fw + gap)
        fy = y + 10
        draw.line([(fx + fw // 2, fy), (fx + fw // 2, y + h - 32)],
                  fill=(204, 204, 194), width=3)
        flag(draw, fx, fy + 4, fw, fh)
        draw.rectangle([fx, fy + 4, fx + fw, fy + 4 + fh], outline=INK, width=1)
    # atom emblem floating above the table, between the flags
    ax, ay = x + w // 2, y + h - 56
    for start in (0, 60, 120):
        draw.arc([ax - 26, ay - 12, ax + 26, ay + 12], start=start,
                 end=start + 150, fill=GOLD, width=2)
    draw.ellipse([ax - 4, ay - 4, ax + 4, ay + 4], fill=GOLD)
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)


def draw_quake_icon(img, x, y, s):
    """Andes peaks with a seismograph zig-zag across them."""
    draw = ImageDraw.Draw(img)
    draw.rectangle([x, y, x + s, y + s], fill=(228, 220, 200))
    base = y + s - 8
    draw.polygon([(x + 2, base), (x + 18, y + 18), (x + 34, base)],
                 fill=(96, 84, 70))
    draw.polygon([(x + 22, base), (x + 40, y + 8), (x + 58, base)],
                 fill=(70, 60, 50))
    draw.polygon([(x + 14, y + 24), (x + 18, y + 18), (x + 22, y + 24),
                  (x + 18, y + 30)], fill=(255, 255, 255))
    draw.polygon([(x + 36, y + 14), (x + 40, y + 8), (x + 44, y + 14),
                  (x + 40, y + 20)], fill=(255, 255, 255))
    # seismograph trace
    pts = [(x + 4, y + s * 0.52), (x + 14, y + s * 0.52), (x + 18, y + s * 0.30),
           (x + 22, y + s * 0.74), (x + 26, y + s * 0.52), (x + 36, y + s * 0.52),
           (x + 40, y + s * 0.24), (x + 44, y + s * 0.80), (x + 48, y + s * 0.52),
           (x + 58, y + s * 0.52)]
    draw.line(pts, fill=RED, width=2)
    draw.rectangle([x, y, x + s - 1, y + s - 1], outline=INK, width=2)


def draw_missile_icon(img, x, y, s):
    """A missile streaking down past the white-and-red Polish flag."""
    draw = ImageDraw.Draw(img)
    draw.rectangle([x, y, x + s, y + s], fill=(36, 52, 92))
    rng = random.Random(19)
    for _ in range(8):
        sx = x + rng.randint(4, s - 4)
        sy = y + rng.randint(4, s // 3)
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(220, 220, 200))
    # Polish flag on a pole
    px = x + 8
    draw.line([(px, y + 10), (px, y + s - 8)], fill=(216, 216, 206), width=3)
    draw.rectangle([px + 3, y + 12, px + 29, y + 25], fill=(255, 255, 255))
    draw.rectangle([px + 3, y + 25, px + 29, y + 38], fill=(220, 20, 60))
    # falling missile with a fire trail
    mx, my = x + s - 22, y + 12
    draw.line([(mx - 14, my - 8), (mx + 4, my + 26)], fill=(255, 200, 90),
              width=3)
    draw.polygon([(mx, my), (mx + 10, my + 4), (mx + 2, my + 22),
                  (mx - 6, my + 14)], fill=(200, 200, 190), outline=INK)
    burst(draw, mx - 6, my + 30, 9, spikes=8, colour=(255, 140, 26))
    draw.rectangle([x, y, x + s - 1, y + s - 1], outline=INK, width=2)


def draw_card_icon(img, x, y, s):
    """A credit card stamped with a big 10%."""
    draw = ImageDraw.Draw(img)
    draw.rectangle([x, y, x + s, y + s], fill=(226, 236, 244))
    draw.rounded_rectangle([x + 4, y + 12, x + s - 4, y + s - 12], radius=6,
                           fill=STEEL, outline=INK, width=2)
    draw.rectangle([x + 4, y + 20, x + s - 4, y + 30], fill=(20, 20, 24))
    fnt = load_font(SANS_BOLD_PATH, 20)
    draw.text((x + 10, y + 30), "10%", font=fnt, fill=(255, 255, 255))
    draw.rectangle([x, y, x + s - 1, y + s - 1], outline=INK, width=2)
