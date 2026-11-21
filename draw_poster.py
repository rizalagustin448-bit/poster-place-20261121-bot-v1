"""Draw the AERLUME travel poster (build-time only, Pillow allowed here).
main.py (the submitted program) is stdlib-only and just copies poster.png.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1024
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

img = Image.new("RGB", (W, H))
px = img.load()

# --- sky gradient: deep indigo top -> violet -> amber horizon (sunset) ---
top = (24, 24, 64)
mid = (94, 52, 96)
low = (214, 110, 66)
bot = (247, 178, 96)
for y in range(H):
    t = y / H
    if t < 0.45:
        f = t / 0.45
        c = tuple(int(top[i] + (mid[i] - top[i]) * f) for i in range(3))
    elif t < 0.75:
        f = (t - 0.45) / 0.30
        c = tuple(int(mid[i] + (low[i] - mid[i]) * f) for i in range(3))
    else:
        f = (t - 0.75) / 0.25
        c = tuple(int(low[i] + (bot[i] - low[i]) * f) for i in range(3))
    for x in range(W):
        px[x, y] = c

d = ImageDraw.Draw(img, "RGBA")

# --- sun: low glowing disc behind the island ---
sun_cx, sun_cy, sun_r = 512, 640, 150
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for r, a in ((260, 26), (220, 42), (185, 70)):
    gd.ellipse([sun_cx - r, sun_cy - r, sun_cx + r, sun_cy + r],
               fill=(255, 196, 110, a))
glow = glow.filter(ImageFilter.GaussianBlur(18))
img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img, "RGBA")
d.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
          fill=(255, 222, 150, 255))
d.ellipse([sun_cx - sun_r + 26, sun_cy - sun_r + 26,
           sun_cx + sun_r - 26, sun_cy + sun_r - 26], fill=(255, 236, 180, 255))

# --- stars in the upper sky ---
import random
random.seed(7)
for _ in range(90):
    x = random.randint(20, W - 20)
    y = random.randint(24, 330)
    r = random.choice([1, 1, 2])
    a = random.randint(90, 210)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 240, 210, a))

# --- distant cloud sea (soft horizontal bands, warm-lit tops) ---
def cloud_band(y0, h, base_col, top_col, seed):
    random.seed(seed)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    x = -120
    while x < W + 120:
        w = random.randint(180, 320)
        hh = random.randint(int(h * 0.55), h)
        ld.ellipse([x, y0 + h - hh, x + w, y0 + h], fill=base_col + (255,))
        x += random.randint(120, 200)
    layer = layer.filter(ImageFilter.GaussianBlur(10))
    img.paste(Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB"), (0, 0))
    # warm rim on top of the band
    d2 = ImageDraw.Draw(img, "RGBA")
    x = -100
    random.seed(seed + 1)
    while x < W + 100:
        w = random.randint(150, 280)
        d2.ellipse([x, y0 - 8, x + w, y0 + 26], fill=top_col + (200,))
        x += random.randint(140, 220)

cloud_band(700, 130, (226, 158, 118), (255, 214, 160), 11)
cloud_band(800, 150, (196, 122, 110), (255, 196, 140), 23)
cloud_band(900, 140, (158, 92, 104), (240, 170, 130), 37)

# --- floating island: dark rock silhouette with warm rim ---
rock = [(330, 700), (390, 640), (470, 612), (560, 606), (640, 640),
        (700, 700), (660, 780), (600, 860), (540, 930), (512, 962),
        (486, 920), (430, 850), (370, 780)]
d.polygon(rock, fill=(38, 26, 48, 255))
# warm rim light on the rock's sun side (right edge)
rim = [(640, 640), (700, 700), (660, 780), (600, 860), (540, 930),
       (512, 962), (528, 940), (566, 872), (622, 792), (668, 716)]
d.polygon(rim, fill=(255, 178, 110, 255))
# grassy top of the island
d.polygon([(330, 700), (390, 640), (470, 612), (560, 606), (640, 640),
           (700, 700), (690, 712), (340, 712)], fill=(52, 74, 52, 255))
# hanging roots / small rocks falling off the island
for (x, y, r) in ((430, 880, 10), (600, 900, 8), (512, 990, 6), (380, 820, 7)):
    d.ellipse([x - r, y - r, x + r, y + r], fill=(38, 26, 48, 255))

# --- lighthouse on the island ---
# tower (tapered), gallery, lamp room, dome
d.polygon([(488, 612), (536, 612), (530, 470), (494, 470)], fill=(244, 232, 208, 255))
d.polygon([(488, 612), (504, 612), (501, 470), (494, 470)], fill=(214, 196, 164, 255))
# red bands on the tower
for (y0, y1) in ((560, 586), (510, 534)):
    xa = 488 + (612 - y1) * (48 / 142) * 0 + (y1 - 470) * 0  # placeholder, replaced below
# (bands drawn as quads to follow the taper)
def band(y_top, y_bot):
    wt = 494 + (612 - y_top) * (6 / 142)
    wb = 494 + (612 - y_bot) * (6 / 142)
    wt2 = 530 - (612 - y_top) * (6 / 142)
    wb2 = 530 - (612 - y_bot) * (6 / 142)
    d.polygon([(wt, y_top), (wt2, y_top), (wb2, y_bot), (wb, y_bot)],
              fill=(178, 64, 52, 255))
band(556, 584)
band(508, 534)
# gallery + railing
d.rectangle([482, 458, 542, 472], fill=(40, 28, 52, 255))
for x in range(486, 540, 9):
    d.line([x, 448, x, 458], fill=(40, 28, 52, 255), width=2)
d.rectangle([484, 446, 540, 450], fill=(40, 28, 52, 255))
# lamp room (glowing)
d.rectangle([494, 420, 530, 448], fill=(255, 214, 130, 255))
d.rectangle([494, 420, 530, 448], outline=(40, 28, 52, 255), width=3)
d.line([512, 420, 512, 448], fill=(40, 28, 52, 255), width=2)
# dome + spire
d.polygon([(490, 420), (534, 420), (512, 398)], fill=(178, 64, 52, 255))
d.line([512, 398, 512, 384], fill=(40, 28, 52, 255), width=3)
d.ellipse([508, 380, 516, 388], fill=(255, 214, 130, 255))
# light beams from the lamp (near-horizontal, both sides)
for (x0, y0, x1, y1) in ((494, 434, 296, 418), (494, 434, 306, 450),
                          (530, 434, 728, 418), (530, 434, 718, 450)):
    d.polygon([(494 if x0 < 512 else 530, 428), (494 if x0 < 512 else 530, 442),
               (x1, y1 + 14), (x1, y1 - 14)], fill=(255, 226, 150, 60))

# --- airship, right side, warm windows ---
bx, by = 730, 300
d.ellipse([bx - 95, by - 42, bx + 95, by + 42], fill=(96, 52, 84, 255))
d.ellipse([bx - 95, by - 42, bx + 95, by - 2], fill=(126, 72, 104, 255))
d.ellipse([bx - 60, by - 34, bx + 20, by - 6], fill=(150, 92, 124, 255))
d.polygon([(bx - 40, by + 30), (bx + 40, by + 30), (bx + 30, by + 52),
           (bx - 30, by + 52)], fill=(52, 34, 56, 255))
for wx in range(bx - 24, bx + 25, 14):
    d.ellipse([wx - 3, by + 36, wx + 3, by + 42], fill=(255, 214, 130, 255))
d.line([bx + 80, by - 8, bx + 118, by - 26], fill=(52, 34, 56, 255), width=3)
d.polygon([(bx + 112, by - 34), (bx + 126, by - 22), (bx + 112, by - 16)],
          fill=(178, 64, 52, 255))
d.line([bx, by + 34, bx, by + 52], fill=(52, 34, 56, 255), width=2)

# --- birds ---
for (x, y, s) in ((250, 260, 12), (290, 300, 9), (760, 200, 11), (820, 250, 8)):
    d.arc([x - s, y - s, x, y + s], 200, 340, fill=(40, 28, 52, 255), width=3)
    d.arc([x, y - s, x + s, y + s], 200, 340, fill=(40, 28, 52, 255), width=3)

# --- title block: AERLUME big, tagline beneath ---
def text_center(y, text, font, fill, spacing=0):
    w = 0
    widths = []
    for ch in text:
        bbox = font.getbbox(ch)
        widths.append(bbox[2] - bbox[0] + spacing)
    w = sum(widths) - spacing
    x = (W - w) // 2
    for ch, cw in zip(text, widths):
        d.text((x, y), ch, font=font, fill=fill)
        x += cw

title_font = ImageFont.truetype(SERIF_B, 118)
# soft shadow for legibility
text_center(96, "AERLUME", title_font, (30, 18, 44, 255), spacing=10)
text_center(92, "AERLUME", title_font, (255, 240, 210, 255), spacing=10)
tag_font = ImageFont.truetype(SANS_B, 34)
text_center(232, "THE LIGHTHOUSE ABOVE THE CLOUDS", tag_font,
            (255, 222, 170, 255), spacing=6)

# --- bottom line ---
line_font = ImageFont.truetype(SANS, 26)
d.line([312, 972, 712, 972], fill=(255, 222, 170, 180), width=2)
text_center(984, "WHERE THE SKY KEEPS ITS LIGHT", line_font,
            (255, 232, 190, 230), spacing=4)

img.save("/home/hatch/workspace/makefun/poster-place-20261121-bot-v1/poster.png",
         optimize=True)
import os
print("saved", os.path.getsize(
    "/home/hatch/workspace/makefun/poster-place-20261121-bot-v1/poster.png"), "bytes")
