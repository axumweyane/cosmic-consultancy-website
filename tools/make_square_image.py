# -*- coding: utf-8 -*-
"""Generate the 1080x1080 square (Instagram) brand image for Cosmic Consultancy Services.

Usage:
    pip install Pillow
    python tools/make_square_image.py

Output: assets/img/og-square.png  (square social card — centered composition)
"""
import os
from PIL import Image, ImageDraw, ImageFont

SS = 2                      # supersample factor
W = H = 1080 * SS

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "assets", "img", "og-square.png")

# ---- brand palette ----
BG_TOP   = (11, 18, 32)     # #0b1220
BG_BOT   = (13, 26, 48)     # #0d1a30
BLUE     = (76, 194, 255)   # #4cc2ff
BLUE_LT  = (127, 214, 255)  # #7fd6ff
WHITE    = (255, 255, 255)
MUTED    = (150, 173, 196)

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

cx, cy = W // 2, H // 2

# ---- faint full-bleed orbit backdrop (centered, low opacity) ----
bg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(bg)
def ring(dd, ox, oy, rx, ry, w, col):
    dd.ellipse([ox - rx, oy - ry, ox + rx, oy + ry], outline=col, width=w)
ring(bd, cx, cy, 520 * SS, 210 * SS, 3 * SS, (76, 194, 255, 45))
ring(bd, cx, cy, 400 * SS, 160 * SS, 3 * SS, (76, 194, 255, 60))
ring(bd, cx, cy, 280 * SS, 112 * SS, 3 * SS, (127, 214, 255, 70))
bg = bg.rotate(-22, resample=Image.BICUBIC, center=(cx, cy))
img.paste(Image.alpha_composite(img.convert("RGBA"), bg).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img)

# ---- helpers ----
def text_w(s, f):
    return d.textbbox((0, 0), s, font=f)[2]

def center(s, f, y, fill):
    d.text(((W - text_w(s, f)) // 2, y), s, font=f, fill=fill)

def center_tracked(s, f, y, fill, track):
    total = sum(text_w(ch, f) + track for ch in s) - track
    x = (W - total) // 2
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill)
        x += text_w(ch, f) + track

# ---- logo mark (orbit icon) at top center ----
mark = Image.new("RGBA", (W, H), (0, 0, 0, 0))
md = ImageDraw.Draw(mark)
mcy = 250 * SS
ring(md, cx, mcy, 92 * SS, 38 * SS, 5 * SS, (76, 194, 255, 230))
mark = mark.rotate(-22, resample=Image.BICUBIC, center=(cx, mcy))
md = ImageDraw.Draw(mark)
for i in range(34, 0, -1):
    a = int(180 * (i / 34) ** 2)
    rad = int(i * 1.0 * SS)
    md.ellipse([cx - rad, mcy - rad, cx + rad, mcy + rad], fill=(76, 194, 255, a // 3))
md.ellipse([cx - 26 * SS, mcy - 26 * SS, cx + 26 * SS, mcy + 26 * SS], fill=(127, 214, 255, 255))
md.ellipse([cx + 78 * SS, mcy - 30 * SS, cx + 90 * SS, mcy - 18 * SS], fill=(127, 214, 255, 255))
img.paste(Image.alpha_composite(img.convert("RGBA"), mark).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img)

# ---- eyebrow ----
eb = font(SEMI, 30 * SS)
center_tracked("TECHNOLOGY  CONSULTANCY", eb, 358 * SS, BLUE, 8 * SS)

# ---- stacked wordmark (auto-fit to widest word, capped so the layout fits) ----
PAD = 110 * SS
maxw = W - 2 * PAD
size = 112 * SS
while size > 60 * SS:
    tf = font(BOLD, size)
    if text_w("Consultancy", tf) <= maxw:
        break
    size -= 2 * SS
tf = font(BOLD, size)
line_h = int(size * 1.02)
y0 = 432 * SS
for i, (word, col) in enumerate([("Cosmic", WHITE), ("Consultancy", BLUE), ("Services", WHITE)]):
    center(word, tf, y0 + i * line_h, col)

# ---- accent bar (centered) ----
bar_y = y0 + 3 * line_h + 24 * SS
bw = 140 * SS
d.rectangle([cx - bw // 2, bar_y, cx + bw // 2, bar_y + 7 * SS], fill=BLUE)

# ---- subtitle ----
sf = font(REG, 36 * SS)
center("One accountable partner across your entire stack", sf, bar_y + 40 * SS, MUTED)

# ---- service chips: Cloud · AI · Security · Data · ERP · CRM (centered, one row) ----
cf = font(SEMI, 34 * SS)
chips = ["Cloud", "AI", "Security", "Data", "ERP", "CRM"]
gap = 24 * SS
dot = 9 * SS
seg_w = [text_w(c, cf) for c in chips]
total = sum(seg_w) + (len(chips) - 1) * (gap * 2 + dot)
x = (W - total) // 2
cyp = bar_y + 118 * SS
for i, c in enumerate(chips):
    if i:
        x += gap
        d.ellipse([x, cyp + 18 * SS, x + dot, cyp + 18 * SS + dot], fill=BLUE)
        x += dot + gap
    d.text((x, cyp), c, font=cf, fill=WHITE)
    x += seg_w[i]

# ---- footer domain ----
ff = font(SEMI, 34 * SS)
center("cosmicconsultancyservices.com", ff, H - 96 * SS, BLUE_LT)

# ---- downsample & save ----
final = img.resize((1080, 1080), Image.LANCZOS)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
final.save(OUT, "PNG", optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
