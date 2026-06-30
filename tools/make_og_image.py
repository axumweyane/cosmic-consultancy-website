# -*- coding: utf-8 -*-
"""Generate the 1200x630 Open Graph share image for Cosmic Consultancy Services.

Usage (from repo root or anywhere):
    pip install Pillow
    python tools/make_og_image.py

Output: assets/img/og-cover.png  (referenced by og:image / twitter:image on every page)
Fonts: uses Segoe UI / Arial from the local system; falls back if unavailable.
"""
import os
from PIL import Image, ImageDraw, ImageFont

SS = 2                      # supersample factor (rendered at 2x then downsampled)
W, H = 1200 * SS, 630 * SS

# Output path is resolved relative to this script, so it works from any CWD.
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "assets", "img", "og-cover.png")

# ---- brand palette ----
BG_TOP   = (11, 18, 32)     # #0b1220
BG_BOT   = (13, 26, 48)     # #0d1a30
BLUE     = (76, 194, 255)   # #4cc2ff
BLUE_LT  = (127, 214, 255)  # #7fd6ff
WHITE    = (255, 255, 255)
MUTED    = (150, 173, 196)  # slate

FONT_DIR = r"C:\Windows\Fonts"
def font(names, size):
    for n in names:
        p = os.path.join(FONT_DIR, n)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

BOLD = ["segoeuib.ttf", "arialbd.ttf", "calibrib.ttf"]
SEMI = ["seguisb.ttf", "segoeuib.ttf", "arialbd.ttf"]
REG  = ["segoeui.ttf", "arial.ttf", "calibri.ttf"]

# ---- canvas + vertical gradient ----
img = Image.new("RGB", (W, H), BG_TOP)
d = ImageDraw.Draw(img)
for y in range(H):
    t = y / (H - 1)
    r = int(BG_TOP[0] + (BG_BOT[0] - BG_TOP[0]) * t)
    g = int(BG_TOP[1] + (BG_BOT[1] - BG_TOP[1]) * t)
    b = int(BG_TOP[2] + (BG_BOT[2] - BG_TOP[2]) * t)
    d.line([(0, y), (W, y)], fill=(r, g, b))

# ---- soft radial glow behind the orbit (right side) ----
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
cx, cy = int(W * 0.78), int(H * 0.44)
for i in range(140, 0, -1):
    a = int(42 * (i / 140) ** 2)
    rad = int(i * 3.2 * SS)
    gd.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(76, 194, 255, a // 6))
img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img)

# ---- orbit decoration (rotated rings + core + planets) on its own layer ----
orb = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(orb)
def ring(rx, ry, w, col):
    od.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=col, width=w)
ring(360 * SS, 150 * SS, 3 * SS, (76, 194, 255, 90))
ring(270 * SS, 112 * SS, 3 * SS, (76, 194, 255, 130))
ring(180 * SS, 74 * SS,  3 * SS, (127, 214, 255, 160))
orb = orb.rotate(-24, resample=Image.BICUBIC, center=(cx, cy))
od = ImageDraw.Draw(orb)
# glowing core
for i in range(40, 0, -1):
    a = int(180 * (i / 40) ** 2)
    rad = int(i * 0.9 * SS)
    od.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(76, 194, 255, a // 3))
od.ellipse([cx - 22 * SS, cy - 22 * SS, cx + 22 * SS, cy + 22 * SS], fill=(127, 214, 255, 255))
# a few planets sitting on the rings
for px, py, pr, c in [
    (cx + 352 * SS, cy - 70 * SS, 9 * SS, BLUE_LT),
    (cx + 300 * SS, cy + 150 * SS, 7 * SS, BLUE),
    (cx + 150 * SS, cy + 200 * SS, 6 * SS, BLUE_LT),
]:
    od.ellipse([px - pr, py - pr, px + pr, py + pr], fill=c + (255,))
img.paste(Image.alpha_composite(img.convert("RGBA"), orb).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img)

# ---- helpers ----
def text_w(s, f):
    return d.textbbox((0, 0), s, font=f)[2]

def draw_tracked(x, y, s, f, fill, track):
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill)
        x += text_w(ch, f) + track
    return x

PAD = 80 * SS

# ---- eyebrow ----
eb = font(SEMI, 24 * SS)
draw_tracked(PAD, 150 * SS, "TECHNOLOGY  CONSULTANCY", eb, BLUE, 6 * SS)

# ---- title (auto-fit, two-tone) : "Cosmic Consultancy Services" ----
maxw = W - PAD - 360 * SS
size = 104 * SS
while size > 40 * SS:
    tf = font(BOLD, size)
    if text_w("Cosmic Consultancy Services", tf) <= maxw:
        break
    size -= 2 * SS
tf = font(BOLD, size)
ty = 196 * SS
x = PAD
for seg, col in [("Cosmic ", WHITE), ("Consultancy ", BLUE), ("Services", WHITE)]:
    d.text((x, ty), seg, font=tf, fill=col)
    x += text_w(seg, tf)
# accent bar under title
bar_y = ty + size + 14 * SS
d.rectangle([PAD, bar_y, PAD + 120 * SS, bar_y + 6 * SS], fill=BLUE)

# ---- subtitle ----
sf = font(REG, 34 * SS)
d.text((PAD, bar_y + 34 * SS), "One accountable partner across your entire stack",
       font=sf, fill=MUTED)

# ---- service chips: Cloud · AI · Security · Data · ERP · CRM ----
cf = font(SEMI, 30 * SS)
chips = ["Cloud", "AI", "Security", "Data", "ERP", "CRM"]
cxp = PAD
cyp = bar_y + 104 * SS
for i, c in enumerate(chips):
    if i:
        cxp = draw_tracked(cxp, cyp, "  ", cf, MUTED, 0)
        d.ellipse([cxp, cyp + 16 * SS, cxp + 8 * SS, cyp + 24 * SS], fill=BLUE)
        cxp += 8 * SS
        cxp = draw_tracked(cxp, cyp, "  ", cf, MUTED, 0)
    d.text((cxp, cyp), c, font=cf, fill=WHITE)
    cxp += text_w(c, cf)

# ---- footer domain ----
ff = font(SEMI, 28 * SS)
d.text((PAD, H - 80 * SS), "cosmicconsultancyservices.com", font=ff, fill=BLUE_LT)

# ---- downsample for anti-aliasing & save ----
final = img.resize((1200, 630), Image.LANCZOS)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
final.save(OUT, "PNG", optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
