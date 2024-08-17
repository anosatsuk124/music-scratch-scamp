import utils as u
import consts as c

import scamp as sc
import scamp_extensions.pitch as pitch

import numpy as np

import copy

from fluid import FLUID

SCALE = pitch.Scale.from_pitches([60, 62, 64-1, 65, 67, 69-1, 71-1, 72])


TEMPO = 130

# ####START SCORES####


def set_insts():
    r3 = FLUID.sfload(
        str(c.FLUID_R3_GM/"FluidR3_GM.sf2")
    )

    # 0	26	Jazz Guitar
    piano1 = (r3, 0, 26)

    FLUID.program_select(0, *piano1)


def melody(clock: sc.Clock, track: sc.ScampInstrument):
    props = None
    vol = 0.3

    scale = copy.deepcopy(SCALE)
    scale = scale.transpose(12)

    dur = [1, 1/2, 1/2]

    melody = [
        [4, 1, 2],
        [3, 2, 1],
        [0, 0, 2],
        [4, 3, 2],
    ]

    for i, m in enumerate(melody):
        u.play_score(track, m, dur, scale, vol, props=props)

    u.play_score(track, [1], [1], scale, vol, props=[sc.StartSlur()])
    u.play_score(track, [1], [1/2], scale, vol, props=[sc.StopSlur()])
    u.play_score(track, [2], [1/2], scale, vol)

    dur = [1, 1]

    melody = [
        [3, 4],
        [2, 0],
        [0, None]
    ]

    for i, m in enumerate(melody):
        u.play_score(track, m, dur, scale, vol, props=props)

    u.rest(2)

    clock.kill()


def scores(session: sc.Session):
    out = c.MIDI_PORT_NAME
    piano1 = session.new_midi_part(
        "piano", out, start_channel=0
    )

    session.fork(melody, args=[piano1])

# ####END SCORES####
