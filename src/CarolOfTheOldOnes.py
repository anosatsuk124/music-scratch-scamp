import utils as u
import scamp as sc
import scamp_extensions.pitch as pitch

import numpy as np

import copy

SCALE = pitch.Scale.major(60)
SCALE = SCALE.transpose(12)

TEMPO = 160


def melody(clock: sc.Clock, track,):
    # props = "length * 1.25"
    props = None

    scale = copy.deepcopy(SCALE)
    melody1 = [0, -1, 0, -2]
    melody2 = [el+2 for el in melody1]
    dur = [1, 1/2, 1/2, 1]
    for _ in range(16):
        u.play_score(track, melody1, dur, scale, props=props)
    for _ in range(4):
        u.play_score(track, melody2, dur, scale, props=props)

    u.rest(3)

    clock.kill()


def song(clock: sc.Clock, track: sc.ScampInstrument):
    scale = copy.deepcopy(SCALE)

    melody1 = [0, 0, -1, 0, -2]
    melody2 = [el+2 for el in melody1]
    dur = [1/2, 1/2, 1/2, 1/2, 1]
    for _ in range(12):
        u.play_score(track, melody1, dur, scale, vol=0.2)

    vols = np.linspace(0.2, 0.4, 8)

    for i in range(4):
        v = vols[i]
        print(v)

        u.play_score(track, melody1, dur, scale, vol=v)

    vols = np.linspace(0.4, 0.7, 4)

    for i in range(4):
        v = vols[i]
        print(v)

        u.play_score(track, melody2, dur, scale, props={
            "articulation": "staccato",
        }, vol=v)

    u.rest(3)

    clock.kill()


def acommpany(clock: sc.Clock, track):
    scale = copy.deepcopy(SCALE)  # scale.transpose(12)

    props = None
    props = "length * 2.25"

    ac1 = [-2, -3, -4, -5]

    ac2 = [[]]

    dur = [3 for _ in range(4)]

    for _ in range(4):
        u.rest(3)
    for i in range(2):
        u.play_score(track, [n-i for n in ac1], dur, scale, props=props)

    u.rest(3*4)
    clock.kill()


def scores(session: sc.Session, parts: list[sc.ScampInstrument]):
    session.fork(acommpany, args=[parts[0]])
    session.fork(song, args=[parts[1]])
    session.fork(melody, args=[parts[2]])
    session.fork(song, args=[parts[3]])


def parts(session: sc.Session):
    song = session.new_part("song", preset="Piano Merlin")
    harp = session.new_part("harp", preset="Harp LP2")
    organ1 = session.new_part("organ", preset="Organ 1")
    violin = session.new_part("violin", preset="Violin LP3")

    return [organ1, violin, harp, song]


def create_performance() -> sc.Performance:
    session = sc.Session(TEMPO)

    part = parts(session)

    session.start_transcribing()
    session.fast_forward()

    scores(session, part)

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


def export_score():
    performance = create_performance()
    score = performance.to_score(
        title="Carol of the Old Ones (Japanese version)",
        composer="",
        time_signature=["3/4"]
    )

    performance.export_to_midi_file("CarolOfTheOldOnes.midi")
    score.export_music_xml("CarolOfTheOldOnes.musicxml")


def play():
    session = sc.Session(TEMPO)
    scores(session, parts(session))
    try:
        session.wait_for_children_to_finish()
    finally:
        session.kill()


def play_repeatly():
    while True:
        play()


# s.print_default_soundfont_presets()

# show_score()

# play_repeatly()
# play()
