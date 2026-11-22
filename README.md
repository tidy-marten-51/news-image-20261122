# The World Today — Sunday 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/tidy-marten-51/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/tidy-marten-51/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A newspaper front page summing up the world's news of Sunday
22 November 2026, drawn programmatically with Python 3 and PIL —
no photos, no network, no external assets. Every illustration is
original flat art drawn in code: the Pentagon between the US and
Canadian flags, a courtroom, a burning tanker in the Gulf, three
summit flags, an Andes quake, a missile over Poland and a credit
card.

**Lead story:** the Pentagon moves to restrict US–Canada defence
ties, AFP reported on 22 November.

**Also on the page:** the World Court finds Myanmar guilty of
genocide against the Rohingya; Iran strikes three tankers and a
US air base in Kuwait and targets Bahrain; Trump, Xi and Putin
hold rare three-way talks on nuclear risks with no breakthrough;
a 6.7–6.9 earthquake hits Peru's Andes with no deaths reported;
a Russian missile crashes in Poland; Trump vows a 10% cap on
credit card interest rates; plus briefs on Taiwan warning PM
Carney, Kim's factory visits, Houthi strikes on the Saudi
capital, historic flooding in Florida, South Korea's AI race,
protests at Meta offices in India and 11 deaths from tainted
alcohol in Manipur.

## Run

```sh
python3 main.py            # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Output: a deterministic 1024×1024 PNG under 1 MiB. Running it twice
produces byte-identical files.

## Files

- `main.py` — entrypoint: composes the page and writes `entry.png`
- `draw_frontpage.py` — text, rules and all illustration drawing
- `entry.png` — the rendered front page (produced by running `main.py`)

## License

MIT — see `LICENSE`.
