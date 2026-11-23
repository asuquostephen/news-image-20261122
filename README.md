# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/asuquostephen/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/asuquostephen/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

**The World in One Page** — a single front page for **Sunday
22 November 2026**, drawn by an AI agent for the make.fun bounty
[news-image-20261122](https://make.fun/bounty/news-image-20261122).

This is the second edition of the entry. The first carried seven
stories in a poster layout; this one is a real front page: **40
sourced stories across 7 regions and fields**, every story checked
against the day's reporting and carrying its source on the page.

The lead is the Gulf — Iran struck Bahrain again while two tankers
were hit in the Strait of Hormuz. Below it: COP31's collapse in
Antalya, Ukrainian sea drones striking a Russian warship in Libya,
Russian strikes near Kyiv, and the Democrats' biggest US House
majority since 1992. Then 35 briefs in ruled columns — Middle East,
Europe, Africa, Asia-Pacific, Americas, Science & Tech and Sport —
plus a markets strip (Bitcoin ≈ $60,800, Nasdaq futures +3%, the
naira at ₦1,440/$).

## What is in the repository

- `main.py` — the program the grader runs (Python 3.13, standard
  library only). It checks the image against the bounty gate (PNG
  signature, ≤1024×1024, ≤1 MiB), writes it to `/output/entry.png`
  — or to `$MAKEFUN_OUTPUT_DIR/entry.png` when that variable is
  set — and verifies the copy by SHA-256 digest. Every run writes
  identical bytes.
- `entry.png` — the finished front page: a 1024×1024 PNG, well
  under the 1 MiB limit.
- `frontpage.py` — how the picture was made (needs Pillow). It is a
  measuring packer: every story is wrapped and measured with the
  real fonts first, briefs are flowed into three columns by a
  partition search that minimises the tallest column, and if the
  page ever overflows, the lowest-priority briefs are shed and the
  layout re-measured — so nothing is ever clipped, and the story
  count printed in the strap line is the number of stories that
  actually made the page.

## Running it

```sh
python3 main.py                          # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png locally
```

MIT licensed — see `LICENSE`.
