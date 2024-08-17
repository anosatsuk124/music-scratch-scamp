import utils as u
import consts as c

import scamp as sc
import scamp_extensions.pitch as pitch

import numpy as np

import copy

from fluid import FLUID

SCALE = pitch.Scale.major(60)
SCALE = SCALE.transpose(12)

TEMPO = 165

# ####START SCORES####


def set_insts():
    r3 = FLUID.sfload(
        str(c.FLUID_R3_GM/"FluidR3_GM.sf2")
    )

    #    8	6	Coupled Harpsichord
    chord = (r3, 8, 6)

    FLUID.program_select(0, *chord)


def melody(clock: sc.Clock, track):
    vol = 0.3

    scale = copy.deepcopy(SCALE)

    dur = [1, 1/2, 1/2, 1/2, 1/2]

    u.play_score(track, [5, 5, 5, 4, 3], dur, scale, vol=vol)
    u.play_score(track, [2, 2, 2, 1, 0], dur, scale, vol=vol)
    u.play_score(track, [1, 1, 1, 2, 1], dur, scale, vol=vol)
    u.play_score(track, [0, -2, -2, -2], dur, scale, vol=vol)

    u.rest(4)

    clock.kill()


def scores(session: sc.Session):
    out = c.MIDI_PORT_NAME
    piano1 = session.new_midi_part(
        "piano", out, start_channel=0)

    session.fork(melody, args=[piano1])

# ####END SCORES####
