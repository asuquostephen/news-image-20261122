#!/usr/bin/env python3
"""Draw entry.png: one picture that sums up the world news of
Sunday 22 November 2026, for the make.fun news-image-20261122 bounty.

The picture is a broadsheet front page: a masthead naming the day, one
lead story in a wide panel, and six story cards beneath it. Every story
is an event of, or first reported on, 22 November 2026 (researched from
AFP, AP and Reuters wire copy and the day's news digests on the morning
of 22 Nov, WAT). The layout is height-budgeted: each text block is
wrapped against real font measurements and shrunk until it fits its
box, so nothing spills over an edge.

Run with a Python that has Pillow installed; it writes entry.png beside
this file. The grader never runs this program (only main.py); it is kept
in the repository so the picture's making is fully reproducible.
"""

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas
W = H = 1024
MARGIN = 44
INK = (13, 22, 38)          # deep navy page
PANEL = (21, 34, 56)        # card background
PANEL_LEAD = (27, 43, 68)   # lead panel background
GOLD = (216, 178, 92)       # rules and kickers
PAPER = (238, 234, 222)     # headline text
SOFT = (196, 203, 214)      # caption text
FAINT = (140, 152, 170)     # footer text

FONT_DIR = "/usr/share/fonts/truetype/liberation"
SERIF_BOLD = f"{FONT_DIR}/LiberationSerif-Bold.ttf"
SERIF = f"{FONT_DIR}/LiberationSerif-Regular.ttf"
SANS_BOLD = f"{FONT_DIR}/LiberationSans-Bold.ttf"
SANS = f"{FONT_DIR}/LiberationSans-Regular.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_width: int) -> list[str]:
    """Greedy word wrap measured with the real font."""
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = word if not current else f"{current} {word}"
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_block(draw, text, path, start_size, max_width, max_lines, min_size=13):
    """Wrap text at shrinking sizes until it fits max_lines.

    Returns (font, lines). If even the minimum size overflows, the last
    line is trimmed with an ellipsis so the block can never spill.
    """
    size = start_size
    while size > min_size:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_width)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    fnt = font(path, min_size)
    lines = wrap(draw, text, fnt, max_width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and draw.textlength(last + "…", font=fnt) > max_width:
            last = last.rsplit(" ", 1)[0]
        lines[-1] = last + "…"
    return fnt, lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- stories
# (kicker, headline, caption) — facts as reported on 22 Nov 2026.
LEAD = (
    "CONFLICT · BAHRAIN AND THE GULF",
    "Iran strikes Bahrain again — and tankers are hit in Hormuz",
    "Bahrain said an Iranian strike set a civilian industrial plant ablaze on "
    "Sitra Island, with no casualties; Iran's Guards said they attacked US "
    "bases. Britain's UKMTO said two tankers were struck by projectiles in "
    "the Strait of Hormuz, and Iran said one tanker hit a naval mine.",
)

CARDS = [
    (
        "WAR · KRYVYI RIH, UKRAINE",
        "'Triple-tap' strike kills two in Zelenskyy's hometown",
        "Russian missiles hit a restaurant car park in Kryvyi Rih, then more "
        "rockets struck the rescuers who responded. A boy of seven and a "
        "paramedic of 20 were killed, and 60 people were wounded.",
    ),
    (
        "AMERICAS · GUASAVE, MEXICO",
        "Mexico captures FBI most-wanted cartel boss",
        "Elite troops seized Fausto Isidro Meza Flores — 'El Chapo Isidro', on "
        "the FBI's 10 most wanted list — in Sinaloa. The firefight killed four "
        "soldiers and seven gunmen and emptied a baseball stadium.",
    ),
    (
        "POLITICS · JERUSALEM",
        "Opposition leader invites Netanyahu's party to talks",
        "Gadi Eisenkot's centrist Yashar party invited the caretaker prime "
        "minister's Likud to 'marathon' coalition talks — a surprise twist in "
        "Israel's long political deadlock.",
    ),
    (
        "EUROPE · PARIS",
        "France's Saturday protests draw smaller crowds",
        "Turnout fell at the sixth straight Saturday of cost-of-living "
        "marches: the Interior Ministry counted 82,500 people nationwide, "
        "down on a week earlier, in largely peaceful protests.",
    ),
    (
        "DISASTER · JUNÍN, PERU",
        "6.7 quake shakes Peru's Andes — no deaths",
        "A magnitude 6.7 earthquake 30 km northwest of Junín, 129 km deep, "
        "brought minor damage, power cuts and landslides but no reported "
        "fatalities; the tremor sent Lima residents into the streets.",
    ),
    (
        "SPORT · DUBLIN",
        "Ireland stun world champions South Africa 20–17",
        "Two tries from Rob Baloucoune and one from Rónan Kelleher gave "
        "Ireland a famous Nations Championship win in Dublin — though a "
        "losing bonus point still sent the Springboks into the final.",
    ),
]


# ---------------------------------------------------------------- layout
def main() -> None:
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    inner_w = W - 2 * MARGIN
    footer_rule_y = H - 54

    # Masthead
    y = 28
    d.text((MARGIN, y), "THE DAY IN ONE PICTURE · A MAKE.FUN NEWS IMAGE",
           font=font(SANS_BOLD, 20), fill=GOLD)
    y += 28
    d.text((MARGIN, y), "WORLD NEWS", font=font(SERIF_BOLD, 76), fill=PAPER)
    y += 88
    d.rectangle([MARGIN, y, W - MARGIN, y + 3], fill=GOLD)
    y += 11
    d.text((MARGIN, y), "SUNDAY · 22 NOVEMBER 2026", font=font(SANS_BOLD, 28), fill=PAPER)
    dateline = "The world's news of one day, in one image"
    dl_fnt = font(SERIF, 21)
    d.text((W - MARGIN - d.textlength(dateline, font=dl_fnt), y + 3),
           dateline, font=dl_fnt, fill=FAINT)
    y += 38

    # Lead panel (height budgeted: pad 14 + kicker 26 + headline 2×46
    # + gap 5 + caption 3×24 + pad 12 = 221)
    lead_h = 221
    d.rectangle([MARGIN, y, W - MARGIN, y + lead_h], fill=PANEL_LEAD, outline=GOLD, width=2)
    pad = 24
    ly = y + 14
    d.text((MARGIN + pad, ly), LEAD[0], font=font(SANS_BOLD, 19), fill=GOLD)
    ly += 28
    hf, hl = fit_block(d, LEAD[1], SERIF_BOLD, 42, inner_w - 2 * pad, 2, min_size=30)
    ly = draw_lines(d, hl, MARGIN + pad, ly, hf, PAPER, 46)
    ly += 5
    cf, cl = fit_block(d, LEAD[2], SANS, 19, inner_w - 2 * pad, 3, min_size=15)
    draw_lines(d, cl, MARGIN + pad, ly, cf, SOFT, 24)
    y += lead_h + 12

    # Story cards: two columns, three rows, filling down to the footer rule
    gap = 12
    card_w = (inner_w - gap) // 2
    card_h = (footer_rule_y - 10 - y - 2 * gap) // 3
    for i, (kick, head, cap) in enumerate(CARDS):
        cx = MARGIN + (i % 2) * (card_w + gap)
        cy = y + (i // 2) * (card_h + gap)
        d.rectangle([cx, cy, cx + card_w, cy + card_h], fill=PANEL)
        d.rectangle([cx, cy, cx + 5, cy + card_h], fill=GOLD)
        tx = cx + 20
        tw = card_w - 36
        ty = cy + 12
        d.text((tx, ty), kick, font=font(SANS_BOLD, 15), fill=GOLD)
        ty += 22
        hf, hl = fit_block(d, head, SANS_BOLD, 24, tw, 2, min_size=19)
        ty = draw_lines(d, hl, tx, ty, hf, PAPER, 28)
        ty += 2
        cap_lines = max(1, (cy + card_h - 8 - ty) // 23)
        cf, cl = fit_block(d, cap, SANS, 17, tw, cap_lines, min_size=13)
        draw_lines(d, cl, tx, ty, cf, SOFT, 23)

    # Footer
    d.rectangle([MARGIN, footer_rule_y, W - MARGIN, footer_rule_y + 2], fill=(52, 68, 92))
    footer = "Sources: AFP · Associated Press · Reuters · Al Jazeera — drawn by an AI agent, 22 Nov 2026"
    ff = font(SANS, 16)
    d.text(((W - d.textlength(footer, font=ff)) / 2, footer_rule_y + 12),
           footer, font=ff, fill=FAINT)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
