# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/naufalumer/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/naufalumer/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A newspaper front page summing up Thursday 19 November 2026's world news in one image. One consequential story per panel, each with a picture, a short bold headline and a one-line deck:

1. **Culture — Vice City (hero):** Grand Theft Auto VI goes live, rolling out at midnight market by market — PS5 and Xbox, $79.99; pre-orders near 16m copies, over $1.5bn.
2. **Diplomacy — Shenzhen:** Trump, Xi and Putin meet in Shenzhen for their first trilateral as sitting leaders; nuclear arms top the agenda, no deals expected.
3. **Markets — AI:** Anthropic debuts on Nasdaq as ANT, priced at $83, above its $70–$78 range.
4. **Weather — India:** Cyclone Akvan bears down on India's east coast; red alerts and schools shut, landfall due Friday at 90–100 km/h.
5. **Diplomacy — Tokyo:** India and Japan hold the 4th 2+2 defence ministers' dialogue in Tokyo.
6. **Space:** NASA briefs on Voyager 1's one-light-day mark at noon EST, a day after the probe passed 16bn miles out.

Every story above happened, was first reported, or is scheduled on Thursday 19 November 2026. Sources: Reuters, AP, NASA, IMD, TechCrunch, Press Information Bureau. Full fact notes: `NEWS_FACTS.md`.

## Run it

```sh
python3 main.py
```

`entry.png` is a pre-rendered 1024x1024 image (712 KB, under the 1 MiB cap). `main.py` (Python standard library only) copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), refusing files over 1,048,576 bytes and checking the copy is byte-identical. `render_front.py` is the renderer that produced the image; re-running it renders byte-identical output. Four panels use AI-generated illustrations (`art/*.jpg`, cropped to their exact boxes); the India–Japan and Voyager panels are drawn with PIL primitives. All text is exact vector text.

---

<sub>Entered on [make.fun](https://make.fun/?ref=bye4mn13&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
