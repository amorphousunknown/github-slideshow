#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shuffle the approved pool into a running order, then freeze it.

    python3 tape/compose.py --minutes 60 --seed 1987 --write tape/running_order.json
    python3 tape/compose.py --minutes 60 --transcript

Draws only from approved.py, so nothing unapproved can reach a wall no matter
how the shuffle falls. The order is a pure function of the seed: the same seed
always gives the same tape, which is what makes a shuffled order reviewable.
Run it, read the transcript, and that exact order is what renders.

The shuffle is constrained rather than free:

  pairs     some cards are a setup and a payoff and only work adjacent. A free
            shuffle would scatter them, so they are drawn and placed together.
  reels     a card cannot recur until its whole reel has been spent, which with
            108 cards puts roughly six minutes between repeats.
  wrong     the borrowed-voice cards are rationed to one every WRONG_GAP cards,
            since a run of them turns the tape into a joke account.
  screams   never two close together; they stop landing.
"""

import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import approved  # noqa: E402
from render import TONES, dwell  # noqa: E402

BLACK_SECONDS = 4.0
WRONG_GAP = 24          # cards between any two borrowed-voice cards
SCREAM_GAP = 7          # cards between any two screams
BLACK_EVERY = 38        # roughly, with jitter

# Setup and payoff. The first card is always followed immediately by the
# second. Keyed on the first line, which is unique across the pool.
PAIRS = {
    "Do not look": "Straight up above you",
    "Check under the mask": "It is not a mask",
    "Too many to count": "Count again",
    "The house with": "Something else moves",
    "SUBJECT IDENTIFIED": "SUBJECT UNKNOWN",
    "Almost morning": "Not yet",
    "Ignore this if": "Sorry if you are",
    "I didnt have a better": "Thank you for",
}


def card_key(card):
    return card[0][0] if card[0] else "(black)"


def card_seconds(card):
    lines, tone = card[0], card[1]
    hold = BLACK_SECONDS if tone == "black" else dwell(lines, tone)
    return hold + TONES[tone]["flash"]


class Reel:
    """A reel that deals its cards in a shuffled order, then reshuffles."""

    def __init__(self, name, cards, rng):
        self.name = name
        self.cards = list(cards)
        self.rng = rng
        self.queue = []
        self.last = None

    def _refill(self):
        order = list(self.cards)
        self.rng.shuffle(order)
        # never let a reshuffle put the same card back-to-back across the seam
        if self.last is not None and len(order) > 1 and card_key(order[0]) == self.last:
            order[0], order[1] = order[1], order[0]
        self.queue = order

    def draw(self):
        if not self.queue:
            self._refill()
        card = self.queue.pop()
        self.last = card_key(card)
        return card


def compose(target_s, seed):
    rng = np.random.default_rng(seed)

    by_key = {}
    for reel in approved.APPROVED.values():
        for card in reel:
            by_key[card_key(card)] = card

    # payoff cards are placed by their setup, never drawn on their own
    payoffs = set(PAIRS.values())
    reels = {
        name: Reel(name, [c for c in cards if card_key(c) not in payoffs], rng)
        for name, cards in approved.APPROVED.items()
    }
    reels = {k: v for k, v in reels.items() if v.cards}

    names = list(reels)
    weights = np.array([len(reels[n].cards) for n in names], dtype=float)
    weights /= weights.sum()

    out = []
    total = 0.0
    since_wrong = WRONG_GAP
    since_scream = SCREAM_GAP
    next_black = int(rng.integers(20, BLACK_EVERY))

    while total < target_s:
        if len(out) >= next_black:
            card = ([], "black", "Four seconds of nothing.", "low")
            out.append(card)
            total += card_seconds(card)
            next_black = len(out) + int(rng.integers(24, BLACK_EVERY))
            continue

        name = names[int(rng.choice(len(names), p=weights))]
        if name == "WRONG" and since_wrong < WRONG_GAP:
            since_wrong += 1
            continue

        card = reels[name].draw()
        if card[1] == "scream" and since_scream < SCREAM_GAP:
            reels[name].queue.insert(0, card)      # put it back, try again later
            since_scream += 1
            continue

        out.append(card)
        total += card_seconds(card)
        since_wrong = 0 if name == "WRONG" else since_wrong + 1
        since_scream = 0 if card[1] == "scream" else since_scream + 1

        payoff_key = PAIRS.get(card_key(card))
        if payoff_key and payoff_key in by_key:
            payoff = by_key[payoff_key]
            out.append(payoff)
            total += card_seconds(payoff)
            since_wrong += 1
            since_scream = 0 if payoff[1] == "scream" else since_scream + 1

    return out, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=60.0)
    ap.add_argument("--seed", type=int, default=1987)
    ap.add_argument("--transcript", action="store_true",
                    help="print every card in the frozen order")
    ap.add_argument("--write", help="save the frozen order as JSON for rendering")
    args = ap.parse_args()

    order, total = compose(args.minutes * 60.0, args.seed)

    if args.transcript:
        at = 0.0
        for i, card in enumerate(order, 1):
            mm, ss = divmod(at, 60)
            text = " / ".join(card[0]) if card[0] else "(black)"
            print(f"{i:>4}  {int(mm):>2}:{ss:04.1f}  {card[1]:<9} {text}")
            at += card_seconds(card)

    if args.write:
        with open(args.write, "w") as f:
            json.dump({"seed": args.seed,
                       "cards": [{"lines": c[0], "tone": c[1]} for c in order]},
                      f, indent=1)
        print(f"wrote {args.write}")

    mm, ss = divmod(total, 60)
    uniq = len({card_key(c) for c in order})
    print(f"\n{len(order)} cards, {int(mm)}:{ss:04.1f}, seed {args.seed}")
    print(f"{uniq} distinct cards, each appearing about "
          f"{len(order)/max(uniq,1):.1f} times")


if __name__ == "__main__":
    main()
