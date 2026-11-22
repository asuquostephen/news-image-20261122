#!/usr/bin/env python3
"""Draw entry.png — the world news of Sunday 22 November 2026 as one
broadsheet front page, for the make.fun news-image-20261122 bounty.

Design: a light-paper broadsheet. A centred masthead, the day's lead
story set full width under a red kicker, then six stories in two
ruled columns. The page is laid out from the content itself: every
block is measured first, column rows grow to fit their tallest cell,
and if the page would overrun, the caption size steps down and the
whole sheet is measured again until it fits.

Stories are the events of, or first reported on, 22 November 2026,
researched that morning (WAT) from AFP, AP and Reuters wire copy.

Only main.py is run by the grader; this program is kept in the repo so
the picture can be reproduced exactly. It needs Pillow and the
Liberation fonts.
"""

from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
EDGE = 48
WIDTH = PAGE - 2 * EDGE
PAPER = (246, 243, 236)
INK = (22, 22, 24)
RED = (163, 32, 36)
GREY = (104, 104, 108)
HAIRLINE = (178, 172, 160)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


@dataclass
class Story:
    kicker: str
    headline: str
    body: str


LEAD = Story(
    "CONFLICT · BAHRAIN AND THE GULF",
    "Iran strikes Bahrain again — and tankers are hit in Hormuz",
    "Bahrain said an Iranian strike set a civilian industrial plant ablaze "
    "on Sitra Island, with no casualties; Iran's Revolutionary Guards said "
    "they attacked US bases. Britain's UKMTO said two tankers were struck "
    "by projectiles in the Strait of Hormuz, and Iran said one tanker hit "
    "a naval mine.",
)

STORIES = [
    Story(
        "WAR · KRYVYI RIH, UKRAINE",
        "'Triple-tap' strike kills two in Zelenskyy's hometown",
        "Russian missiles hit a restaurant car park in Kryvyi Rih, then "
        "more rockets struck the rescuers who responded. A boy of seven "
        "and a paramedic of 20 were killed, and 60 people were wounded.",
    ),
    Story(
        "AMERICAS · GUASAVE, MEXICO",
        "Mexico captures FBI most-wanted cartel boss",
        "Elite troops seized Fausto Isidro Meza Flores — 'El Chapo "
        "Isidro', on the FBI's 10 most wanted list — in Sinaloa. The "
        "firefight killed four soldiers and seven gunmen and emptied a "
        "baseball stadium.",
    ),
    Story(
        "POLITICS · JERUSALEM",
        "Opposition leader invites Netanyahu's party to talks",
        "Gadi Eisenkot's centrist Yashar party invited the caretaker "
        "prime minister's Likud to 'marathon' coalition talks — a "
        "surprise twist in Israel's long political deadlock.",
    ),
    Story(
        "EUROPE · PARIS",
        "France's Saturday protests draw smaller crowds",
        "Turnout fell at the sixth straight Saturday of cost-of-living "
        "marches: the Interior Ministry counted 82,500 people "
        "nationwide, down on a week earlier, in largely peaceful "
        "protests.",
    ),
    Story(
        "DISASTER · JUNÍN, PERU",
        "6.7 quake shakes Peru's Andes — no deaths",
        "A magnitude 6.7 earthquake 30 km northwest of Junín, 129 km "
        "deep, brought minor damage, power cuts and landslides but no "
        "reported fatalities; the tremor sent Lima residents into the "
        "streets.",
    ),
    Story(
        "SPORT · DUBLIN",
        "Ireland stun world champions South Africa 20–17",
        "Two tries from Rob Baloucoune and one from Rónan Kelleher gave "
        "Ireland a famous Nations Championship win in Dublin — though a "
        "losing bonus point still sent the Springboks into the final.",
    ),
]


def load(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def text_w(draw: ImageDraw.ImageDraw, s: str, fnt) -> float:
    return draw.textlength(s, font=fnt)


def break_lines(draw, text: str, fnt, width: int) -> list[str]:
    """Split text into lines of at most `width` pixels.

    Each line takes the longest run of whole words that fits, found by
    binary search over the word list rather than by trial appending.
    """
    words = text.split()
    lines: list[str] = []
    i = 0
    while i < len(words):
        lo, hi = i + 1, len(words)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if text_w(draw, " ".join(words[i:mid]), fnt) <= width:
                lo = mid
            else:
                hi = mid - 1
        lines.append(" ".join(words[i:lo]))
        i = lo
    return lines


def choose(draw, text: str, path: str, sizes, width: int, max_lines: int):
    """First size in `sizes` whose wrapping fits `max_lines` lines.

    Falls back to the smallest size with the overflow cut short.
    """
    for size in sizes:
        fnt = load(path, size)
        lines = break_lines(draw, text, fnt, width)
        if len(lines) <= max_lines:
            return fnt, lines
    fnt = load(path, sizes[-1])
    lines = break_lines(draw, text, fnt, width)[:max_lines]
    tail = lines[-1]
    while tail and text_w(draw, tail + "…", fnt) > width:
        tail = tail.rsplit(" ", 1)[0]
    lines[-1] = tail + "…"
    return fnt, lines


def block_h(lines: int, leading: int) -> int:
    return lines * leading


def measure_sheet(draw, caption_size: int):
    """Measure the whole page at one caption size.

    Returns (plan, total_height): plan holds the wrapped blocks, and
    total_height is what the sheet needs below the masthead.
    """
    cap = load(SANS, caption_size)
    cap_lead = caption_size + 6

    lead_head_f, lead_head = choose(draw, LEAD.headline, SERIF,
                                    (46, 42, 38, 34), WIDTH, 2)
    lead_body = break_lines(draw, LEAD.body, cap, WIDTH)
    lead_h = 26 + block_h(len(lead_head), 50) + 8 + block_h(len(lead_body), cap_lead)

    col_w = (WIDTH - 30) // 2
    cells = []
    for story in STORIES:
        hf, hl = choose(draw, story.headline, SANS_B, (24, 22, 20), col_w, 2)
        bl = break_lines(draw, story.body, cap, col_w)
        cells.append((story, hf, hl, bl))
    rows = []
    for r in range(3):
        pair = cells[2 * r:2 * r + 2]
        h = max(20 + block_h(len(hl), 27) + 4 + block_h(len(bl), cap_lead)
                for _, _, hl, bl in pair)
        rows.append((pair, h))
    grid_h = sum(h for _, h in rows) + 2 * 18
    return (lead_head_f, lead_head, lead_body, rows), lead_h + 16 + grid_h


def centred(draw, y: int, s: str, fnt, fill) -> int:
    draw.text(((PAGE - text_w(draw, s, fnt)) / 2, y), s, font=fnt, fill=fill)
    return y + fnt.size + 8


def render() -> None:
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- masthead -------------------------------------------------
    y = 30
    y = centred(draw, y, "THE DAY IN ONE PICTURE · A MAKE.FUN NEWS IMAGE",
                load(SANS_B, 19), RED)
    y = centred(draw, y, "WORLD NEWS", load(SERIF, 88), INK)
    draw.rectangle([EDGE, y, PAGE - EDGE, y + 5], fill=INK)
    y += 12
    y = centred(draw, y, "SUNDAY · 22 NOVEMBER 2026", load(SANS_B, 27), INK)
    draw.rectangle([EDGE, y, PAGE - EDGE, y + 2], fill=INK)
    y += 20

    # ---- measure, stepping the caption size down until it fits ----
    footer_top = PAGE - 52
    caption_size = 18
    while True:
        plan, needed = measure_sheet(draw, caption_size)
        if y + needed <= footer_top - 8 or caption_size <= 13:
            break
        caption_size -= 1
    lead_head_f, lead_head, lead_body, rows = plan
    cap = load(SANS, caption_size)
    cap_lead = caption_size + 6
    kick_f = load(SANS_B, 17)

    # ---- lead story -----------------------------------------------
    draw.text((EDGE, y), LEAD.kicker, font=kick_f, fill=RED)
    y += 26
    for line in lead_head:
        draw.text((EDGE, y), line, font=lead_head_f, fill=INK)
        y += 50
    y += 8
    for line in lead_body:
        draw.text((EDGE, y), line, font=cap, fill=(52, 52, 56))
        y += cap_lead
    y += 16

    # ---- story grid -------------------------------------------------
    col_w = (WIDTH - 30) // 2
    for r, (pair, row_h) in enumerate(rows):
        if r:
            draw.line([EDGE, y - 9, PAGE - EDGE, y - 9], fill=HAIRLINE, width=1)
        for c, (story, hf, hl, bl) in enumerate(pair):
            x = EDGE + c * (col_w + 30)
            if c:
                draw.line([x - 15, y, x - 15, y + row_h - 6],
                          fill=HAIRLINE, width=1)
            cy = y
            draw.text((x, cy), story.kicker, font=load(SANS_B, 14), fill=RED)
            cy += 20
            for line in hl:
                draw.text((x, cy), line, font=hf, fill=INK)
                cy += 27
            cy += 4
            for line in bl:
                draw.text((x, cy), line, font=cap, fill=(52, 52, 56))
                cy += cap_lead
        y += row_h + 18

    # ---- footer -----------------------------------------------------
    draw.rectangle([EDGE, footer_top, PAGE - EDGE, footer_top + 2], fill=INK)
    centred(draw, footer_top + 12,
            "Sources: AFP · Associated Press · Reuters · Al Jazeera — drawn by an AI agent, 22 Nov 2026",
            load(SANS, 15), GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size, "caption size", caption_size)


if __name__ == "__main__":
    render()
