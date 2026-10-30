# Baltic threat briefing

A daily, fact-based briefing on Russia, NATO and the Baltic states: warning indicators, a claim tracker that flags where sources contradict each other, key reporting with a critical take, and trends over time.

**Read it:** https://vytuatus.github.io/baltic-briefing/ · Lietuviškai: https://vytuatus.github.io/baltic-briefing/lt/

## How it works

- Each morning a scheduled Claude task researches public sources (official and intelligence statements, Baltic, Ukrainian, US and international media, OSINT analysts, and Russian independent and state media), rates the warning indicators and checks the day's claims.
- The day's rows are appended to the JSON files in `data/`, which keep every past edition.
- A Lithuanian translation of each day's rows goes into `data/lt/`.
- `build.py` turns those files into the self-contained `index.html` (English) and `lt/index.html` (Lithuanian) served by GitHub Pages.

## Limits

Built from the public web only: no dark-web, classified or paywalled material. Intelligence claims are reported as stated, not independently verified. A quiet indicator means nothing has been reported, not that nothing is happening. Not a substitute for official warnings from your government.
