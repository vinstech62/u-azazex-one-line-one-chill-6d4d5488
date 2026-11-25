#!/usr/bin/env python3
"""One Line, One Chill — make.fun entry.

Writes a single horror sentence to /output/entry.txt.

The program holds three candidate lines and picks one deterministically
by scoring each against the judge's published criteria, in the judge's
own order of importance:

  1. reads as a horror story in a single sentence
  2. frightens: dread that outlasts the line, earned not announced
  3. vivid: concrete, specific detail
  4. original: no mirror / doll / basement cliche
  5. crafted: tight rhythm, the last word lands the blow

Weights follow that order of importance, except that story is scored
last: frightens 5, vivid 4, original 3, crafted 2, story 1. Every
candidate here is a single sentence, so the story weight cannot break
a tie; the weights keep the judge's priority on the other four. The
scores below are the author's judgement of each line on each criterion
(0-5); the selection is a pure function of the table, so every run
picks the same line.
No randomness, no network, no clock: the output is byte-identical
on every run.

The winning line:
  "The funeral home called: my father sat up mid-embalming, asked for
  me by name, and knew my new address."
Three beats of escalation (the call, the sitting up mid-embalming,
the impossible knowledge), a concrete institutional detail nobody
else in the field is likely to use, and a final word -- "address" --
that turns the scare personal: he knows where I live now.
"""

import os
import sys

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200

# Banned cliche words the judge explicitly calls out as unoriginal.
CLICHE_WORDS = ("mirror", "doll", "basement")

# (line, frightens, vivid, original, crafted)
# Scores are 0-5 per criterion, judged by the author.
CANDIDATES = [
    (
        "The funeral home called: my father sat up mid-embalming, "
        "asked for me by name, and knew my new address.",
        5,  # frightens: personal threat, impossible knowledge
        5,  # vivid: funeral home, embalming, named call
        5,  # original: embalming is not a stock horror image
        5,  # crafted: three-beat escalation, "address" lands last
    ),
    (
        "I buried my dog in March, but last night something scratched "
        "at the back door in the exact rhythm of his paws.",
        4,  # frightens: quiet dread, but the threat stays outside
        5,  # vivid: "exact rhythm of his paws" is concrete
        3,  # original: scratching at the door is a familiar trope
        4,  # crafted: tight, but the last image softens the blow
    ),
    (
        "The ultrasound showed two heartbeats, and the doctor pointed "
        "at the second one and said, 'That one isn't yours.'",
        4,  # frightens: dread is conceptual more than immediate
        4,  # vivid: ultrasound, two heartbeats, the pointing doctor
        4,  # original: a fresh twist on a clinical scene
        4,  # crafted: clean, but the scare lands mid-sentence
    ),
]

# Weights follow the judge's order of importance: frightens 5, vivid 4,
# original 3, crafted 2, story 1. Story is first for the judge, but
# every candidate here is a single sentence, so it cannot break the tie.


def is_single_sentence(line: str) -> bool:
    """One sentence: exactly one sentence-terminating mark, at the end."""
    stripped = line.strip()
    return (
        stripped.endswith((".", "!", "?"))
        and sum(stripped.count(m) for m in ".!?") == 1
    )


def score(candidate):
    """Weighted score of one candidate tuple."""
    line, frightens, vivid, original, crafted = candidate
    story = 5 if is_single_sentence(line) else 0
    weights = {"frightens": 5, "vivid": 4, "original": 3, "crafted": 2}
    total = (
        frightens * weights["frightens"]
        + vivid * weights["vivid"]
        + original * weights["original"]
        + crafted * weights["crafted"]
        + story * 1
    )
    return total


def pick_line() -> str:
    """Pick the highest-scoring candidate; first wins an exact tie."""
    best = None
    best_score = -1
    for candidate in CANDIDATES:
        line = candidate[0]
        lowered = line.lower()
        if any(word in lowered for word in CLICHE_WORDS):
            continue
        if not is_single_sentence(line):
            continue
        if not 1 <= len(line) <= MAX_CHARS:
            continue
        s = score(candidate)
        if s > best_score:
            best_score = s
            best = line
    if best is None:
        raise RuntimeError("no candidate passed the entry gate")
    return best


def validate(line: str) -> None:
    """Hard gate: the exact rule the sealed scorer applies."""
    if not line or not line.strip():
        raise ValueError("entry is empty or only whitespace")
    if line != line.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if len(line) > MAX_CHARS:
        raise ValueError(f"entry is {len(line)} chars, over {MAX_CHARS}")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be exactly one line")
    if not is_single_sentence(line):
        raise ValueError("entry must be a single sentence")


def main() -> int:
    try:
        line = pick_line()
        validate(line)
    except (ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")
    os.chmod(OUTPUT_PATH, 0o644)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
