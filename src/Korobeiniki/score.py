import utils as u
import consts as c

import scamp as sc
import scamp_extensions.pitch as pitch

import numpy as np

import copy

from fluid import FLUID

SCALE = pitch.Scale.from_pitches([60, 62, 64-1, 65, 67, 69-1, 71-1, 72])


TEMPO = 112

# ####START SCORES####


def set_insts():
    r3 = FLUID.sfload(
        str(c.FLUID_R3_GM/"FluidR3_GM.sf2")
    )

    dmg = FLUID.sfload(
        str(c.INST_ROOT/"DMG-CPU1.5/DMG-CPU1.5.SF2")
    )

    # r3 0	26	Jazz Guitar

    # 0	30	FC Triangle
    piano1 = (dmg, 0, 30)

    piano3 = (dmg, 0, 35)

    piano2 = (dmg, 0, 43)

    FLUID.program_select(0, *piano1)
    FLUID.program_select(1, *piano3)
    FLUID.program_select(2, *piano2)


def melody(clock: sc.Clock, track1: sc.ScampInstrument, track2: sc.ScampInstrument, track3: sc.ScampInstrument):
    props1 = None

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

    def base1(track, scale, vol):
        for i, m in enumerate(melody1):
            u.play_score(track, m, dur1, scale, vol, props=tuple(
                [None] * (len(melody1)-1)) + props2)

        for i, m in enumerate(melody2):
            u.play_score(track, m, dur2, scale, vol, props=props1)

    def change(track, scale, vol):
        dur = [1/2, 1/2, 1/2, 1/2]

        melody = [None, 3, 3, 5]

        u.play_score(track, melody, dur, scale, vol,
                     props=(None, sc.StartSlur(), sc.StopSlur(), None))

    def base2(track, scale, vol):
        for i, m in enumerate(melody3):
            u.play_score(track, m, dur3, scale, vol,
                         props=tuple([None]*3)+props2)

        for i, m in enumerate(melody1[3:]):
            u.play_score(track, m, dur1, scale, vol, props=props1)

        for i, m in enumerate(melody2):
            u.play_score(track, m, dur2, scale, vol, props=props1)

    def master_palay(count: int, vol: float, scale, trans, ratio):
        tempo = TEMPO
        args = (track1, scale, vol)

        for i in range(count):
            print(clock.tempo)

            base1(*args)
            change(*args)
            base2(*args)

            scale.transpose(trans)

            change(*args)
            base2(*args)

            tempo += ratio * (i+1) * 2
            clock.tempo = tempo
        scale.transpose(trans)

    def trackN_play(track, count: int, vol: float, scale, trans):
        args = (track, scale, vol)

        for i in range(count):
            base1(*args)
            change(*args)
            base2(*args)

            scale.transpose(trans)

            change(*args)
            base2(*args)
        scale.transpose(trans)

    def once(track, vol, scale, trans):
        args = (track, scale, vol)
        base1(*args)
        change(*args)
        base2(*args)

        scale.transpose(trans)

        change(*args)
        base2(*args)

        scale.transpose(trans)

    scale1 = copy.deepcopy(SCALE)

    vol1 = 0.8

    print("start1")
    clock.fork(once, args=[track1, vol1, scale1, 1])
    clock.wait_for_children_to_finish()

    scale1 = copy.deepcopy(SCALE)

    scale2 = copy.deepcopy(scale1)

    scale2.transpose(12)
#
    vol2 = vol1 - 0.1
#     print("start2")
#     clock.fork(master_palay, args=[2, vol1, scale1, 1, 5])
#     clock.fork(trackN_play, args=[track3, 2, vol2, scale2, 1])
#     clock.wait_for_children_to_finish()

    # scale3.transpose(12)

    print("start3")
    # vol3 = vol2 - 0.1

    vol3 = vol2 - 0.3
    clock.fork(master_palay, args=[1, vol1, scale1, -1, 0.55])
    clock.fork(trackN_play, args=[track2, 1, vol2, scale2, -1])
    # clock.fork(trackN_play, args=[track3, 1, vol3, scale3, -1])
    clock.wait_for_children_to_finish()

    scale3 = copy.deepcopy(scale1)
    scale3.transpose(12)

    print("start4")
    clock.fork(once, args=[track1, vol1, scale1, 2])
    clock.fork(once, args=[track2, vol2, scale2, 2])
    clock.fork(once, args=[track3, vol3, scale3, 2])
    clock.wait_for_children_to_finish()

    print("start5")
    clock.fork(master_palay, args=[2, vol1, scale1, 1, 11])
    clock.fork(trackN_play, args=[track2, 2, vol2, scale2, 1])
    clock.fork(trackN_play, args=[track3, 2, vol3, scale3, 1])
    clock.wait_for_children_to_finish()

    u.rest(2)

    clock.kill()


def scores(session: sc.Session):
    out = c.MIDI_PORT_NAME
    piano1 = session.new_midi_part(
        "piano", out, start_channel=0
    )
    piano2 = session.new_midi_part(
        "piano", out, start_channel=1
    )
    piano3 = session.new_midi_part(
        "piano", out, start_channel=2
    )

    session.fork(melody, args=[piano1, piano2, piano3], initial_tempo=TEMPO)

# ####END SCORES####
