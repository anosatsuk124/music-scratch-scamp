import utils as u
import consts as c

import scamp as sc
import scamp_extensions.pitch as pitch

import numpy as np

import copy

from fluid import FLUID


SESSION = sc.Session()

SCALE = pitch.Scale.major(60)
SCALE = SCALE.transpose(12)

TEMPO = 165


def set_insts():
    vp_violin = FLUID.sfload(
        str(c.VP_ORCHESTRA/"Strings/1st-violin-SOLO-KS-C2.sf2")
    )

    vp_harp = FLUID.sfload(
        str(c.VP_ORCHESTRA/"Strings/harp-KS-C0.sf2")
    )

    r3 = FLUID.sfload(
        str(c.FLUID_R3_GM/"FluidR3_GM.sf2")
    )

    # harp = (vp_harp, 0, 0)
    # 0	46	Harp
    harp = (r3, 0, 46)

    organ = (r3, 8, 19)
    # 0	40	Violin
    violin = (r3, 0, 40)

    FLUID.program_select(0, *harp)
    FLUID.program_select(1, *organ)
    FLUID.program_select(2, *violin)


def melody(clock: sc.Clock, track):
    # props = "length * 1.25"
    props = None

    vol = 0.32

    scale = copy.deepcopy(SCALE)
    melody1 = [0, -1, 0, -2]
    melody2 = [el+2 for el in melody1]
    dur = [1, 1/2, 1/2, 1]

    for _ in range(16):
        u.play_score(track, melody1, dur, scale, props=props, vol=vol)
    for _ in range(4):
        u.play_score(track, melody2, dur, scale, props=props, vol=vol)

    dur = [1, 1/2, 1/2, 1/2, 1/2]

    u.play_score(track, [5, 5, 5, 4, 3], dur, scale, vol=vol)
    u.play_score(track, [2, 2, 2, 1, 0], dur, scale, vol=vol)
    u.play_score(track, [1, 1, 1, 2, 1], dur, scale, vol=vol)
    u.play_score(track, [0, -2, -2, -2], dur, scale, vol=vol)

    u.rest(3)

    clock.kill()


def violin(clock: sc.Clock, track: sc.ScampInstrument):
    scale = copy.deepcopy(SCALE)

    vol = 0.3

    melody1 = [0, 0, -1, 0, -2]
    melody2 = [el+2 for el in melody1]
    dur = [1/2, 1/2, 1/2, 1/2, 1]
    for _ in range(12):
        u.play_score(track, melody1, dur, scale, vol=vol)

    vol2 = vol-0.05
    vols = np.linspace(vol, vol2, 4)

    for i in range(4):
        v = vols[i]
        print(v)

        u.play_score(track, melody1, dur, scale, vol=v,
                     props={
                         "articulation": "staccato",
                     })

    vol3 = vol2+0.2

    vols = np.linspace(vol2, vol3, 4)

    for i in range(4):
        v = vols[i]
        print(v)

        u.play_score(track, melody2, dur, scale, props={
            "articulation": "staccato",
        }, vol=v)

    vol = vol3

    dur = [1, 1/2, 1/2, 1/2, 1/2]

    u.play_score(track, [5, 5, 5, 4, 3], dur, scale, vol=vol)
    u.play_score(track, [2, 2, 2, 1, 0], dur, scale, vol=vol)
    u.play_score(track, [1, 1, 1, 2, 1], dur, scale, vol=vol)
    u.play_score(track, [0, -2, -2, -2], dur, scale, vol=vol)

    u.rest(3)

    clock.kill()


def song(clock: sc.Clock, track: sc.ScampInstrument):
    violin(clock, track)


def acommpany(clock: sc.Clock, track):
    scale = copy.deepcopy(SCALE)  # scale.transpose(12)

    vol = 0.3

    props = None
    props = f"length * {1 + 1 / 8}"

    ac1 = [-2, -3, -4, -5]

    ac2 = [[]]

    dur = [3 for _ in range(4)]

    for _ in range(4):
        u.rest(3)
    for i in range(2):
        u.play_score(track, [n-i for n in ac1], dur,
                     scale, props=props, vol=vol)

    u.rest(3*4)
    clock.kill()


def scores(session: sc.Session):
    out = c.MIDI_PORT_NAME
    harp1 = session.new_midi_part(
        "harp", out, start_channel=0)
    organ1 = session.new_midi_part("organ", out, start_channel=1)
    violin1 = session.new_midi_part("violin", out, start_channel=2)
    song1 = session.new_midi_part("song", out, start_channel=3)

    session.fork(acommpany, args=[organ1])
    session.fork(violin, args=[violin1])
    session.fork(melody, args=[harp1])
    session.fork(song, args=[song1])


def create_performance() -> sc.Performance:
    session = sc.Session(TEMPO)

    scores(session)

    session.start_transcribing()
    session.fast_forward()

    try:
        session.wait_for_children_to_finish()
    finally:
        session.kill()

    return session.stop_transcribing()


def show_score():
    performance = create_performance()

    score = performance.to_score(
        title="Carol of the Old Ones (Japanese version)",
        composer="",
        time_signature=["3/4"]
    )
    score.show()


def export_score(path: str):
    performance = create_performance()
    score = performance.to_score(
        title="Carol of the Old Ones (Japanese version)",
        composer="",
        time_signature=["3/4"]
    )

    performance.export_to_midi_file(path + ".midi")
    score.export_music_xml(path + ".musicxml")


def play_midi(seek=0, wait=False):
    global SESSION
    SESSION = sc.Session(TEMPO)
    # Seek to the beginning of the session
    SESSION.fast_forward_to_time(seek)

    if wait:
        SESSION.wait(3)

    scores(SESSION)
    try:
        SESSION.wait_for_children_to_finish()
    finally:
        SESSION.kill()


def force_stop():
    global SESSION
    SESSION.kill()


# s.print_default_soundfont_presets()

# show_score()

# play_repeatly()
# play()
