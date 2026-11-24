#!/usr/bin/env python3
"""Render the news-image-20261124 entry: a one-page newspaper front page
summing up Tuesday 24 November 2026. Drawn from scratch with PIL.

Stories (all verified as 24 Nov 2026 news):
  HERO  - South Korea scrambles jets as Russian planes enter the KADIZ
  GRID  - Nvidia reinstates Jensen Huang; Megaspeed blacklisted
  GRID  - Zelenskyy urges four-party peace talks "as soon as possible"
  GRID  - Leaked Rosstat data: Russia's war dead past 700,000
  STRIP - Zelenskyy quote + ALSO TODAY nuggets
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
RED = (176, 32, 32)
NAVY = (26, 48, 92)
SKY = (186, 214, 235)
SEA = (32, 68, 110)
GREY = (96, 93, 84)
LIGHT_RED = (214, 110, 110)
SUN = (250, 226, 140)
ISLAND = (52, 96, 66)
JET = (58, 58, 62)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(SANS, size)


def wrap(d, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, max_w, text, fnt, fill=INK, leading=None):
    if leading is None:
        leading = fnt.size + 6
    for line in wrap(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centre(d, y, text, fnt, fill=INK):
    w = d.textlength(text, font=fnt)
    d.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + 6


def rule(d, y, x0=28, x1=996, width=2):
    d.rectangle([x0, y, x1, y + width - 1], fill=INK)


def jet(d, cx, cy, s, color=JET):
    # Simple top-view fighter jet: fuselage + swept wings + tail.
    d.polygon([(cx, cy - 26 * s), (cx + 5 * s, cy + 6 * s),
               (cx, cy + 2 * s), (cx - 5 * s, cy + 6 * s)], fill=color)
    d.polygon([(cx - 4 * s, cy - 2 * s), (cx - 26 * s, cy + 14 * s),
               (cx - 4 * s, cy + 10 * s)], fill=color)
    d.polygon([(cx + 4 * s, cy - 2 * s), (cx + 26 * s, cy + 14 * s),
               (cx + 4 * s, cy + 10 * s)], fill=color)
    d.polygon([(cx - 3 * s, cy + 8 * s), (cx - 10 * s, cy + 20 * s),
               (cx - 3 * s, cy + 16 * s)], fill=color)
    d.polygon([(cx + 3 * s, cy + 8 * s), (cx + 10 * s, cy + 20 * s),
               (cx + 3 * s, cy + 16 * s)], fill=color)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Frame
    d.rectangle([14, 14, 1010, 1010], outline=INK, width=2)
    d.rectangle([20, 20, 1004, 1004], outline=INK, width=1)

    # Masthead
    f_mast = F(SERIF_B, 54)
    centre(d, 32, "THE WORLD IN ONE IMAGE", f_mast)

    # Dateline row
    f_date = F(SANS_B, 18)
    d.text((28, 102), "TUESDAY, 24 NOVEMBER 2026", font=f_date, fill=INK)
    right = "ONE DAY — ONE PAGE"
    d.text((996 - d.textlength(right, font=f_date), 102), right,
           font=f_date, fill=INK)

    # Double rule under masthead
    d.rectangle([28, 132, 996, 136], fill=INK)
    d.rectangle([28, 140, 996, 141], fill=INK)

    # ---------- HERO ----------
    hx0, hx1, hy0, hy1 = 28, 996, 152, 560
    tx1 = 566  # text column ends here
    ix0 = 580  # illustration starts here

    d.text((40, 164), "KOREA — AIR DEFENCE", font=F(SANS_B, 19), fill=RED)
    y = para(d, 40, 196, tx1 - 40,
             "JETS SCRAMBLED AS RUSSIAN PLANES NEAR ULLEUNG",
             F(SERIF_B, 40), leading=46)
    y = para(d, 40, y + 8, tx1 - 40,
             "Seoul sends fighters up after several Russian warplanes "
             "enter the air-defence zone over the East Sea — islanders "
             "are told to shelter, then stood down three minutes later.",
             F(SERIF, 20), leading=26)
    para(d, 40, y + 10, tx1 - 40,
         "The alert sounded on Ulleung Island at 7:52 a.m. Seoul says "
         "there was no violation of its airspace. The Defence Ministry "
         "will summon Russia's defence attaché to protest. It was the "
         "second such scramble in eight days — Russian planes entered "
         "the zone last Monday too.",
         F(SANS, 17), leading=22)

    # Vertical divider between text and illustration
    d.line([(572, 164), (572, 548)], fill=GREY, width=1)

    # Illustration: East Sea, Ulleung Island, jets, radar arcs
    d.rectangle([ix0, hy0, hx1, 428], fill=SKY)
    d.ellipse([918, 172, 964, 218], fill=SUN)
    d.ellipse([620, 190, 700, 214], fill=(255, 255, 255))
    d.ellipse([680, 210, 760, 230], fill=(255, 255, 255))
    # Radar arcs, centred off the right edge
    for r in (60, 95, 130):
        d.ellipse([880 - r, 300 - r, 880 + r, 300 + r],
                  outline=LIGHT_RED, width=2)
    # Red dashed flight path
    for x in range(600, 960, 28):
        d.line([(x, 300), (x + 16, 292)], fill=RED, width=3)
    # Jets with contrails
    d.line([(640, 260), (700, 252)], fill=(255, 255, 255), width=3)
    jet(d, 716, 250, 1.0)
    d.line([(800, 330), (860, 322)], fill=(255, 255, 255), width=3)
    jet(d, 876, 320, 0.85)
    # Sea + island
    d.rectangle([ix0, 428, hx1, hy1], fill=SEA)
    d.polygon([(620, 470), (690, 408), (770, 470)], fill=ISLAND)
    d.polygon([(760, 470), (820, 430), (880, 470)], fill=(44, 82, 56))
    d.line([(600, 492), (980, 492)], fill=(255, 255, 255), width=1)
    d.line([(640, 516), (760, 516)], fill=(255, 255, 255), width=1)
    d.text((592, 528), "ULLEUNG ISLAND  •  EAST SEA",
           font=F(SANS_B, 14), fill=(255, 255, 255))
    # Red tag on the illustration
    d.rectangle([ix0, hy0, 748, hy0 + 26], fill=RED)
    d.text((ix0 + 10, hy0 + 4), "AIR DEFENCE ZONE",
           font=F(SANS_B, 14), fill=(255, 255, 255))

    rule(d, 574)

    # ---------- GRID: three stories ----------
    cols = [(28, 336), (360, 668), (692, 996)]
    stories = [
        ("TECH — WALL STREET", "HUANG IS BACK",
         "Nvidia's board unanimously reinstated Jensen Huang as chief "
         "executive, 11 days after he resigned. Trump says he talked "
         "the board round. Shares leapt 31.5% — a record $952bn in a "
         "day. The US blacklisted Megaspeed and six linked firms."),
        ("UKRAINE — PEACE TALKS", "TALKS 'AS SOON AS POSSIBLE'",
         "Volodymyr Zelenskyy urged a four-party meeting — Ukraine, "
         "Russia, the US and Europe — 'as soon as possible', saying "
         "Kyiv is ready 'literally tomorrow'. Partners aim to meet "
         "before Christmas. He also warned of fresh Russian strikes."),
        ("RUSSIA — THE HUMAN COST", "THE 700,000 DEAD",
         "Leaked Rosstat records put Russia's war dead far higher than "
         "admitted. Meduza and Mediazona count about 490,000 registered "
         "military deaths — and estimate the true toll past 700,000, "
         "one in every 200 Russians. Total casualties may top two million."),
    ]
    for (x0, x1), (kicker, head, body) in zip(cols, stories):
        w = x1 - x0
        d.text((x0, 588), kicker, font=F(SANS_B, 15), fill=RED)
        y = para(d, x0, 612, w, head, F(SERIF_B, 25), leading=29)
        para(d, x0, y + 6, w, body, F(SANS, 15), leading=20)
    # Column dividers
    d.line([(348, 588), (348, 824)], fill=GREY, width=1)
    d.line([(680, 588), (680, 824)], fill=GREY, width=1)

    rule(d, 838)

    # ---------- QUOTE STRIP ----------
    centre(d, 850,
           "\u201cWe are ready to do this. Literally tomorrow.\u201d",
           F(SERIF_I, 21))
    centre(d, 882,
           "— Volodymyr Zelenskyy, urging four-party peace talks",
           F(SANS, 14), fill=GREY)

    rule(d, 912)

    # ---------- ALSO TODAY ----------
    d.text((28, 924), "ALSO TODAY", font=F(SANS_B, 15), fill=RED)
    also = [
        "Seoul to summon Russia's defence attaché over the KADIZ entry.",
        "Huang walks back into Nvidia HQ to applause from staff.",
        "Zelenskyy repeats Kyiv's plea to join NATO.",
        "Megaspeed and six affiliates added to the US Entity List.",
    ]
    ax = [28, 272, 516, 760]
    aw = [228, 228, 228, 236]
    for x, wdt, item in zip(ax, aw, also):
        para(d, x, 940, wdt, item, F(SANS, 14), leading=18)

    # Sources line
    centre(d, 978,
           "Sources: Reuters  •  AP  •  France 24  •  Meduza / Mediazona  •  "
           "Financial Times  —  Tuesday 24 November 2026",
           F(SANS, 12), fill=GREY)

    img.save(OUT, "PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
