#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Emit a review page for a block: every card, its timing, intent and risk.

    python3 tape/make_review_page.py 01 > review.html

The page is for sign-off before anything is rendered, so it is generated from
blocks.py rather than transcribed — what is read here is what would play.
"""

import argparse
import base64
import html
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blocks  # noqa: E402
from render import TONES, dwell, render_figure, SEED  # noqa: E402

BLACK_SECONDS = 4.0

TONE_NOTE = {
    "question": "the house voice; long enough to read and answer in your head",
    "dread": "the ones it already knows the answer to; longest hold on the tape",
    "curt": "clipped follow-up, usually landing on the card before it",
    "glitch": "the machine talking to itself, not to you",
    "scream": "one line, large, gone before you are sure you read it",
    "ident": "tape furniture; a breath between runs of questions",
    "black": "nothing on screen; on a wall it reads as the projector dying",
}


def figures_b64(n=4):
    out = []
    for i in range(n):
        img = render_figure(SEED + i * 977).convert("RGB")
        img.thumbnail((300, 225))
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=72)
        out.append(base64.b64encode(buf.getvalue()).decode())
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("block", nargs="?", default="01")
    args = ap.parse_args()
    deck = blocks.BLOCKS[args.block]

    rows, total = [], 0.0
    counts, risks = {}, {}
    for i, (lines, tone, impact, risk) in enumerate(deck, 1):
        hold = BLACK_SECONDS if tone == "black" else dwell(lines, tone)
        flash = TONES[tone]["flash"]
        mm, ss = divmod(total, 60)
        text = ("<br>".join(html.escape(l) for l in lines)
                if lines else "<em class='blk'>(black screen)</em>")
        counts[tone] = counts.get(tone, 0) + 1
        risks[risk] = risks.get(risk, 0) + 1
        rows.append(f"""<li class="card" id="c{i}">
  <div class="n">{i}</div>
  <div class="body">
    <div class="say">{text}</div>
    <div class="meta">
      <span class="t t-{tone}">{tone}</span>
      <span class="secs">{hold:.1f}s on screen</span>
      <span class="at">enters at {int(mm)}:{ss:04.1f}</span>
      <span class="risk r-{risk}">{risk}</span>
    </div>
    <p class="impact">{html.escape(impact)}</p>
  </div>
</li>""")
        total += hold + flash

    mm, ss = divmod(total, 60)
    figs = figures_b64()
    figs_html = "".join(
        f'<img src="data:image/jpeg;base64,{b}" alt="Figure variant {i+1}">'
        for i, b in enumerate(figs))
    tone_rows = "".join(
        f"<tr><td class='t t-{k}'>{k}</td><td>{v}</td>"
        f"<td>{TONES[k]['floor']:.1f}s floor</td><td>{html.escape(TONE_NOTE[k])}</td></tr>"
        for k, v in sorted(counts.items()))

    print(f"""<title>Block 01 Running Order</title>
<style>
  /* Layout: one column of cards in play order, each carrying what it says,
     how long it holds, and what it is expected to do. Single dark theme by
     intent — it is reviewed in the same conditions it is projected in. */
  :root {{
    --void:#0a0a0c; --panel:#121216; --rule:#24242b;
    --fg:#e4e3df; --dim:#8b8a85; --faint:#5a5a57;
    --low:#4a7c59; --med:#b08430; --high:#a33a2a; --cg:#cfd4cf;
    --mono:"SFMono-Regular",ui-monospace,Menlo,Consolas,monospace;
    --sans:"Helvetica Neue",Helvetica,Arial,sans-serif;
    color-scheme: dark;
  }}
  body {{ background:var(--void); color:var(--fg); font-family:var(--sans);
         margin:0; padding:0 16px 80px; line-height:1.5; }}
  .wrap {{ max-width:780px; margin:0 auto; padding-block:40px 0; }}
  h1 {{ font-size:clamp(1.6rem,5vw,2.3rem); margin:0 0 6px; letter-spacing:-.01em;
        text-wrap:balance; }}
  .sub {{ color:var(--dim); margin:0 0 28px; font-size:.95rem; }}
  .bar {{ display:flex; flex-wrap:wrap; gap:10px 22px; padding:14px 16px;
          background:var(--panel); border:1px solid var(--rule); border-radius:3px;
          margin-bottom:30px; font-family:var(--mono); font-size:.76rem;
          color:var(--dim); }}
  .bar b {{ color:var(--fg); font-weight:600; }}
  h2 {{ font-size:1rem; text-transform:uppercase; letter-spacing:.13em;
        color:var(--dim); margin:38px 0 14px; font-weight:600; }}
  ol {{ list-style:none; margin:0; padding:0; }}
  .card {{ display:flex; gap:14px; padding:14px 0; border-top:1px solid var(--rule); }}
  .n {{ font-family:var(--mono); font-size:.8rem; color:var(--faint);
        min-width:2.2em; text-align:right; padding-top:3px; }}
  .body {{ flex:1; min-width:0; }}
  .say {{ font-family:var(--mono); font-size:1.02rem; color:var(--cg);
          text-transform:uppercase; letter-spacing:.055em; line-height:1.32; }}
  .blk {{ color:var(--faint); text-transform:none; letter-spacing:0; font-style:italic; }}
  .meta {{ display:flex; flex-wrap:wrap; gap:6px 12px; margin:8px 0 6px;
           font-family:var(--mono); font-size:.7rem; color:var(--faint); }}
  .t {{ text-transform:uppercase; letter-spacing:.1em; }}
  .t-question{{color:#7f9ec4}} .t-dread{{color:#a98fc0}} .t-curt{{color:#86a08a}}
  .t-glitch{{color:#c4a05f}} .t-scream{{color:#c4766a}} .t-ident{{color:#6f7f8c}}
  .t-black{{color:#5a5a57}}
  .risk {{ padding:1px 7px; border-radius:2px; text-transform:uppercase;
           letter-spacing:.08em; color:#0a0a0c; font-weight:700; }}
  .r-low{{background:var(--low)}} .r-med{{background:var(--med)}} .r-high{{background:var(--high)}}
  .impact {{ margin:0; color:var(--dim); font-size:.88rem; }}
  table {{ border-collapse:collapse; width:100%; font-size:.85rem; }}
  td,th {{ text-align:left; padding:7px 10px; border-bottom:1px solid var(--rule);
           vertical-align:top; }}
  th {{ color:var(--faint); font-family:var(--mono); font-size:.7rem;
        text-transform:uppercase; letter-spacing:.1em; font-weight:500; }}
  td:nth-child(2),td:nth-child(3) {{ font-family:var(--mono); white-space:nowrap;
        font-variant-numeric:tabular-nums; }}
  .figs {{ display:flex; flex-wrap:wrap; gap:10px; margin:14px 0; }}
  .figs img {{ width:min(100%,220px); border:1px solid var(--rule); display:block; }}
  .note {{ background:var(--panel); border:1px solid var(--rule); border-left:2px solid var(--med);
           padding:14px 16px; border-radius:3px; color:var(--dim); font-size:.9rem; }}
  .note b {{ color:var(--fg); }}
</style>

<div class="wrap">
  <h1>Block 01 — running order</h1>
  <p class="sub">Proposed. Nothing is rendered until this is signed off. Reply with the
     numbers you want cut or changed.</p>

  <div class="bar">
    <span><b>{len(deck)}</b> cards</span>
    <span><b>{int(mm)}:{ss:04.1f}</b> runtime</span>
    <span>risk <b>{risks.get('low',0)}</b> low · <b>{risks.get('med',0)}</b> med ·
          <b>{risks.get('high',0)}</b> high</span>
    <span>640×480 · 24fps</span>
  </div>

  <div class="note">
    <b>On the ten-minute unit.</b> This block runs {int(mm)}:{ss:04.1f} across {len(deck)} cards.
    A full ten minutes is roughly 175 cards, and a full hour with nothing repeating
    would be about 1050 — more than is reasonable to approve one by one. The workable
    shape is to approve a <b>pool</b> of cards this way, block by block, then freeze a
    single running order built only from approved material. Every card that can appear
    on the wall would have been signed off; the order is fixed and exportable as a
    transcript.
  </div>

  <h2>Timing</h2>
  <table>
    <tr><th>tone</th><th>cards</th><th>minimum</th><th>what it is for</th></tr>
    {tone_rows}
  </table>
  <p class="sub" style="margin-top:12px">Hold time is
     <code>(0.70s + words × 0.28s) × multiplier</code>, floored per tone, so a long card
     holds longer than a short one in the same voice. Between every pair of cards the
     figure cuts in for 0.08–0.52s depending on the outgoing card.</p>

  <h2>The figure between cards</h2>
  <div class="figs">{figs_html}</div>
  <p class="sub">Generated fresh for each appearance — same face, different grain,
     position and tracking tears every time, so it never looks like a repeated still.
     It is on screen for a fraction of a second. Four of the fourteen variants shown.
     This is the only image on the tape; everything else is type on black.</p>

  <h2>Running order</h2>
  <ol>{"".join(rows)}</ol>
</div>""")


if __name__ == "__main__":
    main()
