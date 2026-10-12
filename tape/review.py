#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Print a block's running order for approval, with exact timings.

    python3 tape/review.py 01

Shows every card in order, what it says, how long it is on screen, what it is
expected to do, and how a stranger could take it. Nothing is rendered.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blocks  # noqa: E402
from render import TONES, dwell  # noqa: E402

BLACK_SECONDS = 4.0


def card_times(card):
    lines, tone = card[0], card[1]
    hold = BLACK_SECONDS if tone == "black" else dwell(lines, tone)
    return hold, TONES[tone]["flash"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("block", nargs="?", default="01")
    ap.add_argument("--risk", choices=["low", "med", "high"],
                    help="only show cards at this risk level")
    args = ap.parse_args()

    deck = blocks.BLOCKS[args.block]
    total = 0.0
    counts, risks = {}, {}

    print(f"BLOCK {args.block} — proposed running order\n")
    print(f"{'#':>3}  {'at':>7}  {'secs':>5}  {'tone':<9} {'risk':<5} text")
    print("-" * 100)

    for i, card in enumerate(deck, 1):
        lines, tone, impact, risk = card
        hold, flash = card_times(card)
        at = total
        text = " / ".join(lines) if lines else "(black)"
        counts[tone] = counts.get(tone, 0) + 1
        risks[risk] = risks.get(risk, 0) + 1
        if not args.risk or args.risk == risk:
            mm, ss = divmod(at, 60)
            print(f"{i:>3}  {int(mm):>2}:{ss:04.1f}  {hold:>5.1f}  {tone:<9} {risk:<5} {text}")
            print(f"{'':>3}  {'':>7}  {'':>5}  {'':<9} {'':<5} └ {impact}")
        total += hold + flash

    mm, ss = divmod(total, 60)
    print("-" * 100)
    print(f"{len(deck)} cards, {int(mm)}:{ss:04.1f} including the frame between cards\n")
    print("tones: " + "  ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    print("risk:  " + "  ".join(f"{k} {v}" for k, v in sorted(risks.items())))


if __name__ == "__main__":
    main()
