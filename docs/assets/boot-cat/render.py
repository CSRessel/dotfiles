#!/usr/bin/env python3
"""Render the website's Unicode cat. Requires python3-gi-cairo, python3-cairo,
gir1.2-pango-1.0 and the fonts module. Run from any directory.
"""
from pathlib import Path
import unicodedata
import cairo
import gi

gi.require_foreign("cairo")
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Pango, PangoCairo

ROOT = Path(__file__).resolve().parent
ART = (ROOT / "cat.txt").read_text().rstrip("\n")


def text(ctx, value, size, x, y, color=1, centered=False, mono=False):
    layout = PangoCairo.create_layout(ctx)
    font = Pango.FontDescription("FiraCode Nerd Font Mono" if mono else "IBM Plex Sans")
    font.set_absolute_size(size * Pango.SCALE)
    layout.set_font_description(font)
    layout.set_text(value, -1)
    width, height = layout.get_pixel_size()
    ctx.move_to(x - width / 2 if centered else x, y)
    ctx.set_source_rgb(color, color, color)
    PangoCairo.show_layout(ctx, layout)
    return width, height


def surface(w, h, black=False):
    img = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(img)
    if black:
        ctx.set_source_rgb(0, 0, 0)
        ctx.paint()
    return img, ctx


# Position glyphs by terminal columns, rather than fallback-font advances.
# Full-width Japanese characters occupy two cells; variation selectors none.
def columns(char):
    return 2 if unicodedata.east_asian_width(char) in ("W", "F") or char in "🖥⌨" else 1


def render_cat(art):
    raw, rc = surface(640, 448)
    lines = [line.replace("\ufe0f", "") for line in art.splitlines()]
    cell = 19.2
    left = (640 - 16 * cell) / 2
    for row, line in enumerate(lines):
        column = 0
        for char in line:
            width = columns(char)
            if not char.isspace():
                glyph = char + "\ufe0f" if char in "🖥⌨" else char
                text(rc, glyph, 32, left + (column + width / 2) * cell,
                     28 + row * 42, centered=True, mono=True)
            column += width
    cat, cc = surface(640, 448)
    cc.set_source_rgb(1, 1, 1)
    # Preserve glyph alpha while making color emoji white.
    cc.mask_surface(raw, 0, 0)
    return cat


def place_cat(ctx, cx, top, scale, artwork):
    ctx.save()
    ctx.translate(cx - 320 * scale, top)
    ctx.scale(scale, scale)
    ctx.set_source_surface(artwork, 0, 0)
    ctx.paint()
    ctx.restore()


# Four clean held-object variants: no separate desktop or keyboard.
for name, emoji in {"coffee": "☕", "key": "🔑", "laptop": "💻", "lock": "🔒"}.items():
    art = ART.replace("🖥️", "").replace("⌨️", "").replace("☕", emoji)
    artwork = render_cat(art)
    artwork.write_to_png(str(ROOT / f"{name}-transparent.png"))
    img, ctx = surface(640, 448, True)
    place_cat(ctx, 320, 0, 1, artwork)
    img.write_to_png(str(ROOT / f"{name}-black.png"))
    img, ctx = surface(1920, 1200, True)
    place_cat(ctx, 340, 530, .9, artwork)
    img.write_to_png(str(ROOT / f"{name}-left.png"))

    if name in ("coffee", "lock"):
        img, ctx = surface(320, 224)
        ctx.scale(.5, .5)
        ctx.set_source_surface(artwork, 0, 0)
        ctx.paint()
        img.write_to_png(str(ROOT / f"{name}-plymouth.png"))
