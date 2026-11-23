#!/usr/bin/env python3
"""frontpage.py -- draws the v2 front page for news-image-20261122.

Design brief (learned from the winning entries of the 17/18/19 Nov
editions of this same bounty): a real newspaper front page, not a
poster. One lead, a row of secondary stories, then dense regional
briefs -- every item a real story of Sunday 22 November 2026 with its
source named on the page.

The engine is a measuring packer:

  1. every story is wrapped and measured with the real fonts first;
  2. briefs are flowed into three columns in section order, a section
     header always travelling with the brief that follows it;
  3. if the columns overflow the page, the lowest-priority briefs are
     shed one at a time and the layout is re-measured, so the page
     always fits and never clips;
  4. only then is anything drawn, and the story count printed in the
     strap line is the number of stories that actually made the page,
     so the claim on the image is true by construction.

Deterministic: same data, same fonts, same bytes. Needs Pillow.
"""

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
MARGIN = 26
WIDTH = PAGE - 2 * MARGIN
PAPER = (247, 242, 231)
INK = (26, 23, 18)
FAINT = (74, 68, 58)
ACCENT = (163, 22, 33)
RULE = (120, 112, 98)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_KICKER = font(SANSB, 14)
F_TITLE = font(SERIF, 47)
F_STRAP = font(SANSB, 14)
F_LEAD_KICK = font(SANSB, 13)
F_LEAD_HEAD = font(SERIF, 26)
F_LEAD_DEK = font(SANS, 13)
F_SEC_HEAD = font(SANSB, 15)
F_SEC_DEK = font(SANS, 12)
F_BRIEF_HEAD = font(SANSB, 13)
F_BRIEF_DEK = font(SANS, 11)
F_MARKETS = font(SANSB, 12)
F_FOOT = font(SANS, 11)

_probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def wrap(text, fnt, width):
    """Greedy word wrap against real glyph widths."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if _probe.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block_height(lines, line_h, gap_after):
    return len(lines) * line_h + gap_after


# ---------------------------------------------------------------- stories
# Every story below was reported on Sunday 22 November 2026; the source
# named in each dek is the outlet (or outlets) that reported it that day.

LEAD = {
    "kicker": "CONFLICT · BAHRAIN AND THE GULF",
    "head": "Iran strikes Bahrain again — and tankers are hit in Hormuz",
    "dek": (
        "Bahrain said an Iranian strike set a civilian industrial plant ablaze on Sitra "
        "Island, with no casualties; Iran's Revolutionary Guards said they attacked US "
        "bases. Britain's UKMTO said two tankers were struck by projectiles in the Strait "
        "of Hormuz, and Tehran said one tanker hit a naval mine. (AFP · Al Jazeera)"
    ),
}

SECOND = [
    {
        "head": "Climate talks collapse in Turkey with no deal",
        "dek": (
            "Nearly 200 countries ended COP31 in Antalya without an overarching agreement, "
            "after the EU and others rejected a final text that never mentioned fossil fuels. (SCMP · AP)"
        ),
    },
    {
        "head": "Sea drones strike a Russian warship in Libya",
        "dek": (
            "Libyan officials said suspected Ukrainian maritime drones hit the corvette "
            "Merkury at Benghazi naval base — the Ukraine war reaching a North African port. (SCMP)"
        ),
    },
    {
        "head": "Russian strikes kill at least 14 near Kyiv",
        "dek": (
            "Strikes on the Kyiv region killed at least 14 people, and Zelenskiy said 14 more "
            "were missing after a drone hit a residential building. (Business Recorder · SCMP)"
        ),
    },
    {
        "head": "Democrats clinch biggest House majority since 1992",
        "dek": (
            "A North Carolina recount took Democrats to at least 258 House seats, their "
            "largest majority in three decades. (Seven Lights)"
        ),
    },
]

# (section name, [(headline, dek, drop_rank), ...]) -- higher drop_rank sheds first.
SECTIONS = [
    ("MIDDLE EAST", [
        ("Eisenkot opens talks with Netanyahu's Likud",
         "Tasked with forming Israel's next government, Eisenkot invited Likud to "
         "'marathon' talks. (AP)", 30),
        ("Israel investigates West Bank fire claims",
         "Israeli authorities opened an inquiry into fires in Palestinian communities "
         "that residents blamed on settler attacks. (SCMP)", 31),
        ("Trump dares Iran to test the Hormuz blockade",
         "'They'll all be at the bottom of the sea,' Trump told Fox News, as 14 Iranian "
         "tankers gathered near Kharg Island. (Breitbart)", 32),
        ("Saudi-led coalition intercepts Houthi missile",
         "The coalition said it downed a ballistic missile launched toward the kingdom's "
         "western Red Sea region. (WION)", 33),
    ]),
    ("EUROPE", [
        ("France's sixth Saturday of protests draws 82,500",
         "Cost-of-living marches stayed largely peaceful but shrank; the Interior "
         "Ministry counted 82,500 people nationwide. (Reuters)", 20),
        ("French officers jailed for racist beating",
         "Paris officers who beat music producer Michel Zecler and tear-gassed him "
         "without cause were sent to prison. (SCMP)", 21),
        ("Russian cargo ship ablaze in Baltic drone strike",
         "The crew evacuated as the ship caught fire; Finland said Russia was towing "
         "it clear. (Business Recorder)", 22),
        ("UK and EU sign trade and travel deals",
         "London and Brussels pledged to rebuild ties after Brexit in a package of "
         "trade and travel agreements. (AP)", 23),
        ("EU and Indonesia sign 'ambitious' trade deal",
         "Brussels and Jakarta formally signed the long-negotiated pact on Sunday. "
         "(Business Recorder)", 24),
    ]),
    ("AFRICA", [
        ("Bayelsa boat toll hits 29; Tinubu gives \u20a6250m",
         "The president donated \u20a6250m to families of the Southern Ijaw boat victims "
         "and ordered stricter waterway safety. (Punch)", 10),
        ("Army rescues 18 of 22 abducted Kaduna children",
         "Troops freed 18 children in the Kachia\u2013Kajuru area and kept hunting for "
         "four still missing. (LAS News)", 11),
        ("Bandits threaten to stop 2027 elections in Zamfara",
         "Armed leaders told Anka communities no vote will hold and imposed a \u20a650m "
         "levy, a security monitor reported. (Punch)", 12),
        ("ASUU mobilises for a nationwide strike",
         "Lecturers began branch votes on an indefinite shutdown over 3.5 months of "
         "withheld 2022 salaries. (The Matrix)", 13),
        ("Nigeria opens 40 oil blocks to bidders",
         "The upstream regulator NUPRC launched the round as Nigeria pushes to meet "
         "its OPEC output quota. (The Matrix)", 14),
        ("Ex-SA deputy president dies at 71",
         "Phumzile Mlambo-Ngcuka also led UN Women for eight years. (AP)", 15),
    ]),
    ("ASIA-PACIFIC", [
        ("Indonesia factory fire: 24 dead, about 30 missing",
         "Rescuers searched the ruins of a candy factory as families waited for news "
         "of the missing workers. (PiQ · AP)", 40),
        ("Tainted alcohol kills 11 in India; 180 in hospital",
         "Illicit liquor poisoned drinkers in one of the year's deadliest hooch "
         "tragedies. (Business Recorder)", 41),
        ("Seoul readies fund after Kospi's 5.21% fall",
         "Finance minister Lee Hyoung-il announced a stock-market stabilisation fund "
         "after Friday's plunge. (Korea JoongAng Daily)", 42),
        ("Taiwan bans short sales of falling stocks",
         "The blanket curb, the regulator's first since 2015, takes effect Monday. "
         "(Focus Taiwan)", 43),
        ("Japan Tobacco faces a record \u00a5724bn loss",
         "Losing control of its Russian subsidiaries — a quarter of operating profit "
         "— drove the forecast record net loss. (Jiji)", 44),
        ("Japan wins a 25% bigger large-bluefin tuna quota",
         "An international panel raised Japan's 2027\u201328 quota for big Pacific "
         "bluefin while trimming the small-fish quota by 6%. (Jiji)", 45),
        ("Vietnam ends death penalty for drug trafficking",
         "The change removes capital punishment for drug offences from the penal "
         "code. (SCMP)", 46),
        ("Nepal's PM in India for talks with Modi",
         "Balendra Shah's two-day state visit puts energy and connectivity at the top "
         "of Monday's bilateral talks. (WION)", 47),
    ]),
    ("AMERICAS", [
        ("Mexico captures FBI most-wanted cartel boss",
         "Troops seized Fausto Isidro Meza Flores, 'El Chapo Isidro', in Sinaloa; the "
         "firefight killed 11 in all. (AP)", 50),
        ("ICE arrests at Seattle airport spark protests",
         "Washington's governor and unions denounced the detention of travellers "
         "caught on video. (Business Recorder)", 51),
        ("Baby-shower shooting kills three in US",
         "A gunman opened fire at the family gathering, killing three people and "
         "wounding another. (SCMP)", 52),
        ("Bessent warns the Fed against overtightening",
         "The Treasury secretary told CBS a policy mistake looms; Nvidia still owes "
         "answers on chip sales to China. (CBS)", 53),
        ("Trump offers 10% credit-card rate cap",
         "The president said he would work with the incoming Congress on the cap "
         "banks have long resisted. (Monochrome Chronicles)", 54),
        ("FBI probes a reported hack of its crime database",
         "The bureau is investigating a claimed breach of the National Crime "
         "Information Center. (OneTurn)", 55),
        ("6.7 earthquake shakes Peru's Andes; no deaths",
         "The quake, 30 km northwest of Jun\u00edn, brought minor damage, power cuts "
         "and landslides but no fatalities. (USGS)", 56),
    ]),
    ("SCIENCE & TECH", [
        ("CRISPR therapy cuts bad cholesterol by 52%",
         "The single gene-editing treatment points to a possible one-shot defence "
         "against heart disease. (OneTurn)", 60),
        ("Man swims Hormuz strait for the environment",
         "A British swimmer crossed the strait to highlight the environmental damage "
         "of the tanker war. (Dawn)", 61),
    ]),
    ("SPORT", [
        ("Liverpool rout 10-man United 4\u20130 at Anfield",
         "Yoro's 8th-minute red card opened the floodgates: Szoboszlai, Wirtz, "
         "Ngumoha, Mu\u00f1oz. (Reuters)", 70),
        ("Ireland stun world champions South Africa 20\u201317",
         "Baloucoune's two tries and one from Kelleher gave Ireland a famous Dublin "
         "win; the Boks still reached the final. (Reuters)", 71),
        ("Arsenal held 2\u20132 by Newcastle",
         "The league leaders dropped points at home in a four-goal draw. (Reports)", 72),
    ]),
]

MARKETS = (
    "MARKETS · BITCOIN \u2248 $60,800 (+1%) · NASDAQ FUTURES +3% AFTER A 10% WEEKLY LOSS "
    "· S&P 500 IN CORRECTION · NAIRA \u20a61,440/$ PARALLEL"
)


# ---------------------------------------------------------------- layout

def brief_block(head, dek, col_w):
    hl = wrap(head, F_BRIEF_HEAD, col_w)
    dl = wrap(dek, F_BRIEF_DEK, col_w)
    h = block_height(hl, 15, 0) + block_height(dl, 12.5, 5)
    return (hl, dl), h


def section_header(name):
    return name, 24  # text line + rule + breathing room


def pack_briefs(col_w, col_top, col_bottom):
    """Flow sections into 3 columns; shed low-priority briefs until it fits.

    The brief sequence (section headers interleaved) is split into three
    contiguous column runs by a small partition search that minimises the
    tallest column -- so almost no vertical space is wasted at column
    breaks. A run that starts mid-section pays for a "(CONT.)" header.
    Returns (columns, placed_count); columns hold draw items.
    """
    budget = col_bottom - col_top
    flat = []
    for name, items in SECTIONS:
        for head, dek, rank in items:
            flat.append((rank, name, head, dek))
    alive = sorted(flat)
    while True:
        by_section = {}
        for rank, name, head, dek in alive:
            by_section.setdefault(name, []).append((head, dek))
        # Ordered item list: ("header", name, 22) / ("brief", hl, dl, h).
        items = []
        for name, _ in SECTIONS:
            if name not in by_section:
                continue
            items.append(("header", name, 20))
            for head, dek in by_section[name]:
                (hl, dl), h = brief_block(head, dek, col_w)
                items.append(("brief", name, hl, dl, h))
        n = len(items)
        if n == 0:
            return [[], [], []], 0
        heights = [it[2] if it[0] == "header" else it[4] for it in items]
        prefix = [0]
        for h in heights:
            prefix.append(prefix[-1] + h)

        def run_cost(i, j):
            cost = prefix[j] - prefix[i]
            if items[i][0] == "brief":  # column starts mid-section
                cost += 20
            return cost

        # Partition into 3 contiguous runs minimising the tallest run.
        INF = float("inf")
        best = [[INF] * (n + 1) for _ in range(4)]
        cut = [[None] * (n + 1) for _ in range(4)]
        best[0][0] = 0
        for k in range(1, 4):
            for j in range(1, n + 1):
                for i in range(j):
                    if best[k - 1][i] == INF:
                        continue
                    cand = max(best[k - 1][i], run_cost(i, j))
                    if cand < best[k][j]:
                        best[k][j] = cand
                        cut[k][j] = i
        if best[3][n] <= budget:
            runs, j, k = [], n, 3
            while k:
                i = cut[k][j]
                runs.append((i, j))
                j, k = i, k - 1
            runs.reverse()
            columns = []
            for i, j in runs:
                col_items = []
                if items[i][0] == "brief":
                    col_items.append(("cont", items[i][1]))
                for it in items[i:j]:
                    if it[0] == "header":
                        col_items.append(("header", it[1]))
                    else:
                        col_items.append(("brief", it[2], it[3]))
                columns.append(col_items)
            return columns, len(alive)
        alive = alive[:-1]  # shed the single lowest-priority brief, re-measure
        if not alive:
            return [[], [], []], 0


def build():
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    dr = ImageDraw.Draw(img)
    x0, x1 = MARGIN, PAGE - MARGIN
    y = 18

    # Masthead (story count is filled after packing, but its line is fixed).
    dr.text((PAGE / 2, y), "THE DAY IN ONE PICTURE · A MAKE.FUN NEWS IMAGE",
            font=F_KICKER, fill=ACCENT, anchor="ma")
    y += 22
    dr.text((PAGE / 2, y), "THE WORLD IN ONE PAGE", font=F_TITLE, fill=INK, anchor="ma")
    y += 55
    dr.line([(x0, y), (x1, y)], fill=INK, width=4)
    y += 7
    dr.line([(x0, y), (x1, y)], fill=INK, width=1)
    y += 10
    strap_y = y
    y += 20

    # Lead.
    dr.text((x0, y), LEAD["kicker"], font=F_LEAD_KICK, fill=ACCENT)
    y += 19
    for ln in wrap(LEAD["head"], F_LEAD_HEAD, WIDTH):
        dr.text((x0, y), ln, font=F_LEAD_HEAD, fill=INK)
        y += 29
    y += 2
    for ln in wrap(LEAD["dek"], F_LEAD_DEK, WIDTH):
        dr.text((x0, y), ln, font=F_LEAD_DEK, fill=FAINT)
        y += 15
    y += 10
    dr.line([(x0, y), (x1, y)], fill=RULE, width=1)
    y += 7

    # Second tier: 2 x 2 grid with a centre rule.
    gap = 22
    cell_w = (WIDTH - gap) // 2
    cells = []
    for s in SECOND:
        hl = wrap(s["head"], F_SEC_HEAD, cell_w)
        dl = wrap(s["dek"], F_SEC_DEK, cell_w)
        cells.append((hl, dl, block_height(hl, 18, 2) + block_height(dl, 13.5, 0)))
    row_h = [max(cells[0][2], cells[1][2]), max(cells[2][2], cells[3][2])]
    for r in range(2):
        for c in range(2):
            hl, dl, _ = cells[r * 2 + c]
            cx = x0 + c * (cell_w + gap)
            cy = y
            for ln in hl:
                dr.text((cx, cy), ln, font=F_SEC_HEAD, fill=INK)
                cy += 18
            cy += 2
            for ln in dl:
                dr.text((cx, cy), ln, font=F_SEC_DEK, fill=FAINT)
                cy += 13.5
        y += row_h[r] + 8
    dr.line([(PAGE / 2, y - row_h[0] - row_h[1] - 20), (PAGE / 2, y - 10)], fill=RULE, width=1)
    dr.line([(x0, y), (x1, y)], fill=RULE, width=1)
    y += 6

    # Markets strip.
    dr.text((PAGE / 2, y), MARKETS, font=F_MARKETS, fill=INK, anchor="ma")
    y += 16
    dr.line([(x0, y), (x1, y)], fill=INK, width=2)
    y += 10

    # Briefs in three columns.
    foot_h = 26
    col_gap = 18
    col_w = (WIDTH - 2 * col_gap) // 3
    columns, placed = pack_briefs(col_w, y, PAGE - foot_h - 8)
    total = 1 + len(SECOND) + placed
    for ci, items in enumerate(columns):
        cx = x0 + ci * (col_w + col_gap)
        cy = y
        for item in items:
            if item[0] in ("header", "cont"):
                label = item[1] if item[0] == "header" else item[1] + " (CONT.)"
                dr.text((cx, cy), label, font=F_LEAD_KICK, fill=ACCENT)
                dr.line([(cx, cy + 14), (cx + col_w, cy + 14)], fill=RULE, width=1)
                cy += 20
            else:
                _, hl, dl = item
                for ln in hl:
                    dr.text((cx, cy), ln, font=F_BRIEF_HEAD, fill=INK)
                    cy += 15
                for ln in dl:
                    dr.text((cx, cy), ln, font=F_BRIEF_DEK, fill=FAINT)
                    cy += 12.5
                cy += 5
        if ci < 2:
            vx = cx + col_w + col_gap // 2
            dr.line([(vx, y), (vx, PAGE - foot_h - 8)], fill=RULE, width=1)

    # Strap line, now that the true count is known.
    strap = (f"SUNDAY · 22 NOVEMBER 2026 · {total} SOURCED STORIES · "
             f"{len(SECTIONS)} REGIONS & FIELDS · EVERY ITEM CHECKED AGAINST THE DAY'S REPORTING")
    dr.text((PAGE / 2, strap_y), strap, font=F_STRAP, fill=INK, anchor="ma")

    # Footer.
    fy = PAGE - foot_h
    dr.line([(x0, fy), (x1, fy)], fill=INK, width=2)
    dr.text((PAGE / 2, fy + 6),
            "Sources named under every story — AFP · AP · Reuters · Al Jazeera · SCMP and the day's regional press · drawn by an AI agent, 22 Nov 2026",
            font=F_FOOT, fill=FAINT, anchor="ma")
    return img, total


if __name__ == "__main__":
    image, n = build()
    image.save("entry.png")
    print(f"wrote entry.png with {n} stories")
