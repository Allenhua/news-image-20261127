#!/usr/bin/env python3
"""Draw entry.png for the 27 November 2026 world-news image (make.fun bounty
news-image-20261127). Flat vector-style newspaper front page, drawn with PIL.

Layout (1024x1024, written fresh for this day):
  header band -> one full-width LEAD story -> 2x2 grid of second stories
  -> a dark bottom strip carrying two more short stories.
Every story carries its own source label, body copy is dark ink on white
for contrast, headlines are set large. Drawn with DejaVu fonts already on
the VM; no network, no AI generation, no randomness, so repeated runs give
identical bytes."""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (13, 27, 48)
NAVY2 = (22, 45, 76)
GOLD = (206, 154, 20)
GOLD_LT = (232, 196, 90)
WHITE = (255, 255, 255)
INK = (17, 24, 36)
MUTED = (52, 64, 82)
LIGHT = (236, 241, 247)
LINE = (198, 206, 216)
SKY = (198, 214, 230)
ORANGE = (214, 84, 20)
RED = (172, 28, 28)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

# ---------- header ----------
d.rectangle([0, 0, W, 150], fill=NAVY)
d.rectangle([0, 150, W, 156], fill=GOLD)
d.text((28, 16), "WORLD NEWS  •  THE DAY IN PICTURES",
       font=font(FB, 24), fill=(148, 178, 212))
d.text((28, 46), "27 NOVEMBER 2026", font=font(FB, 66), fill=WHITE)
d.text((28, 118), "Friday — seven stories that defined the day",
       font=font(FR, 24), fill=(200, 214, 230))
d.ellipse([W - 122, 30, W - 38, 114], outline=GOLD, width=5)
d.text((W - 80, 56), "27", font=font(FB, 32), fill=GOLD, anchor="mm")
d.text((W - 80, 90), "NOV", font=font(FB, 19), fill=GOLD, anchor="mm")


def icon(draw, key, x, y, s, col):
    """Flat pictogram inside an s x s box at (x, y)."""
    if key == "drone":
        # quadcopter drone: body, four arms, four rotors
        cx, cy = x + s * 0.50, y + s * 0.52
        for ax, ay in ((0.16, 0.18), (0.84, 0.18), (0.16, 0.82), (0.84, 0.82)):
            draw.line([cx, cy, x + s * ax, y + s * ay], fill=NAVY2, width=6)
            draw.ellipse([x + s * (ax - 0.10), y + s * (ay - 0.10),
                          x + s * (ax + 0.10), y + s * (ay + 0.10)],
                         outline=NAVY2, width=4)
            draw.line([x + s * (ax - 0.13), y + s * ay,
                       x + s * (ax + 0.13), y + s * ay], fill=NAVY2, width=4)
        draw.rounded_rectangle([cx - s * 0.20, cy - s * 0.13,
                                cx + s * 0.20, cy + s * 0.13],
                               radius=8, fill=col)
        draw.ellipse([cx - s * 0.07, cy - s * 0.05,
                      cx + s * 0.07, cy + s * 0.05], fill=WHITE)
        draw.line([cx - s * 0.12, cy + s * 0.13, cx - s * 0.16, cy + s * 0.26],
                  fill=NAVY2, width=4)
        draw.line([cx + s * 0.12, cy + s * 0.13, cx + s * 0.16, cy + s * 0.26],
                  fill=NAVY2, width=4)
    elif key == "eu":
        # ring of twelve stars around a euro sign
        cx, cy, r = x + s * 0.50, y + s * 0.50, s * 0.34
        for i in range(12):
            a = math.pi * 2 * i / 12 - math.pi / 2
            px = cx + r * math.cos(a)
            py = cy + r * math.sin(a)
            draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=GOLD)
        draw.text((cx, cy), "€", font=font(FB, int(s * 0.42)),
                  fill=col, anchor="mm")
    elif key == "derrick":
        # oil derrick with a flame on top and a drop
        draw.line([x + s * 0.30, y + s * 0.90, x + s * 0.48, y + s * 0.22],
                  fill=NAVY2, width=9)
        draw.line([x + s * 0.70, y + s * 0.90, x + s * 0.52, y + s * 0.22],
                  fill=NAVY2, width=9)
        for yy in (0.40, 0.58, 0.76):
            draw.line([x + s * 0.36, y + s * yy, x + s * 0.64, y + s * yy],
                      fill=NAVY2, width=5)
        draw.polygon([(x + s * 0.44, y + s * 0.22), (x + s * 0.50, y + s * 0.06),
                      (x + s * 0.56, y + s * 0.22)], fill=col)
        draw.polygon([(x + s * 0.46, y + s * 0.20), (x + s * 0.50, y + s * 0.10),
                      (x + s * 0.54, y + s * 0.20)], fill=GOLD_LT)
        draw.ellipse([x + s * 0.78, y + s * 0.60, x + s * 0.94, y + s * 0.76],
                     fill=INK)
        draw.polygon([(x + s * 0.86, y + s * 0.44), (x + s * 0.78, y + s * 0.62),
                      (x + s * 0.94, y + s * 0.62)], fill=INK)
    elif key == "missile":
        # missile climbing, with exhaust flame
        draw.polygon([(x + s * 0.42, y + s * 0.12), (x + s * 0.58, y + s * 0.12),
                      (x + s * 0.62, y + s * 0.44), (x + s * 0.38, y + s * 0.44)],
                     fill=NAVY2)
        draw.polygon([(x + s * 0.42, y + s * 0.12), (x + s * 0.50, y + s * 0.02),
                      (x + s * 0.58, y + s * 0.12)], fill=col)
        draw.polygon([(x + s * 0.38, y + s * 0.44), (x + s * 0.30, y + s * 0.60),
                      (x + s * 0.42, y + s * 0.50)], fill=col)
        draw.polygon([(x + s * 0.62, y + s * 0.44), (x + s * 0.70, y + s * 0.60),
                      (x + s * 0.58, y + s * 0.50)], fill=col)
        draw.polygon([(x + s * 0.44, y + s * 0.60), (x + s * 0.50, y + s * 0.78),
                      (x + s * 0.56, y + s * 0.60)], fill=ORANGE)
    elif key == "ballot":
        # ballot box with a ballot paper and a tick
        draw.rectangle([x + s * 0.14, y + s * 0.52, x + s * 0.86, y + s * 0.90],
                       fill=NAVY2)
        draw.rectangle([x + s * 0.40, y + s * 0.46, x + s * 0.60, y + s * 0.54],
                       fill=WHITE)
        draw.polygon([(x + s * 0.30, y + s * 0.52), (x + s * 0.50, y + s * 0.12),
                      (x + s * 0.70, y + s * 0.52)], fill=WHITE,
                     outline=NAVY2)
        draw.line([x + s * 0.42, y + s * 0.36, x + s * 0.48, y + s * 0.44],
                  fill=col, width=6)
        draw.line([x + s * 0.48, y + s * 0.44, x + s * 0.60, y + s * 0.24],
                  fill=col, width=6)
        draw.text((x + s * 0.50, y + s * 0.72), "65", font=font(FB, int(s * 0.22)),
                  fill=WHITE, anchor="mm")
    elif key == "ruin":
        # damaged building with a jagged top and smoke
        draw.polygon([(x + s * 0.16, y + s * 0.88), (x + s * 0.16, y + s * 0.34),
                      (x + s * 0.30, y + s * 0.22), (x + s * 0.38, y + s * 0.36),
                      (x + s * 0.50, y + s * 0.20), (x + s * 0.62, y + s * 0.38),
                      (x + s * 0.74, y + s * 0.26), (x + s * 0.84, y + s * 0.34),
                      (x + s * 0.84, y + s * 0.88)], fill=NAVY2)
        for wy in (0.48, 0.64):
            for wx in (0.28, 0.52):
                draw.rectangle([x + s * wx, y + s * wy,
                                x + s * (wx + 0.10), y + s * (wy + 0.10)],
                               fill=GOLD_LT)
        for cx, cy, r in ((0.30, 0.12, 0.07), (0.48, 0.08, 0.09), (0.66, 0.13, 0.06)):
            draw.ellipse([x + s * (cx - r), y + s * (cy - r),
                          x + s * (cx + r), y + s * (cy + r)], fill=col)
    elif key == "chart":
        # rising market chart with an arrowhead
        draw.line([x + s * 0.14, y + s * 0.16, x + s * 0.14, y + s * 0.86],
                  fill=NAVY2, width=6)
        draw.line([x + s * 0.14, y + s * 0.86, x + s * 0.88, y + s * 0.86],
                  fill=NAVY2, width=6)
        draw.line([x + s * 0.18, y + s * 0.70, x + s * 0.38, y + s * 0.56,
                   x + s * 0.54, y + s * 0.62, x + s * 0.82, y + s * 0.28],
                  fill=col, width=7)
        draw.polygon([(x + s * 0.82, y + s * 0.28), (x + s * 0.66, y + s * 0.28),
                      (x + s * 0.82, y + s * 0.44)], fill=col)


# ---------- LEAD story, full width ----------
LX, LY, LW, LH = 24, 172, 976, 220
LEAD_COL = (172, 28, 28)
d.rounded_rectangle([LX, LY, LX + LW, LY + LH], radius=10, fill=WHITE,
                    outline=LINE, width=2)
d.rectangle([LX, LY, LX + LW, LY + 8], fill=LEAD_COL)
d.rectangle([LX + 16, LY + 20, LX + 296, LY + LH - 16], fill=LIGHT)
icon(d, "drone", LX + 16, LY + 20, 184, LEAD_COL)
tx = LX + 320
d.text((tx, LY + 22), "LEAD  •  KUWAIT — GULF",
       font=font(FB, 20), fill=LEAD_COL)
lead_head = wrap(d, "Drone attack in Kuwait kills two Italians",
                 font(FB, 34), LW - 320 - 20)
y = LY + 50
for ln in lead_head[:2]:
    d.text((tx, y), ln, font=font(FB, 34), fill=INK)
    y += 40
lead_body = wrap(
    d, "Two Rheinmetall Italia technicians die at an air-defence site; "
       "Kuwait blames Iranian drones. Tehran denies it.",
    font(FR, 22), LW - 320 - 20)
y += 4
for ln in lead_body[:3]:
    d.text((tx, y), ln, font=font(FR, 22), fill=MUTED)
    y += 27
d.text((tx, LY + LH - 26), "SOURCE: REUTERS",
       font=font(FB, 16), fill=(120, 96, 20))

# ---------- second stories, 2 x 2 grid ----------
cards = [
    ("EUROPEAN UNION", (22, 45, 76), "EU budget talks stall",
     "Leaders split over a €1.6tn budget and a €45bn Ukraine loan; "
     "Meloni: “light-years away”.",
     "eu", "SOURCE: REUTERS"),
    ("SAUDI ARABIA", (146, 90, 16), "Jazan refinery hit, one killed",
     "A projectile hits Aramco’s Jazan refinery; a Nepali worker dies, "
     "some operations halt.",
     "derrick", "SOURCE: REUTERS / AL JAZEERA"),
    ("UKRAINE", (122, 20, 20), "Missiles hit Kyiv, couple killed",
     "Missiles hit a Kyiv shopping centre, wounding 7; a drone kills a "
     "couple in Kharkiv.",
     "missile", "SOURCE: REUTERS"),
    ("NEW ZEALAND", (14, 110, 128), "Coalition one seat short",
     "The ruling coalition wins 65 of 130 seats; Luxon needs the "
     "Opportunity Party to govern.",
     "ballot", "SOURCE: REUTERS"),
]

MX, MY = 24, 408
GW, GH = 16, 16
CW = (W - 2 * MX - GW) // 2   # 480
CH = 212

for i, (tag, col, head, sub, key, src) in enumerate(cards):
    cx = MX + (i % 2) * (CW + GW)
    cy = MY + (i // 2) * (CH + GH)
    d.rounded_rectangle([cx, cy, cx + CW, cy + CH], radius=10, fill=WHITE,
                        outline=LINE, width=2)
    d.rectangle([cx, cy, cx + CW, cy + 8], fill=col)
    # icon panel, left
    d.rectangle([cx + 14, cy + 20, cx + 142, cy + 148], fill=LIGHT)
    icon(d, key, cx + 14, cy + 20, 128, col)
    # tag + headline + body + source
    tx = cx + 158
    d.text((tx, cy + 22), tag, font=font(FB, 19), fill=col)
    hl = wrap(d, head, font(FB, 28), CW - 158 - 14)
    y = cy + 48
    for ln in hl[:2]:
        d.text((tx, y), ln, font=font(FB, 28), fill=INK)
        y += 34
    sl = wrap(d, sub, font(FR, 18), CW - 158 - 14)
    y += 2
    for ln in sl[:3]:
        d.text((tx, y), ln, font=font(FR, 18), fill=MUTED)
        y += 22
    d.text((tx, cy + CH - 24), src, font=font(FB, 15), fill=col)

# ---------- bottom strip: two more short stories ----------
SY = 864
d.rectangle([0, SY, W, H], fill=NAVY)
d.rectangle([W // 2, SY + 14, W // 2, H - 14], fill=(38, 64, 100))

strip = [
    ("GAZA", "Nine killed in Gaza strikes",
     "Nine killed, including a Hamas-appointed minister, officials say.",
     "ruin", "SOURCE: REUTERS", (198, 60, 60)),
    ("MARKETS", "Shares steady, dollar climbs",
     "Shares steady after a bruising month; dollar up for a third month.",
     "chart", "SOURCE: REUTERS", (22, 120, 60)),
]

for i, (tag, head, sub, key, src, col) in enumerate(strip):
    bx = 28 + i * (W // 2)
    bw = W // 2 - 56
    d.rectangle([bx, SY + 18, bx + 92, SY + 110], fill=LIGHT)
    icon(d, key, bx, SY + 18, 92, col)
    tx = bx + 108
    d.text((tx, SY + 20), tag, font=font(FB, 17), fill=GOLD_LT)
    hl = wrap(d, head, font(FB, 25), bw - 108)
    y = SY + 44
    for ln in hl[:1]:
        d.text((tx, y), ln, font=font(FB, 25), fill=WHITE)
        y += 31
    sl = wrap(d, sub, font(FR, 18), bw - 108)
    for ln in sl[:2]:
        d.text((tx, y), ln, font=font(FR, 18), fill=SKY)
        y += 23
    d.text((tx, SY + 132), src, font=font(FB, 14), fill=GOLD_LT)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
