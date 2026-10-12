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
    (["You have stopped", "walking"], "dread",
     "Only true of someone who stopped to read it, which is everyone "
     "who reads it. The tape appears to have noticed.", "med"),
    (["You have not stopped", "walking"], "curt",
     "The other half. Catches the ones still moving, who get it "
     "over their shoulder.", "med"),
    (["Dont scream"], "scream",
     "Shouted in the largest type on the tape, under a second. The form "
     "contradicts the instruction, which is the joke.", "med"),
    (["You have attracted", "the attention of", "something truly evil"], "dread",
     "Long read, and the reader spends all of it being looked at. "
     "Theatrical enough to stay fiction.", "med"),
    (["Remember to", "look behind you"], "curt",
     "Remember implies they were told before. Most will turn.", "med"),
    (["Dont make", "eye contact"], "curt",
     "Never says with what. The street supplies candidates.", "med"),
    (["Start walking through them"], "curt",
     "An instruction, and deliberately unclear what 'them' is — the crowd, "
     "or what is standing in it. Reads as a dare.", "med"),
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
    (["Hell was full", "so I came back"], "curt",
     "The dead returning with swagger rather than sorrow. Sits well "
     "against the cards that miss someone.", "low"),
    (["I waited all year", "for tonight"], "dread",
     "Opens the reel. Establishes that the speaker has been counting.", "low"),
    (["I only get", "until morning"], "dread",
     "Puts a clock on everything else the reel says.", "low"),
    (["Do you still live", "I cant tell tonight"], "question",
     "Live as in reside, or live as in alive. The speaker genuinely "
     "cannot tell, which is worse than a threat.", "med"),
    (["I went back", "but you had moved on"], "dread",
     "Moved house, moved on. Does more work than the line it replaced.", "low"),
    (["They are not haunting you", "They are visiting"], "curt",
     "Corrects the reader's assumption. Reframes the entire reel.", "low"),
    (["Thank you for", "leaving the light off"], "dread",
     "Gratitude for the wrong thing. The off is what makes it land.", "med"),
    (["Next year", "I may not find you"], "dread",
     "The loss is the speaker's, not the reader's. Rare on a horror tape.", "low"),
    (["You stopped", "talking about me"], "dread",
     "An accusation made of grief. The heaviest card in the reel.", "med"),
    (["The costumes help"], "curt",
     "Four words explaining how the dead are on the street at all tonight. "
     "Makes the rest of the tape cohere.", "low"),
    (["They tried to hold", "your hand"], "dread",
     "Past tense, and the reader starts remembering.", "low"),
    (["You felt it", "You said it was the cold"], "dread",
     "Supplies the memory and the excuse the reader already used.", "low"),
    (["You have never", "looked up before"], "dread",
     "Literally true of anyone reading a projection on a building.", "med"),
    (["Do not be frightened", "It is only for tonight"], "curt",
     "The first card on the tape trying to be kind, and failing "
     "in an interesting direction.", "low"),
    (["Take them home", "with you"], "curt",
     "An invitation rather than a threat, which makes it worse.", "med"),
    (["Are your emotions", "strong enough", "when your body is gone"], "question",
     "Asks what survives. The reel's whole premise put as a question "
     "rather than a claim.", "low"),
    (["Ignore this if", "you are living"], "curt",
     "A polite exclusion. Setup — the beat before the payoff is what "
     "makes the payoff work.", "low"),
    (["Sorry if you are", "finding out you are not"], "dread",
     "The apology is the horror. Best card on the tape.", "med"),
    (["Sorry if you", "dont remember"], "dread",
     "Reads two ways and needs neither resolved: sorry you have "
     "forgotten whoever is speaking, or sorry you have forgotten what "
     "happened to you. Echoes the apology above without repeating it.", "low"),
    (["Dont look at me"], "dread",
     "Shame rather than threat. The speaker does not want to be seen "
     "in whatever state it is in.", "low"),
    (["Im sorry", "the warning came", "too late"], "dread",
     "An apology for a warning the reader never received, about "
     "something already done.", "med"),
    (["I didnt have a better", "way of contacting you"], "curt",
     "Explains why any of this is on a building at all. Setup.", "low"),
    (["Thank you for", "your messages"], "dread",
     "Payoff. Implies the reader has been answering, which they have "
     "been doing silently all night.", "med"),
    (["One night is not", "very long"], "dread",
     "Closes the reel. Resignation rather than menace.", "low"),
]

# --------------------------------------------------------------------------
# Tonight. The street as it actually is on the night — costumes, doors, sweets,
# things handed over. These only work on the date they are projected.
TONIGHT = [
    (["Not all need", "costumes tonight"], "dread",
     "Reads the crowd back to itself. Everyone checks everyone.", "low"),
    (["Someone unseen", "is trying to get", "your attention"], "dread",
     "Long read, and the reader spends all of it looking around.", "med"),
    (["Check under the mask", "Not all have faces"], "dread",
     "Specific instruction with a horrible second clause.", "med"),
    (["It is not a mask"], "scream",
     "Four words, large, under a second. Strongest short card kept.", "med"),
    (["The sweets are fine", "The house is not"], "curt",
     "Reassures and withdraws it in the same breath.", "low"),
    (["Nobody lives there", "anymore"], "dread",
     "The anymore is doing everything.", "low"),
    (["That is definitely", "a cursed object"], "curt",
     "Casual about the supernatural. Light relief that is still on theme.", "low"),
    (["I hope you have pockets", "Some creatures need rides"], "curt",
     "Charming and slightly wrong. Nothing else on the tape sounds like it.", "low"),
    (["Some tricks", "involve sorcery"], "curt",
     "Plays the night's own vocabulary straight.", "low"),
    (["A knock at the door"], "dread",
     "The author's own two-word horror story. Works at every door on "
     "the street at once, and needs nothing after it.", "low"),
    (["Behind the door", "they wait"], "dread",
     "Works at every door on the street at once.", "low"),
    (["It is wearing", "a costume too"], "dread",
     "Turns every costume in view into a question.", "med"),
    (["Too many to count"], "curt",
     "Answers a question the tape never asked.", "low"),
    (["Count again"], "curt",
     "Best placed after the card above. Refuses to say what changed.", "low"),
    (["Goodbye"], "scream",
     "One word, large. Reads as the tape ending, which it is not.", "low"),
    (["Almost morning"], "curt",
     "True by the end of the night. The tape appears to know the hour.", "low"),
    (["Not yet"], "curt",
     "Answers the card above, or nothing at all.", "low"),
    (["I see this year", "you chose transparent"], "curt",
     "A compliment on a costume nobody is wearing.", "low"),
    (["It is the only night", "nobody questions", "appearances"], "dread",
     "States the night's one rule, and why the dead can use it.", "low"),
    (["The house with", "no lights on"], "curt",
     "Every street has one. Everyone looks for it.", "low"),
    (["Something else moves"], "dread",
     "Follows the card above without naming what or where.", "low"),
    (["How many houses", "wont you see tomorrow"], "question",
     "Reframes an ordinary street as temporary.", "med"),
    (["Question everything", "tonight"], "curt",
     "Instruction the reader can safely follow. Low risk, real effect.", "low"),
    (["It is still waiting"], "dread",
     "No subject, no object. The reader fills both in.", "low"),
    (["The street is", "longer tonight"], "dread",
     "Doubt cast on the walk home itself.", "low"),
    (["Have you learnt", "how they hide"], "question",
     "Assumes the reader has been studying. Some will feel caught.", "med"),
    (["That scream was", "not human"], "dread",
     "Reclassifies whatever the street just heard. On a loud night "
     "there is always something to attach it to.", "med"),
    (["Which eye do they", "see out of"], "question",
     "Assumes more than two. Worst question on the tape to be asked "
     "while looking at a mask.", "med"),
    (["Something got in", "without keys"], "dread",
     "Past tense and already finished. Nothing to do about it.", "med"),
    (["Do you know ghouls", "give out candy too"], "curt",
     "Reframes every door already knocked on tonight.", "low"),
    (["Not all doors", "can be opened", "by the possessed"], "dread",
     "Sounds like reassurance. Means some doors can, and does not say "
     "which.", "low"),
    (["Even the darkness", "is alive tonight"], "dread",
     "States the night's condition rather than threatening anyone.", "low"),
    (["Something isnt right"], "dread",
     "Names the feeling the whole tape is building without pointing "
     "at a cause.", "low"),
    (["Then the sky blinked"], "dread",
     "Past tense, enormous, and never explained. Nothing else on the "
     "tape is this large.", "low"),
    (["This is the day", "reality resets"], "dread",
     "Gives the night a mechanism. Reads as folklore rather than threat.", "low"),
    (["Sleep with", "one eye open"], "curt",
     "An old saying delivered as instruction.", "med"),
    (["Dont be afraid", "some people see them", "all the time"], "dread",
     "Comfort that makes it worse. The reel's best reassurance.", "low"),
    (["The trees are watching"], "dread",
     "Works on any street with a tree on it, which is this one.", "low"),
    (["Watch the shadows"], "scream",
     "Three words, large. Instruction and warning at once.", "med"),
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
    (["Who let you out"], "dread",
     "Three words that retroactively put the reader somewhere they were "
     "being kept. Nothing else on the tape implies containment.", "med"),
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
    (["BODIES 7", "COSTUMES 8"], "glitch",
     "Two numbers that should match. The whole card is the gap.", "low"),
    (["DOORBELL ACTIVITY", "AT VACANT ADDRESS"], "glitch",
     "Something is knocking at a house with nobody in it.", "low"),
    (["SUGAR LEVELS NOMINAL", "SOUL COUNT LOW"], "glitch",
     "Bureaucratic bathos. Funny first, then not.", "low"),
    (["CURFEW LIFTED", "FOR THE DECEASED"], "glitch",
     "Explains the night as policy, which is funnier and colder than magic.", "low"),
    (["MASK DETECTED", "FACE NOT DETECTED"], "glitch",
     "The machine looking at the crowd and failing. Best status card kept.", "med"),
    (["SUBJECT UNAWARE", "SUBJECT POSSESSED"], "glitch",
     "Two readings of the same person, filed without comment.", "med"),
    (["WELCOME VISITORS"], "ident",
     "Hospitable, placed among cards that are not. Works as an opener.", "low"),
]

# --------------------------------------------------------------------------
# Inside. The tape stops addressing the reader and starts claiming to be them.
# A page of text is already being read in the reader's own voice, so these are
# the only cards that are literally true while they are on screen.
INSIDE = [
    (["The voice in your head", "knows me"], "dread",
     "The author's line and the best idea in this reel. True while it is read, "
     "which is what makes it work.", "med"),
    (["Are you in control"], "question",
     "Three words. Opens the whole register without explaining it.", "med"),
    (["Do you hear them", "in your ear"], "question",
     "Sends people listening to their own head rather than the street.", "med"),
    (["So what do you feel"], "question",
     "Asked flatly, like a form. The gap between the question and the tone "
     "is the unpleasant part.", "low"),
    (["You are trapped"], "dread",
     "Long hold on three words. Abstract enough to read as fiction, "
     "heavy enough to sit badly.", "med"),
    (["That thought", "was not yours"], "dread",
     "Lands on whatever the reader was already thinking. Never misses.", "med"),
    (["Who are you", "reading this to"], "question",
     "Assumes the reader is reading aloud to someone. Many are.", "med"),
    (["You are saying these", "in my voice"], "dread",
     "The trick only projected text can do. True as it is read.", "med"),
    (["Stop reading", "This message is not", "for the living"], "dread",
     "Excludes the reader from the living by implication. "
     "Best card in the reel.", "med"),
    (["I chose the words", "You chose to hear them"], "dread",
     "Splits the blame. Makes the reader complicit in their own scare.", "low"),
    (["We have been talking", "for a while now"], "curt",
     "Rewrites the last few minutes as a conversation.", "med"),
    (["Do you argue with it"], "question",
     "Takes for granted that there is something to argue with.", "med"),
    (["WARNING", "IT USES YOUR VOICE", "SO THAT YOU OBEY"], "glitch",
     "The machine warning the reader about itself, in the machine's own "
     "register. Explains the whole reel.", "med"),
    (["Dont create monsters"], "dread",
     "The only card that warns the reader about themselves. Reads as "
     "advice, a rule, or an accusation depending on who catches it.", "low"),
    (["Its okay", "its still a secret"], "curt",
     "Conspiratorial. Assumes a secret the reader does not know they "
     "are keeping.", "low"),
    (["You arent dreaming"], "curt",
     "Deliberately unpaired from the card below. The shuffle keeps them "
     "minutes apart so the contradiction is something the reader "
     "notices themselves, later.", "low"),
    (["You are dreaming"], "dread",
     "The other half, arriving long after the first is half forgotten.", "med"),
    (["(Screaming internally)"], "curt",
     "The joke version of every other card in this reel. Lands as relief, "
     "then as recognition.", "low"),
]

# --------------------------------------------------------------------------
# The wrong voice. Cards the machine should not be able to produce: posters,
# captions, the register of a motivational feed. Scarcity is the whole effect —
# a few across an hour read as something else using the tape, a run of them
# reads as a joke account. The composition keeps them far apart.
WRONG = [
    (["Hungry dogs", "are never loyal"], "dread",
     "A proverb on an interrogation tape. Sounds like advice and is not.", "low"),
    (["You vs you", "Remember that"], "curt",
     "Gym poster. Harmless alone, strange here, which is the point.", "low"),
    (["No shortcuts"], "curt",
     "Two words of someone else's motivation, delivered by something "
     "with no interest in motivating anyone.", "low"),
    (["Chill", "Its only chaos here"], "curt",
     "The tape being reassuring, badly.", "low"),
    (["Sleep like the dead"], "curt",
     "A saying that stops being a saying on this tape.", "low"),
    (["Smile", "Its good for stress"], "curt",
     "Wellness advice from something with teeth. Pairs with the grins.", "low"),
    (["Live laugh", "Leave"], "curt",
     "Three words of wall art, one word wrong.", "low"),
    (["Hang in there"], "curt",
     "Encouragement with nothing behind it.", "low"),
    (["Rise", "Some of us cannot"], "curt",
     "Starts as a slogan and finishes as a complaint from the ground.", "low"),
    (["No notes", "just markings on stones"], "curt",
     "A review turning into a graveyard. Best line in the reel.", "low"),
    (["( Awkward silence )"], "ident",
     "Stage direction as furniture, like the dramatic pause.", "low"),
    (["( Someone coughs )"], "ident",
     "Implies an audience in the room with the tape.", "low"),
    (["( Dramatic pause )"], "ident",
     "Stage direction as furniture. Works best where an ident would go.", "low"),
    (["Tell your cat", "I said pspspsps"], "curt",
     "The furthest from the tape's voice and the biggest laugh. "
     "One appearance an hour is plenty.", "low"),
]

APPROVED = {
    "STREET": STREET,
    "RETURNED": RETURNED,
    "TONIGHT": TONIGHT,
    "INSIDE": INSIDE,
    "FILE": FILE,
    "SYSTEM": SYSTEM,
    "WRONG": WRONG,
}

# --------------------------------------------------------------------------
# Held back pending the author's wording. The voice transcription was unclear
# and these are not mine to guess at — see the questions put to them. Nothing
# here renders.
PENDING = [
    "'Who are the same way homeless normal or they will get lost' — cannot parse",
]
