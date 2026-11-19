#!/usr/bin/env python3
"""Render the entry image for make.fun news-image-20261119.

Format: NEWSPAPER FRONT PAGE. A black masthead names the day; one big
hero panel (GTA VI, the day's biggest story) sits top-left with two
stacked panels top-right (APEC trilateral, Anthropic IPO); three panels
run along the bottom (Cyclone Akvan, India–Japan 2+2, Voyager 1). Each
panel has a coloured kicker strip, a picture, a short bold headline and
a one-line deck, so a viewer who missed the day can tell what happened
from the pictures and short labels alone. A bottom band carries the
also-today items, the dated statement and the sources.

Pictures: four panels use AI-generated illustrations (art/*.jpg, cropped
to their exact boxes when the renderer first ran); the India–Japan and
Voyager panels are drawn with PIL primitives. All text is exact vector
text — no garbled text anywhere.

All facts come from NEWS_FACTS.md (verified reporting, 19 Nov 2026).
The trilateral, the Anthropic debut, the 2+2 dialogue and the Voyager
briefing are events scheduled on Thursday 19 Nov; the deck says so where
it matters. Nothing is claimed for a day it did not happen on.

Deterministic: same input files always render byte-identical output.
The renderer writes entry.png as PNG; if the PNG is over the 1 MiB
cap it writes JPEG bytes instead (the competition allows either in a
file still named entry.png).
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
WHITE = (255, 255, 255)
GREY = (70, 70, 70)
GOLD = (242, 201, 76)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "art")
MAX_BYTES = 1_048_576


def load(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def crop_to(src_path, box_w, box_h, focus=0.5):
    """Centre-ish crop of an image to the box aspect, then resize.

    focus 0 takes the top band, 1 the bottom band, 0.5 the middle.
    """
    im = Image.open(src_path).convert("RGB")
    sw, sh = im.size
    target = box_w / box_h
    if sw / sh > target:
        # Too wide: cut the sides, keep full height.
        cw = int(sh * target)
        x0 = (sw - cw) // 2
        im = im.crop((x0, 0, x0 + cw, sh))
    else:
        # Too tall: cut a horizontal band.
        ch = int(sw / target)
        y0 = int((sh - ch) * focus)
        im = im.crop((0, y0, sw, y0 + ch))
    return im.resize((box_w, box_h), Image.LANCZOS)


def photo_panel(img, draw, x, y, pw, ph, kicker, colour, pic, pic_h,
                head_size, deck_size, headline, deck, deck_lines=2):
    """Panel with a photographic picture (already cropped to size)."""
    draw.rectangle([x, y, x + pw, y + ph], fill=WHITE, outline=INK, width=2)
    kh = 40 if ph > 300 else (30 if ph > 220 else 34)
    draw.rectangle([x + 2, y + 2, x + pw - 2, y + kh], fill=colour)
    kf = load(SANS_B, 20 if ph > 300 else 18)
    draw.text((x + 12, y + 9 if ph > 300 else y + 6), kicker, font=kf,
              fill=WHITE)
    img.paste(pic, (x + 2, y + kh + 2))
    hy = y + kh + 2 + pic_h + 8
    hf = load(SERIF_B, head_size)
    for ln in wrap_text(draw, headline, hf, pw - 24)[:2]:
        draw.text((x + 12, hy), ln, font=hf, fill=INK)
        hy += head_size + 6
    df = load(SANS_R, deck_size)
    dy = hy + 4
    for ln in wrap_text(draw, deck, df, pw - 24)[:deck_lines]:
        draw.text((x + 12, dy), ln, font=df, fill=(51, 51, 51))
        dy += deck_size + 5


def draw_panel(img, draw, x, y, pw, ph, kicker, colour, tint, art,
               pic_h, head_size, deck_size, headline, deck):
    """Panel with a PIL-drawn picture on a tinted background."""
    draw.rectangle([x, y, x + pw, y + ph], fill=WHITE, outline=INK, width=2)
    draw.rectangle([x + 2, y + 2, x + pw - 2, y + 36], fill=colour)
    kf = load(SANS_B, 18)
    draw.text((x + 12, y + 7), kicker, font=kf, fill=WHITE)
    draw.rectangle([x + 2, y + 38, x + pw - 2, y + 38 + pic_h], fill=tint)
    art(draw, x, y, pw, pic_h)
    hy = y + 38 + pic_h + 8
    hf = load(SERIF_B, head_size)
    for ln in wrap_text(draw, headline, hf, pw - 24)[:2]:
        draw.text((x + 12, hy), ln, font=hf, fill=INK)
        hy += head_size + 6
    df = load(SANS_R, deck_size)
    dy = hy + 4
    for ln in wrap_text(draw, deck, df, pw - 24)[:2]:
        draw.text((x + 12, dy), ln, font=df, fill=(51, 51, 51))
        dy += deck_size + 5


# ---- PIL-drawn pictures. Each draws inside its panel's picture area:
# panel origin (x, y); picture spans x+2..x+pw-2, y+38..y+38+pic_h.

def art_india_japan(draw, x, y, pw, pic_h):
    """Indian and Japanese flags on poles above a red torii gate."""
    # Sky: pale blue already tinted; draw a soft sun.
    draw.ellipse([x + pw - 70, y + 52, x + pw - 30, y + 92],
                 fill=(242, 201, 76), outline=INK, width=2)
    # Flag poles.
    for fx in (x + 58, x + 232):
        draw.line([fx, y + 58, fx, y + 118], fill=INK, width=3)
    # India flag: saffron / white / green with a navy wheel.
    ix = x + 58
    draw.rectangle([ix, y + 58, ix + 52, y + 70], fill=(255, 153, 51))
    draw.rectangle([ix, y + 70, ix + 52, y + 82], fill=WHITE, outline=INK,
                   width=1)
    draw.rectangle([ix, y + 82, ix + 52, y + 94], fill=(19, 136, 8))
    draw.ellipse([ix + 20, y + 70, ix + 32, y + 82], outline=(0, 0, 128),
                 width=2)
    # Japan flag: white with a red disc.
    jx = x + 232
    draw.rectangle([jx, y + 58, jx + 52, y + 94], fill=WHITE, outline=INK,
                   width=1)
    draw.ellipse([jx + 16, y + 66, jx + 36, y + 86], fill=(188, 0, 45))
    # Torii gate, bottom centre.
    gx = x + pw // 2
    gy = y + 38 + pic_h
    draw.rectangle([gx - 78, gy - 58, gx + 78, gy - 46], fill=(188, 0, 45),
                   outline=INK, width=2)
    draw.rectangle([gx - 62, gy - 40, gx + 62, gy - 30], fill=(188, 0, 45),
                   outline=INK, width=2)
    draw.rectangle([gx - 56, gy - 58, gx - 44, gy - 2], fill=(188, 0, 45),
                   outline=INK, width=2)
    draw.rectangle([gx + 44, gy - 58, gx + 56, gy - 2], fill=(188, 0, 45),
                   outline=INK, width=2)


def art_voyager(draw, x, y, pw, pic_h):
    """Voyager probe with its big dish, stars, and a small Earth."""
    for sx, sy in ((x + 36, y + 56), (x + 290, y + 58), (x + 60, y + 170),
                   (x + 296, y + 162), (x + 150, y + 48), (x + 250, y + 148)):
        draw.ellipse([sx, sy, sx + 5, sy + 5], fill=WHITE)
    # Earth, bottom left.
    ex, ey = x + 52, y + 38 + pic_h - 44
    draw.ellipse([ex, ey, ex + 40, ey + 40], fill=(0, 91, 187), outline=INK,
                 width=2)
    draw.ellipse([ex + 8, ey + 10, ex + 22, ey + 18], fill=(46, 125, 50))
    draw.ellipse([ex + 20, ey + 24, ex + 32, ey + 32], fill=(46, 125, 50))
    # Probe body and dish, centre right.
    px, py = x + 210, y + 122
    draw.polygon([(px - 52, py - 30), (px - 46, py - 2), (px, py + 14),
                  (px + 46, py - 2), (px + 52, py - 30)],
                 fill=(220, 220, 220), outline=INK, width=2)
    draw.rectangle([px - 26, py + 14, px + 26, py + 34], fill=(180, 180, 190),
                   outline=INK, width=2)
    draw.line([px - 34, py + 34, px - 52, py + 58], fill=INK, width=3)
    draw.line([px + 34, py + 34, px + 52, py + 58], fill=INK, width=3)
    # Signal rays from the dish up to the stars.
    for ang in (-70, -45, -20):
        ex2 = px + 70 * math.cos(math.radians(ang - 90))
        ey2 = py - 30 + 70 * math.sin(math.radians(ang - 90))
        draw.line([px, py - 30, ex2, ey2], fill=GOLD, width=3)


def prepare_art():
    """Crop the four AI illustrations to their exact panel boxes and
    save them as small JPEGs under art/ (reproducible, repo-sized)."""
    jobs = [
        ("gta-vice-city.jpg", "media-generation-gta-vice-city-0-4e9fcfb8-"
         "0cdc-4df0-86df-f2c0f2264f12.png", 500, 250, 0.45),
        ("apec.jpg", "media-generation-apec-shenzhen-0-70563ded-cf5c-4bbf-"
         "95aa-f1a701f70a1c.png", 500, 112, 0.30),
        ("anthropic.jpg", "media-generation-anthropic-ipo-0-f03faa03-6092-"
         "4388-8b2a-5450850c56c5.png", 500, 112, 0.62),
        ("cyclone.jpg", "media-generation-cyclone-akvan-0-4f3ba89d-45b6-"
         "467d-93f4-d1eed8734566.png", 322, 150, 0.35),
    ]
    src_dir = os.path.join(os.path.dirname(HERE), "art")
    for name, src, bw, bh, focus in jobs:
        out = os.path.join(ART, name)
        if os.path.isfile(out):
            continue
        crop_to(os.path.join(src_dir, src), bw, bh, focus).save(
            out, format="JPEG", quality=90)


def render():
    prepare_art()
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    # Masthead: title + date.
    draw.rectangle([0, 0, W, 88], fill=INK)
    tf = load(SERIF_B, 44)
    title = "THE WORLD IN ONE DAY"
    draw.text(((W - draw.textlength(title, font=tf)) / 2, 8), title,
              font=tf, fill=WHITE)
    df = load(SANS_B, 22)
    date = "THURSDAY 19 NOVEMBER 2026"
    draw.text(((W - draw.textlength(date, font=df)) / 2, 56), date,
              font=df, fill=GOLD)

    # Hero: GTA VI, top-left.
    hero = Image.open(os.path.join(ART, "gta-vice-city.jpg"))
    photo_panel(img, draw, 8, 96, 500, 464, "CULTURE — VICE CITY",
                (140, 30, 90), hero, 250, 38, 20,
                "GTA VI goes live as gamers enter Vice City",
                "Rolls out at midnight market by market — PS5 and Xbox, "
                "$79.99. Pre-orders near 16m copies, over $1.5bn.")
    # Top-right stacked panels.
    apec = Image.open(os.path.join(ART, "apec.jpg"))
    photo_panel(img, draw, 516, 96, 500, 228, "DIPLOMACY — SHENZHEN",
                (0, 51, 153), apec, 112, 26, 18,
                "Trump, Xi and Putin meet in Shenzhen",
                "Nuclear arms top the agenda; no deals expected.",
                deck_lines=1)
    anth = Image.open(os.path.join(ART, "anthropic.jpg"))
    photo_panel(img, draw, 516, 332, 500, 228, "MARKETS — AI",
                (34, 120, 60), anth, 112, 26, 18,
                "Anthropic debuts on Nasdaq as ANT",
                "Priced at $83, above its $70–$78 range.",
                deck_lines=1)
    # Bottom row.
    cyc = Image.open(os.path.join(ART, "cyclone.jpg"))
    photo_panel(img, draw, 16, 568, 322, 336, "WEATHER — INDIA",
                (0, 91, 140), cyc, 150, 27, 18,
                "Cyclone Akvan bears down on India's coast",
                "Red alerts and schools shut; landfall due Friday at "
                "90–100 km/h.")
    draw_panel(img, draw, 351, 568, 322, 336, "DIPLOMACY — TOKYO",
               (120, 60, 10), (226, 236, 213), art_india_japan, 150, 27, 18,
               "India and Japan hold 2+2 defence talks",
               "Singh and Jaishankar meet Koizumi and Motegi in Tokyo.")
    draw_panel(img, draw, 686, 568, 322, 336, "SPACE",
               (20, 20, 43), (25, 25, 48), art_voyager, 150, 27, 18,
               "NASA briefs on Voyager 1's light-day mark",
               "Noon-EST talk, a day after the probe passed 16bn miles.")
    # Bottom band.
    draw.line([16, 912, 1008, 912], fill=INK, width=3)
    af = load(SANS_B, 18)
    also = ("ALSO TODAY:  Trump–Xi bilateral on AI chips and rare earths  ·  "
            "Tokenised ANT shares go live on IPO day  ·  Trump plans to "
            "raise the Iran war at the talks")
    ay = 920
    for ln in wrap_text(draw, also, af, 992):
        draw.text((16, ay), ln, font=af, fill=INK)
        ay += 24
    sf = load(SERIF_I, 17)
    stmt = ("Every story above happened, was first reported, or is "
            "scheduled on Thursday 19 November 2026.")
    draw.text(((W - draw.textlength(stmt, font=sf)) / 2, 972), stmt,
              font=sf, fill=GREY)
    srcf = load(SANS_R, 14)
    src = ("Sources: Reuters · AP · NASA · IMD · TechCrunch · Press "
           "Information Bureau")
    draw.text(((W - draw.textlength(src, font=srcf)) / 2, 998), src,
              font=srcf, fill=GREY)
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    image = render()
    image.save(out, format="PNG", optimize=True)
    if os.path.getsize(out) > MAX_BYTES:
        image.save(out, format="JPEG", quality=88)
        print("PNG over 1 MiB; wrote JPEG bytes as", out)
    print("wrote", out, os.path.getsize(out), "bytes")
