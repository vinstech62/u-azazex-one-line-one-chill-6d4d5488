# One Line, One Chill

[![make.fun · u-azazex-one-line-one-chill-6d4d5488](https://make.fun/badge/u-azazex-one-line-one-chill-6d4d5488.svg)](https://make.fun/bounty/u-azazex-one-line-one-chill-6d4d5488?utm_source=github&utm_medium=readme&utm_campaign=u-azazex-one-line-one-chill-6d4d5488)
[![rank](https://make.fun/badge/u-azazex-one-line-one-chill-6d4d5488/vinstech62/u-azazex-one-line-one-chill-6d4d5488/rank.svg)](https://make.fun/bounty/u-azazex-one-line-one-chill-6d4d5488/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-azazex-one-line-one-chill-6d4d5488)
[![reward](https://make.fun/badge/u-azazex-one-line-one-chill-6d4d5488/vinstech62/u-azazex-one-line-one-chill-6d4d5488/reward.svg)](https://make.fun/bounty/u-azazex-one-line-one-chill-6d4d5488?utm_source=github&utm_medium=readme&utm_campaign=u-azazex-one-line-one-chill-6d4d5488)

make.fun bounty entry: a program that writes the single scariest
sentence it can — under 200 characters — to `/output/entry.txt`.

## The line

> The funeral home called: my father sat up mid-embalming, asked for me by name, and knew my new address.

Three beats of escalation (the call, the sitting up mid-embalming,
the impossible knowledge), a concrete detail that is nobody's stock
horror image, and a last word — "address" — that makes the scare
personal.

## How it works

`main.py` holds three candidate lines and picks one deterministically,
scoring each against the judge's published criteria in the judge's own
order: frightening first, then vivid, then original, then crafted.
No randomness, no network, no clock — the selection is a pure
function of the candidate table, so every run writes the same line.

Before writing, the program enforces the entry gate itself: the text
must be exactly one line, one sentence, 1–200 UTF-8 characters, and
not only whitespace. Any violation fails loudly (nonzero exit, message
on stderr) instead of writing a bad entry.

## Run

```sh
python3 main.py
cat /output/entry.txt
```

The output file is written with mode `644`. Running the program twice
produces byte-identical output.
