# -*- coding: utf-8 -*-
"""Cards signed off by the author.

Separate from content.py on purpose. content.py is a drafting pool; everything
here has been read and kept by the person whose building it is projected from
and who carries the message. Nothing enters this file without that.

Each card is (lines, tone, impact, risk) — the same shape blocks.py uses.
Risk is how a stranger alone on a street at night could take it:
  low   reads as fiction, clinical, or about someone else
  med   second person, could feel aimed at the reader
  high  could be taken as a real warning, instruction or threat

Several cards here are high. That is a deliberate choice by the author, made
with the ratings in front of them, not an oversight.
"""

# --------------------------------------------------------------------------
# The street. These speak to whoever is on the pavement, which nothing else
# on the tape does. They are the strongest cards and carry the most risk.
STREET = [
    (["Do not look"], "scream",
     "One line, large, under a second. Sets up the card after it.", "med"),
    (["Straight up above you"], "dread",
     "Pays off the card before it. People look up. Pairs only — never alone.", "med"),
    (["How long have you", "been followed"], "dread",
     "Reframes the walk they just took. Lands hardest on someone alone.", "high"),
    (["The person beside you", "their face just changed"], "dread",
     "Only works on a group, which is most of a Halloween street. "
     "Everyone looks at everyone.", "high"),
    (["Not you", "the one behind you"], "dread",
     "The turn-around card. Strongest on the tape and the one most likely "
     "to be taken as real.", "high"),
    (["Your mirror self", "appears when viewed"], "question",
     "Quieter and stranger than the rest. Sits with people afterwards.", "med"),
    (["You will forget this"], "curt",
     "Flat and certain. Reads as a threat or a kindness depending on the reader.", "med"),
    (["Eat the candy"], "curt",
     "The one joke in the street reel. On Halloween it reads as a joke; "
     "out of season it reads as an instruction from a stranger.", "med"),
    (["Keep walking"], "curt",
     "Dismissive, which is worse than menacing. Could be read as a real "
     "instruction by someone already uneasy.", "high"),
    (["Run"], "scream",
     "One word. The highest-risk card on the tape: no context survives at "
     "this speed, and some readers will simply believe it.", "high"),
    (["Wrong street"], "scream",
     "Disorienting without threatening. Does the work of Run at half the risk.", "med"),
    (["Not here"], "scream",
     "Same register. Reads as a refusal rather than a warning.", "med"),
]

# --------------------------------------------------------------------------
# The returned. The author's own register, and a different one: the dead come
# back on this night, and some of them are glad to see you. Melancholy rather
# than clinical. Kept as its own reel so it does not fight the machine voice.
RETURNED = [
    (["Why is it only", "on this night", "I get to see you", "again"], "dread",
     "The tenderest card on the tape, and the only one that wants something. "
     "Longest hold. This is the one people will remember.", "low"),
    (["Back again", "How was the afterlife"], "curt",
     "Casual about something enormous. The flatness is the joke.", "low"),
    (["The dead walk", "the night"], "dread",
     "Plain statement of the season. Grounds the stranger cards around it.", "low"),
    (["You are never alone", "when you have", "two shadows"], "dread",
     "Reads as folklore rather than a threat, so it lands without alarming.", "med"),
    (["What happens when", "the night goes still"], "question",
     "Open question. Makes the quiet between traffic feel deliberate.", "low"),
    (["Have you heard it", "when it goes quiet"], "question",
     "People stop and listen. Reliable physical reaction, no risk.", "low"),
    (["Something answered"], "curt",
     "Two words doing the work of a paragraph. Answers nothing.", "low"),
    (["Little flying vampires"], "curt",
     "Bats. The lightest card kept — a breath between heavier ones.", "low"),
]

# --------------------------------------------------------------------------
# The file. The machine's interrogation voice, edited by the author.
FILE = [
    (["How are you here"], "question",
     "Opens by questioning the reader's presence rather than their answers.", "med"),
    (["You arrived on foot"], "curt",
     "Flat observation that happens to be true of everyone reading it.", "med"),
    (["You are the one", "on file"], "dread",
     "Singles the reader out. The whole apparatus suddenly points at them.", "med"),
    (["The tape has", "your answers"], "dread",
     "Implies they have already been through this. Good on a loop.", "med"),
    (["One of them is", "ahead of you"], "dread",
     "Works without ever saying what 'them' is.", "high"),
    (["Are the lights on"], "question",
     "Three words that send people looking at their own windows.", "med"),
]

# --------------------------------------------------------------------------
# Machine status. Printed by the tape for itself, not addressed to anyone.
SYSTEM = [
    (["LAST CAR", "OCCUPANCY 1", "SHADOWS 2"], "glitch",
     "Data rather than address, so it unsettles without accusing.", "low"),
    (["SPIRIT ASSIGNED", "TO OBSERVER"], "glitch",
     "Bureaucracy applied to the supernatural. Funny and not.", "low"),
    (["NON HUMAN VIEWER", "COUNT RISING"], "glitch",
     "Counts the audience, then says the count is wrong.", "low"),
    (["SUBJECT IDENTIFIED"], "glitch",
     "Two words. The reader supplies the dread themselves.", "med"),
    (["SUBJECT UNKNOWN"], "glitch",
     "The reverse, and somehow worse. Good directly after the card above.", "low"),
]

APPROVED = {
    "STREET": STREET,
    "RETURNED": RETURNED,
    "FILE": FILE,
    "SYSTEM": SYSTEM,
}

# --------------------------------------------------------------------------
# Held back pending the author's wording. The voice transcription was unclear
# and these are not mine to guess at — see the questions put to them. Nothing
# here renders.
PENDING = [
    "1/2  walking vs. stopped — two cards or one",
    "17   THAT SCREAM WAS NOT HUMAN  (transcribed as 'screen')",
    "18   unclear — possibly WHO LET YOU IN",
    "21   WHICH EYE DO THEY SEE OUT OF  (transcribed as 'say')",
    "28   SOMETHING GOT IN WITHOUT KEYS",
    "38   SUBJECT UNAWARE / SUBJECT POSSESSED",
]
