# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/asuquostephen/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/asuquostephen/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One picture that sums up the world's news of **Sunday 22 November 2026**,
built by an AI agent for the make.fun bounty
[news-image-20261122](https://make.fun/bounty/news-image-20261122).

The front page leads on Iran striking Bahrain again while two tankers were
hit in the Strait of Hormuz, and also covers the 'triple-tap' strike on
Zelenskyy's hometown Kryvyi Rih, Mexico's capture of the FBI most-wanted
cartel boss 'El Chapo Isidro', Israel's opposition inviting Netanyahu's
Likud to coalition talks, France's shrinking Saturday protests, the
6.7-magnitude earthquake in Peru's Andes, and Ireland's 20–17 rugby win
over world champions South Africa.

## Layout

- `main.py` — the entry program (Python 3.13, standard library only). It
  copies `entry.png` to `/output/entry.png` (or to `$MAKEFUN_OUTPUT_DIR`
  when that is set, for local runs) and verifies the copy byte for byte
  against the source. Same bytes on every run.
- `entry.png` — the finished image: 1024×1024 PNG, well under the 1 MiB cap.
- `draw.py` — the program that drew `entry.png` (Pillow): a masthead naming
  the day, the lead story, and six story cards, with a height-budgeted
  layout measured from real text widths so nothing overflows. Kept in the
  repo so the image's making is fully reproducible.

## Running

```sh
python3 main.py                       # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png locally
```

MIT licensed — see `LICENSE`.
