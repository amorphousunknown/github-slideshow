#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the debrief tape to an MP4 sized for a cheap SD-card projector.

    python3 tape/render.py --minutes 60 --out tape.mp4

Output is 640x480 (4:3), H.264 baseline-compatible, yuv420p, AAC stereo —
the combination the no-name media players in budget projectors actually
decode. 4:3 is deliberate: projected onto a wall the pillarbox is simply
absent light, and the shape is right for the source material.

The look is built in two places. Everything fixed per card — type,
chromatic fringe, scanlines, vignette — is baked into a PNG once. Everything
that must differ every frame — grain, the drifting tracking bar — is an
ffmpeg filter over the whole timeline, so a card held for four seconds is
still moving.
"""

import argparse
import math
import os
import random
import shutil
import struct
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content  # noqa: E402

W, H = 640, 480
FPS = 24
SEED = 1987

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_CG = os.path.join(HERE, "fonts", "VT323.ttf")
FONT_UI = os.path.join(HERE, "fonts", "ShareTechMono.ttf")

# hold:  multiplier on the reading-time estimate
# floor: minimum seconds on screen
# flash: seconds the frame between cards lasts
# thud:  loudness of the hit on that frame, 0-1
TONES = {
    "question": dict(hold=1.45, floor=3.4, flash=0.15, thud=0.50, size=54),
    "dread":    dict(hold=1.80, floor=3.8, flash=0.33, thud=0.65, size=54),
    "curt":     dict(hold=1.00, floor=2.2, flash=0.21, thud=0.50, size=54),
    "glitch":   dict(hold=0.55, floor=1.1, flash=0.08, thud=0.85, size=42),
    "scream":   dict(hold=0.34, floor=0.9, flash=0.52, thud=1.00, size=82),
    "alarm":    dict(hold=2.00, floor=4.4, flash=0.42, thud=0.70, size=46),
    "ident":    dict(hold=1.20, floor=2.6, flash=0.18, thud=0.40, size=48),
    "black":    dict(hold=1.00, floor=3.0, flash=0.00, thud=0.00, size=0),
}

WORD_S = 0.28
BASE_S = 0.70


def dwell(lines, tone):
    t = TONES[tone]
    words = len(" ".join(lines).split()) if lines else 4
    return round(max(t["floor"], (BASE_S + words * WORD_S) * t["hold"]), 2)


# --------------------------------------------------------------- tape look
def scanline_mask():
    """Darken every other pair of lines, the way a CRT line structure reads."""
    m = np.ones((H, W), dtype=np.float32)
    m[1::2] *= 0.56
    return m


def vignette_mask():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W / 2.0, H * 0.48
    r = np.sqrt(((x - cx) / (W * 0.62)) ** 2 + ((y - cy) / (H * 0.62)) ** 2)
    v = np.clip(1.18 - 0.95 * np.clip(r - 0.42, 0, None) * 1.9, 0.06, 1.0)
    return v.astype(np.float32)


SCAN = scanline_mask()
VIG = vignette_mask()


def finish(img):
    """Apply the artefacts that are constant for a given card."""
    a = np.asarray(img.convert("RGB"), dtype=np.float32)
    a *= (SCAN * VIG)[:, :, None]
    # lift the floor a touch so pure black still reads as tape, not as void
    a += 3.0
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def chroma_text(draw_target, pos, lines, font, line_h, fill=(233, 236, 232),
                centre=False):
    """Draw text three times to make the red/cyan fringe of a bad transfer."""
    layers = [((-3, 0), (255, 30, 80)), ((3, 0), (40, 255, 210)), ((0, 0), fill)]
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(glow)

    for dx_dy, colour in layers:
        dx, dy = dx_dy
        layer = Image.new("RGB", (W, H), (0, 0, 0))
        ld = ImageDraw.Draw(layer)
        for i, line in enumerate(lines):
            x, y = pos[0] + dx, pos[1] + dy + i * line_h
            if centre:
                bb = ld.textbbox((0, 0), line, font=font)
                x = (W - (bb[2] - bb[0])) // 2 + dx
            ld.text((x, y), line, font=font, fill=colour)
            if colour == fill:
                gd.text((x, y), line, font=font, fill=colour)
        draw_target.alpha_composite(layer.convert("RGBA"))

    glow = glow.filter(ImageFilter.GaussianBlur(5))
    g = np.asarray(glow, dtype=np.float32) * 0.42
    base = np.asarray(draw_target.convert("RGB"), dtype=np.float32)
    out = np.clip(base + g, 0, 255).astype(np.uint8)
    return Image.fromarray(out).convert("RGBA")


def render_caption(lines, tone, centre=False):
    size = TONES[tone]["size"]
    lines = [l.upper() for l in lines]
    font = ImageFont.truetype(FONT_CG, size)
    # no caption may run past the safe right edge; step the size down until it fits
    probe = ImageDraw.Draw(Image.new("RGB", (W, H)))
    avail = W - int(W * 0.13) - 16
    while size > 20:
        widest = max(probe.textlength(l, font=font) for l in lines)
        if widest <= avail:
            break
        size -= 2
        font = ImageFont.truetype(FONT_CG, size)
    line_h = int(size * 1.16)
    img = Image.new("RGBA", (W, H), (6, 6, 8, 255))
    x = int(W * 0.13)
    y = int(H * 0.23)
    if centre:
        total = line_h * len(lines)
        y = (H - total) // 2
    img = chroma_text(img, (x, y), lines, font, line_h, centre=centre)
    return finish(img)


# ------------------------------------------------------------ seven segment
SEGMENTS = {
    "0": "abcdef", "1": "bc", "2": "abdeg", "3": "abcdg", "4": "bcfg",
    "5": "acdfg", "6": "acdefg", "7": "abc", "8": "abcdefg", "9": "abcdfg",
}
CELL_W, CELL_H, SEG_T, SEG_GAP, COLON_W = 56, 104, 12, 18, 24


def _h(x, y):
    L = CELL_W - 2 * SEG_T
    t = SEG_T
    return [(x, y + t / 2), (x + t / 2, y), (x + L - t / 2, y), (x + L, y + t / 2),
            (x + L - t / 2, y + t), (x + t / 2, y + t)]


def _v(x, y, L):
    t = SEG_T
    return [(x + t / 2, y), (x + t, y + t / 2), (x + t, y + L - t / 2),
            (x + t / 2, y + L), (x, y + L - t / 2), (x, y + t / 2)]


def render_clock(time_str, label):
    mid = (CELL_H - SEG_T) / 2
    run = mid - SEG_T
    scale = 2.25
    cells = []
    x = 0
    for ch in time_str:
        if ch == ":":
            cells.append(("colon", x, COLON_W))
            x += COLON_W + SEG_GAP
        else:
            # a 1 gets a narrow cell, the way a real display sets it
            cw = CELL_W * 0.5 if ch == "1" else CELL_W
            cells.append((ch, x, cw))
            x += cw + SEG_GAP
    total_w = x - SEG_GAP

    plate = Image.new("RGB", (int(total_w * scale) + 40, int(CELL_H * scale) + 40),
                      (0, 0, 0))
    pd = ImageDraw.Draw(plate)
    red = (212, 26, 16)

    def put(points):
        pd.polygon([(20 + px * scale, 20 + py * scale) for px, py in points], fill=red)

    for ch, ox, cw in cells:
        if ch == "colon":
            for cy in (CELL_H * 0.24, CELL_H * 0.62):
                pd.ellipse([20 + (ox + (COLON_W - SEG_T * 1.3) / 2) * scale,
                            20 + cy * scale,
                            20 + (ox + (COLON_W + SEG_T * 1.3) / 2) * scale,
                            20 + (cy + SEG_T * 1.3) * scale], fill=red)
            continue
        geo = {
            "a": _h(ox + SEG_T, 0),
            "b": _v(ox + cw - SEG_T, SEG_T, run),
            "c": _v(ox + cw - SEG_T, mid + SEG_T, run),
            "d": _h(ox + SEG_T, CELL_H - SEG_T),
            "e": _v(ox, mid + SEG_T, run),
            "f": _v(ox, SEG_T, run),
            "g": _h(ox + SEG_T, mid),
        }
        for k in SEGMENTS.get(ch, ""):
            put(geo[k])

    bloom = plate.filter(ImageFilter.GaussianBlur(9))
    plate = Image.fromarray(np.clip(
        np.asarray(plate, np.float32) + np.asarray(bloom, np.float32) * 1.25,
        0, 255).astype(np.uint8))

    img = Image.new("RGB", (W, H), (0, 0, 0))
    px = (W - plate.width) // 2
    py = int(H * 0.22)
    img.paste(plate, (px, py))

    font = ImageFont.truetype(FONT_CG, 52)
    d = ImageDraw.Draw(img)
    bb = d.textbbox((0, 0), label, font=font)
    lx = (W - (bb[2] - bb[0])) // 2
    ly = py + plate.height + 2
    d.text((lx, ly), label, font=font, fill=red)
    glow = img.filter(ImageFilter.GaussianBlur(6))
    img = Image.fromarray(np.clip(
        np.asarray(img, np.float32) + np.asarray(glow, np.float32) * 0.5,
        0, 255).astype(np.uint8))

    # the clock card is its own world: no scanlines, just the red in the dark
    a = np.asarray(img, np.float32) * VIG[:, :, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def render_black():
    return finish(Image.new("RGBA", (W, H), (6, 6, 8, 255)))


# ------------------------------------------------------------ the figure
def render_figure(seed):
    """The frame between cards. Procedural, different every time it appears."""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)

    cx = W / 2 + rng.uniform(-40, 40)
    cy = H * 0.46 + rng.uniform(-25, 25)
    rx = W * rng.uniform(0.17, 0.23)
    ry = H * rng.uniform(0.31, 0.40)

    r = np.sqrt(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2)
    face = np.clip(1.0 - r, 0, 1) ** 1.5
    img = face * rng.uniform(150, 205)

    def socket(ox, oy, srx, sry):
        rr = np.sqrt(((x - ox) / srx) ** 2 + ((y - oy) / sry) ** 2)
        return np.clip(1.0 - rr, 0, 1) ** 0.8

    ex = rx * 0.42
    ey = cy - ry * 0.16
    img -= socket(cx - ex, ey, rx * 0.26, ry * 0.19) * 240
    img -= socket(cx + ex, ey, rx * 0.26, ry * 0.19) * 240
    img += socket(cx - ex, ey - 3, 3.5, 3.5) * 150
    img += socket(cx + ex, ey - 3, 3.5, 3.5) * 150
    img -= socket(cx, cy + ry * 0.52, rx * 0.30, ry * 0.07) * 200

    img += rng.normal(0, 22, (H, W))
    img = np.clip(img, 0, 255)

    # tracking tears: shove bands of the picture sideways
    for _ in range(rng.integers(3, 7)):
        top = int(rng.integers(0, H - 20))
        hgt = int(rng.integers(3, 26))
        shift = int(rng.integers(-34, 34))
        img[top:top + hgt] = np.roll(img[top:top + hgt], shift, axis=1)
        img[top:top + hgt] += rng.uniform(10, 40)

    img = np.clip(img, 0, 255)
    rgb = np.stack([img, img, img], axis=-1)
    rgb[:, :, 0] *= 1.04      # the smallest warm bias, so it isn't dead grey
    rgb[:, :, 2] *= 0.97
    out = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
    return finish(out.convert("RGBA"))


def render_bar():
    """The tracking bar that drifts up the picture. Overlaid live by ffmpeg."""
    bh = 110
    a = np.zeros((bh, W, 4), dtype=np.float32)
    prof = np.sin(np.linspace(0, math.pi, bh)) ** 2
    a[:, :, :3] = 236.0
    a[:, :, 3] = (prof * 26)[:, None]
    return Image.fromarray(a.astype(np.uint8), mode="RGBA")


# ------------------------------------------------------------ the playlist
def build_playlist(target_s, rng):
    """Walk the reels in order, shuffling within each, until the hour is full.

    Cards are consumed from shuffled copies of each reel, so a card cannot
    recur until its whole reel has been spent — roughly a twenty minute gap,
    and never twice in a row.
    """
    pools = {name: [] for name, _ in content.REELS}
    sys_pool, ident_pool, clock_pool = [], [], []
    items, total = [], 0.0

    def draw(pool, source):
        if not pool:
            pool.extend(source)
            rng.shuffle(pool)
        return pool.pop()

    reel_i = 0
    while total < target_s:
        name, cards = content.REELS[reel_i % len(content.REELS)]
        reel_i += 1

        # a short ident to open the section
        if rng.random() < 0.75:
            lines = draw(ident_pool, content.IDENTS)
            items.append(dict(kind="ident", lines=lines, tone="ident"))
            total += dwell(lines, "ident") + TONES["ident"]["flash"]

        run = rng.integers(5, 9)
        for _ in range(int(run)):
            if not pools[name]:
                pools[name] = list(cards)
                rng.shuffle(pools[name])
            lines, tone = pools[name].pop()
            items.append(dict(kind="caption", lines=lines, tone=tone))
            total += dwell(lines, tone) + TONES[tone]["flash"]

            roll = rng.random()
            if roll < 0.13:
                lines = draw(sys_pool, content.SYSTEM)
                items.append(dict(kind="caption", lines=lines, tone="glitch"))
                total += dwell(lines, "glitch") + TONES["glitch"]["flash"]
            elif roll < 0.18:
                t, label = draw(clock_pool, content.CLOCKS)
                items.append(dict(kind="clock", time=t, label=label, tone="alarm"))
                total += dwell([label], "alarm") + TONES["alarm"]["flash"]
            elif roll < 0.23:
                d = round(float(rng.uniform(2.5, 6.0)), 2)
                items.append(dict(kind="black", tone="black", seconds=d))
                total += d

    return items, total


# ------------------------------------------------------------ audio
def write_audio(items, path, rng):
    """A low bed under the whole tape, with a hit on every cut."""
    sr = 44100
    wf = wave.open(path, "wb")
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)

    phase = 0.0
    for it in items:
        secs = it["_dur"] + it["_flash"]
        n = int(secs * sr)
        if n <= 0:
            continue
        t = np.arange(n, dtype=np.float32) / sr

        # bed: a 47 Hz drone with slow movement, plus filtered hiss
        drone = np.sin(2 * math.pi * 47.0 * t + phase) * 0.030
        drone += np.sin(2 * math.pi * 23.5 * t + phase) * 0.018
        drone *= 0.85 + 0.15 * np.sin(2 * math.pi * 0.07 * t)
        phase = (phase + 2 * math.pi * 47.0 * secs) % (2 * math.pi)

        hiss = rng.normal(0, 1, n).astype(np.float32)
        hiss = np.convolve(hiss, np.ones(12, dtype=np.float32) / 12, mode="same")
        buf = drone + hiss * 0.012

        # the hit, landing on the cut into the frame between cards
        force = TONES[it["tone"]]["thud"]
        if force > 0 and it["_flash"] > 0:
            start = int(it["_dur"] * sr)
            hl = min(int(sr * (0.9 + 0.6 * force)), n - start)
            if hl > 64:
                ht = np.arange(hl, dtype=np.float32) / sr
                env = np.exp(-ht * (5.5 - 2.5 * force))
                sweep = 86 + 64 * force
                f = sweep * np.exp(-ht * 7.0) + 26
                thump = np.sin(2 * math.pi * np.cumsum(f) / sr) * env
                burst = rng.normal(0, 1, hl).astype(np.float32)
                burst = np.convolve(burst, np.ones(6, dtype=np.float32) / 6,
                                    mode="same") * np.exp(-ht * 26)
                buf[start:start + hl] += (thump * (0.16 + 0.30 * force)
                                          + burst * (0.05 + 0.10 * force))

        wf.writeframes((np.clip(buf, -1, 1) * 32000).astype("<i2").tobytes())

    wf.close()


# ------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=60.0)
    ap.add_argument("--out", default="tape.mp4")
    ap.add_argument("--work", default="build")
    ap.add_argument("--crf", type=int, default=25)
    ap.add_argument("--keep", action="store_true", help="keep the frame cache")
    args = ap.parse_args()

    rng = np.random.default_rng(SEED)
    random.seed(SEED)

    work = os.path.abspath(args.work)
    frames = os.path.join(work, "frames")
    if os.path.isdir(work) and not args.keep:
        shutil.rmtree(work)
    os.makedirs(frames, exist_ok=True)

    target = args.minutes * 60.0
    items, est = build_playlist(target, rng)
    print(f"playlist: {len(items)} cards, {est/60:.1f} min")

    # one PNG per distinct card, reused wherever it recurs
    cache = {}
    figures = []
    for i in range(14):
        p = os.path.join(frames, f"fig{i:02d}.png")
        render_figure(SEED + i * 977).save(p)
        figures.append(p)

    def frame_for(it):
        if it["kind"] == "black":
            key = ("black",)
        elif it["kind"] == "clock":
            key = ("clock", it["time"], it["label"])
        else:
            key = (it["kind"], tuple(it["lines"]), it["tone"])
        if key in cache:
            return cache[key]
        path = os.path.join(frames, f"c{len(cache):04d}.png")
        if it["kind"] == "black":
            img = render_black()
        elif it["kind"] == "clock":
            img = render_clock(it["time"], it["label"])
        elif it["kind"] == "ident":
            img = render_caption(it["lines"], "ident", centre=True)
        else:
            img = render_caption(it["lines"], it["tone"])
        img.save(path)
        cache[key] = path
        return path

    lines_out = []
    total = 0.0
    for it in items:
        it["_dur"] = it.get("seconds", dwell(it.get("lines", []), it["tone"]))
        it["_flash"] = TONES[it["tone"]]["flash"]
        card = frame_for(it)
        lines_out.append(f"file '{card}'\nduration {it['_dur']:.3f}")
        total += it["_dur"]
        if it["_flash"] > 0:
            fig = figures[int(rng.integers(0, len(figures)))]
            lines_out.append(f"file '{fig}'\nduration {it['_flash']:.3f}")
            total += it["_flash"]
    # the concat demuxer ignores the final duration unless the file repeats
    lines_out.append(f"file '{lines_out[-1].split(chr(10))[0][6:-1]}'")

    concat = os.path.join(work, "concat.txt")
    with open(concat, "w") as f:
        f.write("\n".join(lines_out) + "\n")
    print(f"distinct frames: {len(cache)} cards + {len(figures)} figures")
    print(f"timeline: {total/60:.2f} min")

    render_bar().save(os.path.join(work, "bar.png"))

    wav = os.path.join(work, "bed.wav")
    write_audio(items, wav, rng)
    print(f"audio: {os.path.getsize(wav)/1e6:.0f} MB wav")

    vf = (
        "[0:v]fps={fps},format=rgb24,"
        "noise=alls=13:allf=t+u,"
        "boxblur=2:1:0:0,"
        "format=yuv420p[base];"
        "[base][1:v]overlay=x=0:y='mod(t*58\\,{hh})-110':format=yuv420[v]"
    ).format(fps=FPS, hh=H + 220)

    cmd = [
        "ffmpeg", "-hide_banner", "-y",
        "-f", "concat", "-safe", "0", "-i", concat,
        "-loop", "1", "-i", os.path.join(work, "bar.png"),
        "-i", wav,
        "-filter_complex", vf,
        "-map", "[v]", "-map", "2:a",
        "-c:v", "libx264",
        "-profile:v", "main", "-level", "3.0",
        "-preset", "veryfast", "-crf", str(args.crf),
        "-maxrate", "2000k", "-bufsize", "4000k",
        "-pix_fmt", "yuv420p",
        "-g", str(FPS * 2), "-keyint_min", str(FPS),
        "-r", str(FPS),
        "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2",
        "-movflags", "+faststart",
        "-shortest",
        args.out,
    ]
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)

    size = os.path.getsize(args.out) / 1e6
    print(f"\nwrote {args.out}  {size:.0f} MB")


if __name__ == "__main__":
    main()
