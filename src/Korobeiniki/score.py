import utils as u
import consts as c

import scamp as sc
import scamp_extensions.pitch as pitch

import numpy as np

import copy

from fluid import FLUID

SCALE = pitch.Scale.from_pitches([60, 62, 64-1, 65, 67, 69-1, 71-1, 72])


TEMPO = 105

# ####START SCORES####


def set_insts():
    r3 = FLUID.sfload(
        str(c.FLUID_R3_GM/"FluidR3_GM.sf2")
    )

    dmg = FLUID.sfload(
        str(c.INST_ROOT/"DMG-CPU1.5/DMG-CPU1.5.SF2")
    )

    # 0	26	Jazz Guitar
    piano1 = (r3, 0, 26)

    # 0	30	FC Triangle
    piano2 = (dmg, 0, 30)

    FLUID.program_select(0, *piano2)


def melody(clock: sc.Clock, track: sc.ScampInstrument):
    props1 = None
    vol = 1.0

    scale = copy.deepcopy(SCALE)
    # scale = scale.transpose(12)

    dur1 = [1, 1/2, 1/2]

    melody1 = [
        [4, 1, 2],
        [3, 2, 1],
        [0, 0, 2],
        [4, 3, 2],
        [1, 1, 2]
    ]
    props2 = (sc.StartSlur(), sc.StopSlur(), None)

    dur2 = [1, 1]

    melody2 = [
        [3, 4],
        [2, 0],
        [0, None]
    ]

    melody3 = [
        [7, 6, 5],
        [4, 4, 2],
    ]

    dur3 = dur1

    def base1():

        for i, m in enumerate(melody1):
            u.play_score(track, m, dur1, scale, vol, props=tuple(
                [None] * (len(melody1)-1)) + props2)

        for i, m in enumerate(melody2):
            u.play_score(track, m, dur2, scale, vol, props=props1)

    def change():
        dur = [1/2, 1/2, 1/2, 1/2]

        melody = [None, 3, 3, 5]

        u.play_score(track, melody, dur, scale, vol,
                     props=(None, sc.StartSlur(), sc.StopSlur(), None))

    def base2():
        for i, m in enumerate(melody3):
            u.play_score(track, m, dur3, scale, vol,
                         props=tuple([None]*3)+props2)

        for i, m in enumerate(melody1[3:]):
            u.play_score(track, m, dur1, scale, vol, props=props1)

        for i, m in enumerate(melody2):
            u.play_score(track, m, dur2, scale, vol, props=props1)

    tempo = TEMPO

    for i in range(1, 4):
        for j in range(1, 3):
            print(clock.tempo)

            base1()
            change()
            base2()

            change()
            base2()

            # scale.transpose(1)

            # change()
            # base2()

            scale.transpose(1)
            tempo += 5 * j
            clock.tempo = tempo

        scale.transpose(1)

        tempo += 5 * i * 2
        clock.tempo = tempo

    u.rest(2)

    clock.kill()


def scores(session: sc.Session):
    out = c.MIDI_PORT_NAME
    piano1 = session.new_midi_part(
        "piano", out, start_channel=0
    )

    session.fork(melody, args=[piano1], initial_tempo=TEMPO)

# ####END SCORES####
