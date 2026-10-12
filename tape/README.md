# Debrief tape

Renders an hour-long loop of the debrief tape to an MP4 that plays off an SD
card in a cheap projector.

## Build

    python3 tape/render.py --minutes 60 --out tape.mp4

Needs `ffmpeg`, `numpy` and `Pillow`. The two fonts ship in `tape/fonts/`.

## Output

640x480 (4:3), 24 fps, H.264 main profile level 3.0, yuv420p, AAC stereo,
capped at 2 Mbit/s with `faststart`. That combination is what the no-name
media players in budget projectors actually decode. 4:3 is deliberate:
projected onto a wall the pillarbox is simply absent light.

## Where the look comes from

Everything fixed for a given card — type, chromatic fringe, scanlines,
vignette — is baked into a PNG once and reused wherever that card recurs.
Everything that must differ every frame — grain, the drifting tracking bar —
is an ffmpeg filter over the whole timeline, so a card held for four seconds
is still moving.

## Editing the content

`content.py` holds every card, grouped into ten reels. Each caption is a list
of lines that break exactly where they are written. Add to a reel and the hour
rebuilds around it; the playlist walks the reels in order and shuffles within
each, so a card cannot recur until its whole reel has been spent.

Timing is derived, not fixed: hold time is
`(0.70s + words x 0.28s) x tone multiplier`, floored per tone. `TONES` in
`render.py` sets the multipliers, the floors, the size, and how hard the
frame between cards hits.

## Useful flags

    --minutes 5     a short test cut
    --crf 23        higher quality, bigger file (default 25)
    --work DIR      where frame PNGs and the concat list are written
