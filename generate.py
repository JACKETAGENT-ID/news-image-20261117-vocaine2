#!/usr/bin/env python3
"""Generate entry.png: a magazine front page summing up the world news of
Tuesday 17 November 2026. Deterministic: fixed palette, fixed layout, fixed
fonts, no timestamps, no randomness. Run: python3 generate.py
"""
import hashlib
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF_REG = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

PAPER = (247, 243, 234)
INK = (20, 33, 61)        # dark navy
RED = (166, 28, 28)
GREY = (90, 90, 88)
LINE = (20, 33, 61)
TEAL = (14, 90, 96)

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, width_px):
    """Greedy word wrap to a pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width_px:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def para(draw, x, y, text, fnt, fill, width_px, leading=None):
    """Draw wrapped paragraph; returns y after last line."""
    leading = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width_px):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y

def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)

# ---------------------------------------------------------------- stories
# Every item below was first reported on Tuesday 17 November 2026.
LEAD_HEAD = "UKRAINE STRIKES CRIMEA BRIDGE \u2014 SPAN PARTLY COLLAPSES"
LEAD_DECK = ("Kyiv says the missile-and-drone attack on the bridge linking Russia "
             "to occupied Crimea took weeks to plan. Moscow answers by hitting "
             "bridges in the capital.")

PANEL_A_HEAD = "GULF WAR WIDENS"
PANEL_A_DECK = ("US jets strike an Iranian missile site on Qeshm Island. Iran's "
                "drones hit a US radar in Bahrain, and tankers burn in the "
                "Strait of Hormuz.")

PANEL_B_HEAD = "US LOSES MEASLES-FREE STATUS"
PANEL_B_DECK = ("The WHO ends the US elimination designation after 26 years: "
                "5,400+ cases in 45 states, 10 deaths. RFK Jr. urges MMR shots.")

MOSAIC = [
    ("JAPAN SCRAMBLES JETS",
     "Two suspected Russian planes breach its airspace; Tokyo protests.",
     "sky"),
    ("MONGOLIA'S PRESIDENT QUITS",
     "Khurelsukh resigns as a corruption scandal closes in.",
     "hall"),
    ("FRANCE MARCHES: 146,000 OUT",
     "Unions strike over living costs; 28,000 rally in Paris.",
     "crowd"),
    ("OPENAI UNVEILS GPT-6.2",
     "Astra and Sol launch; flagship price cut by a fifth.",
     "chip"),
]

# (category, headline) — 32 items, read column by column, 4 columns x 8.
INDEX = [
    ("WAR", "Russia hits bridges in Kyiv in reply to the Crimea strike"),
    ("WAR", "Russian An-12 crashes in Siberia; all 19 aboard killed"),
    ("WAR", "Moldova shuts airspace after Russian drones cross border"),
    ("WAR", "Houthis push Yemen's army back from Red Sea coast"),
    ("MIDEAST", "Settlers kill woman, 72, near Jericho"),
    ("MIDEAST", "Kahana elected Knesset speaker in Eisenkot win"),
    ("MIDEAST", "West urges Israel to open Gaza crossings for aid"),
    ("POLITICS", "Mongolia's president resigns amid corruption scandal"),
    ("POLITICS", "Trump leaves Manila for first Xi-Putin three-way summit"),
    ("POLITICS", "Quad leaders reaffirm Indo-Pacific pact"),
    ("POLITICS", "US soldier held in Britain on spying suspicion"),
    ("POLITICS", "Pentagon fails its audit for the ninth year running"),
    ("POLITICS", "FEMA tests the US emergency alert system"),
    ("COURTS", "Depardieu admits sex assault charge in Paris"),
    ("TECH", "US tightens AI chip rules; Beijing vows response"),
    ("TECH", "Nvidia reports after the bell as chip shares rebound"),
    ("TECH", "US outages hit flights and banks; Trump plays it down"),
    ("TECH", "China tests a 250-mile electric plane"),
    ("TECH", "ESA's Hera probe surveys the asteroid crash site"),
    ("CLIMATE", "COP31: Turkiye and ITU launch AI climate pledge"),
    ("WEATHER", "Cyclone Akvan nears India's Andhra coast"),
    ("DISASTER", "Gas leak in Andhra Pradesh forces 800 people to flee"),
    ("DISASTER", "Fire on Thailand's Phuket island kills 11"),
    ("DISASTER", "17 killed in two mass shootings in South Africa"),
    ("DISASTER", "Serbian MiG-29 crashes; pilot killed"),
    ("DISASTER", "Three die in Grand Canyon plane crash"),
    ("CULTURE", "Anne Hathaway welcomes her third child"),
    ("SPORT", "Haaland's late penalty sends Norway through, 3-2"),
    ("SPORT", "Portugal edge Wales 3-2 to top their group"),
    ("SPORT", "Zverev beats Shelton to reach ATP Finals knockouts"),
    ("SPORT", "India beat Pakistan 2-1 to win SAFF final"),
    ("SPORT", "Mexico edge Jamaica 1-0 to reach semis"),
]

def draw_bridge(draw, x, y, w, h):
    """Flat dusk scene: strait, broken bridge, smoke, blast."""
    sky_top, sky_bot = (232, 126, 62), (58, 52, 96)
    for i in range(h):
        t = i / max(h - 1, 1)
        c = tuple(int(sky_top[k] + (sky_bot[k] - sky_top[k]) * t) for k in range(3))
        draw.line([(x, y + i), (x + w, y + i)], fill=c)
    # sun low on the horizon
    draw.ellipse([x + w - 118, y + h - 112, x + w - 58, y + h - 52],
                 fill=(244, 196, 96))
    # sea
    draw.rectangle([x, y + h - 52, x + w, y + h], fill=(24, 52, 88))
    for k in range(5):
        yy = y + h - 44 + k * 9
        draw.line([(x + 8 + (k % 2) * 30, yy), (x + w - 8 - (k % 2) * 30, yy)],
                  fill=(70, 110, 150), width=2)
    # bridge deck: left span, broken gap, right span
    deck_y = y + h - 108
    draw.rectangle([x + 8, deck_y, x + int(w * 0.44), deck_y + 10], fill=(28, 28, 34))
    draw.rectangle([x + int(w * 0.60), deck_y, x + w - 8, deck_y + 10],
                   fill=(28, 28, 34))
    # fallen span tilting into the sea
    draw.polygon([(x + int(w * 0.45), deck_y + 4),
                  (x + int(w * 0.58), deck_y + 26),
                  (x + int(w * 0.60), deck_y + 40),
                  (x + int(w * 0.47), deck_y + 18)], fill=(52, 52, 60))
    # towers
    for tx in (x + 70, x + w - 110):
        draw.rectangle([tx, deck_y - 62, tx + 12, deck_y], fill=(28, 28, 34))
        draw.rectangle([tx - 6, deck_y - 70, tx + 18, deck_y - 62],
                       fill=(28, 28, 34))
    # cables
    draw.line([(x + 76, deck_y - 62), (x + int(w * 0.44), deck_y)],
              fill=(120, 120, 128), width=2)
    draw.line([(x + w - 104, deck_y - 62), (x + int(w * 0.60), deck_y)],
              fill=(120, 120, 128), width=2)
    # blast starburst at the break
    bx, by = x + int(w * 0.52), deck_y - 6
    for ang in range(0, 360, 30):
        r = 34 if ang % 60 == 0 else 20
        ex = bx + int(r * math.cos(math.radians(ang)))
        ey = by + int(r * math.sin(math.radians(ang)))
        draw.line([(bx, by), (ex, ey)], fill=(255, 176, 32), width=5)
    draw.ellipse([bx - 16, by - 16, bx + 16, by + 16], fill=(255, 214, 90))
    # smoke plume, small puffs just above the blast (stay inside the art)
    for cx, cy, r in [(bx - 20, by - 26, 13), (bx + 4, by - 36, 15),
                      (bx + 26, by - 26, 11), (bx + 6, by - 46, 8)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(88, 84, 92))

def draw_mosaic_art(draw, kind, x, y, w, h):
    """Small flat pictogram for a mosaic panel."""
    if kind == "sky":  # jets scrambling under a red sun
        draw.rectangle([x, y, x + w, y + h], fill=(52, 96, 148))
        draw.ellipse([x + w - 62, y + 10, x + w - 14, y + 58], fill=(214, 48, 49))
        for jx, jy, s in [(x + 30, y + 62, 1.0), (x + 110, y + 36, 0.75)]:
            pts = [(jx, jy), (jx + int(64 * s), jy + int(10 * s)),
                   (jx + int(52 * s), jy + int(20 * s)),
                   (jx + int(20 * s), jy + int(18 * s))]
            draw.polygon(pts, fill=(240, 240, 235))
            draw.polygon([(jx + int(52 * s), jy + int(20 * s)),
                          (jx + int(64 * s), jy + int(10 * s)),
                          (jx + int(70 * s), jy + int(26 * s))],
                         fill=(200, 200, 195))
        for cx in range(x + 8, x + w - 8, 26):
            draw.line([(cx, y + h - 12), (cx + 14, y + h - 12)],
                      fill=(255, 255, 255), width=2)
    elif kind == "hall":  # parliament steps, columns, dome
        draw.rectangle([x, y, x + w, y + h], fill=(122, 28, 28))
        draw.rectangle([x + 14, y + h - 16, x + w - 14, y + h - 8],
                       fill=(232, 222, 200))
        draw.rectangle([x + 28, y + h - 30, x + w - 28, y + h - 16],
                       fill=(232, 222, 200))
        for k in range(5):
            cx = x + 52 + k * 36
            draw.rectangle([cx, y + 44, cx + 12, y + h - 30],
                           fill=(232, 222, 200))
        draw.rectangle([x + 40, y + 36, x + w - 40, y + 46],
                       fill=(232, 222, 200))
        draw.pieslice([x + w // 2 - 26, y + 2, x + w // 2 + 26, y + 54],
                      180, 360, fill=(232, 222, 200))
        draw.rectangle([x + w // 2 - 3, y - 2, x + w // 2 + 3, y + 8],
                       fill=(244, 196, 96))
    elif kind == "crowd":  # protest crowd with placards
        draw.rectangle([x, y, x + w, y + h], fill=(26, 54, 96))
        for r, yy in enumerate((y + 24, y + 46, y + 66)):
            for k in range(6 - r):
                cx = x + 24 + k * 38 + (r % 2) * 14
                draw.ellipse([cx, yy, cx + 15, yy + 15], fill=(240, 222, 190))
                draw.rectangle([cx - 3, yy + 15, cx + 18,
                                min(yy + 25, y + h - 4)],
                               fill=(200 - r * 30, 60 + r * 10, 60 + r * 14))
        draw.rectangle([x + 26, y + 8, x + 96, y + 26], fill=(244, 196, 96))
        draw.rectangle([x + 150, y + 8, x + 214, y + 26], fill=(255, 255, 255))
    else:  # chip: dark board, gold chip, circuit traces
        draw.rectangle([x, y, x + w, y + h], fill=(18, 22, 30))
        for ty in (y + 18, y + h - 18):
            draw.line([(x + 10, ty), (x + w - 10, ty)], fill=(90, 160, 140),
                      width=2)
        for tx in (x + 16, x + w - 16):
            draw.line([(tx, y + 10), (tx, y + h - 10)], fill=(90, 160, 140),
                      width=2)
        cx0, cy0 = x + w // 2 - 42, y + h // 2 - 42
        draw.rectangle([cx0, cy0, cx0 + 84, cy0 + 84], fill=(176, 124, 24))
        draw.rectangle([cx0 + 14, cy0 + 14, cx0 + 70, cy0 + 70],
                       fill=(20, 33, 61))
        for k in range(4):
            draw.line([(cx0 - 12, cy0 + 16 + k * 18),
                       (cx0, cy0 + 16 + k * 18)], fill=(176, 124, 24), width=3)
            draw.line([(cx0 + 84, cy0 + 16 + k * 18),
                       (cx0 + 96, cy0 + 16 + k * 18)], fill=(176, 124, 24),
                      width=3)
        draw.text((cx0 + 42, cy0 + 42), "6.2", font=font(SANS_B, 26),
                  fill=(255, 255, 255), anchor="mm")

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer double border
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=1)

    # ---- masthead (positions measured from the real glyph boxes) ----
    f_kick = font(SANS_B, 13)
    kick = "O N E   D A Y  \u00b7  O N E   W O R L D  \u00b7  E V E R Y   S T O R Y   T H A T   M A T T E R E D"
    d.text((W // 2, 22), kick, font=f_kick, fill=GREY, anchor="ma")
    f_title = font(SERIF, 58)
    title = "THE DAY IN FULL"
    d.text((W // 2, 54), title, font=f_title, fill=INK, anchor="mt")
    tb = d.textbbox((W // 2, 54), title, font=f_title, anchor="mt")
    band_y = tb[3] + 12
    d.rectangle([22, band_y, W - 22, band_y + 34], fill=RED)
    f_date = font(SANS_B, 24)
    d.text((W // 2, band_y + 17), "TUESDAY, 17 NOVEMBER 2026", font=f_date,
           fill=(255, 255, 255), anchor="mm")

    # ---- lead story (left) + right column ----
    top = band_y + 44
    lx, lw = 22, 596
    draw_bridge(d, lx, top, lw, 168)
    f_lead = font(SERIF, 26)
    y = para(d, lx, top + 176, LEAD_HEAD, f_lead, INK, lw, leading=31)
    rule(d, lx, y + 4, lx + lw, width=2, fill=RED)
    f_deck = font(SANS, 14)
    deck_end = para(d, lx, y + 12, LEAD_DECK, f_deck, (40, 40, 40), lw,
                    leading=18)

    rx, rw = 634, 368
    for ptop, head, deck, accent in (
            (top, PANEL_A_HEAD, PANEL_A_DECK, RED),
            (top + 140, PANEL_B_HEAD, PANEL_B_DECK, TEAL)):
        d.rectangle([rx, ptop, rx + rw, ptop + 132], outline=INK, width=2)
        d.rectangle([rx, ptop, rx + rw, ptop + 34], fill=accent)
        f_ph = font(SANS_B, 16)
        d.text((rx + 12, ptop + 17), head, font=f_ph, fill=(255, 255, 255),
               anchor="lm")
        para(d, rx + 12, ptop + 44, deck, font(SANS, 14), (40, 40, 40),
             rw - 24, leading=19)

    # ---- mosaic strip: four photo panels ----
    my = deck_end + 14
    rule(d, 22, my - 8, W - 22, width=2)
    pw, gap = 236, 8
    mosaic_end = my
    for i, (head, deck, kind) in enumerate(MOSAIC):
        px = 22 + i * (pw + gap)
        draw_mosaic_art(d, kind, px, my, pw, 88)
        d.rectangle([px, my, px + pw, my + 88], outline=INK, width=1)
        f_mh = font(SANS_B, 15)
        yy = para(d, px, my + 96, head, f_mh, INK, pw, leading=18)
        yy = para(d, px, yy + 2, deck, font(SANS, 12), (60, 60, 60), pw,
                  leading=14)
        mosaic_end = max(mosaic_end, yy)

    # ---- index: the day in 32 headlines, 4 columns x 8 ----
    iy = mosaic_end + 12
    f_idx_h = font(SERIF, 21)
    d.text((22, iy), "THE DAY IN 32 HEADLINES", font=f_idx_h, fill=INK)
    d.text((W - 22, iy + 4), "numbered for the record",
           font=font(SANS, 12), fill=GREY, anchor="ra")
    rule(d, 22, iy + 28, W - 22, width=2)
    col_w, col_x = 236, (22, 264, 506, 748)
    f_num = font(SANS_B, 12)
    f_cat = font(SANS_B, 11)
    f_item = font(SANS, 12)
    rows_end = iy + 40
    for col in range(4):
        for row in range(8):
            n = col * 8 + row
            cat, head = INDEX[n]
            x = col_x[col]
            yy = iy + 40 + row * 32
            d.text((x, yy), "%02d" % (n + 1), font=f_num, fill=RED)
            # category inline as a prefix, then the headline over 2 lines:
            # line 1 shares its width with the prefix, line 2 uses it all.
            prefix = cat + " \u2014 "
            pw = d.textlength(prefix, font=f_cat)
            tx = x + 28
            w1, w2 = col_w - 28 - pw - 4, col_w - 28
            l1 = wrap(d, head, f_item, w1)
            first, rest = l1[0], " ".join(l1[1:])
            second = wrap(d, rest, f_item, w2)
            if len(second) > 1:  # headline too long: trim with ellipsis
                second = [second[0][:-3].rstrip() + "\u2026"]
            d.text((tx, yy), prefix, font=f_cat, fill=GREY)
            d.text((tx + pw + 4, yy), first, font=f_item, fill=(30, 30, 30))
            if second:
                d.text((tx, yy + 14), second[0], font=f_item,
                       fill=(30, 30, 30))
            rows_end = max(rows_end, yy + 28)

    # ---- footer ----
    rule(d, 22, rows_end + 10, W - 22, width=1, fill=GREY)
    f_foot = font(SERIF_REG, 13)
    d.text((W // 2, rows_end + 26),
           "Every story above was first reported on Tuesday 17 November 2026.",
           font=f_foot, fill=GREY, anchor="mm")
    return img

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    img = build()
    img.save(out, format="PNG", optimize=True)
    data = open(out, "rb").read()
    print("entry.png: %d bytes, %s, sha256 %s"
          % (len(data), img.size, hashlib.sha256(data).hexdigest()))

if __name__ == "__main__":
    main()
