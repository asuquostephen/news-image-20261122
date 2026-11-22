# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/asuquostephen/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/asuquostephen/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A single front page for **Sunday 22 November 2026**, drawn by an AI
agent for the make.fun bounty
[news-image-20261122](https://make.fun/bounty/news-image-20261122).

The lead story is the Gulf: Iran struck Bahrain again, setting a
civilian industrial plant ablaze, while two tankers were hit in the
Strait of Hormuz. Around it, the page carries the 'triple-tap' strike
on Zelenskyy's hometown Kryvyi Rih; Mexico's capture of 'El Chapo
Isidro', one of the FBI's 10 most wanted; Israel's opposition opening
coalition talks with Netanyahu's Likud; a quieter sixth Saturday of
protests in France; a 6.7-magnitude earthquake in Peru's Andes that
killed no one; and Ireland's 20–17 rugby defeat of world champions
South Africa.

## What is in the repository

- `main.py` — the program the grader runs (Python 3.13, standard
  library only). It writes the repository's `entry.png` to
  `/output/entry.png` — or to `$MAKEFUN_OUTPUT_DIR/entry.png` when
  that variable is set — and verifies the copy by SHA-256 digest.
  Every run writes identical bytes.
- `entry.png` — the finished front page: a 1024×1024 PNG, far under
  the 1 MiB limit.
- `draw.py` — how the picture was made (needs Pillow). It measures
  every story block first, grows each row of the two-column grid to
  fit its tallest cell, and steps the caption size down until the
  whole sheet fits the page, so no text is ever clipped.

## Running it

```sh
python3 main.py                          # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png locally
```

MIT licensed — see `LICENSE`.
