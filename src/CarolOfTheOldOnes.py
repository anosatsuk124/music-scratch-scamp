import utils as u
import scamp as sc
import scamp_extensions.pitch as pitch

import copy
import typing as t

SCALE = pitch.Scale.major(60)
SCALE = SCALE.transpose(12)

Score = list[t.Union[float, list[float]]]

# s.fast_forward_to_beat(100)
# s.tempo = 150


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
    # props = "length * 1"
    props = None

    scale = copy.deepcopy(SCALE)

    melody1 = [0, 0, -1, 0, -2]
    melody2 = [el+2 for el in melody1]
    dur = [1/2, 1/2, 1/2, 1/2, 1]
    for _ in range(16):
        u.play_score(track, melody1, dur, scale, props=props)
    for _ in range(4):
        u.play_score(track, melody2, dur, scale, props=props)

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


def main(session: sc.Session):
    session.tempo = 160

    piano = session.new_part("song", preset="piano")
    harp = session.new_part("harp")
    organ1 = session.new_part("organ")
    cello = session.new_part("cello")

    session.fork(acommpany, args=[organ1])
    session.fork(acommpany, args=[cello])
    session.fork(melody, args=[harp])
    session.fork(song, args=[piano])

    try:
        session.wait_for_children_to_finish()
    finally:
        session.kill()


def show_score():
    session = sc.Session()
    session.fast_forward()

    main(session)

    performance = session.stop_transcribing()
    score = performance.to_score(
        title="Carol of the Old Ones (Japanese version)",
        composer="",
        time_signature=["3/4"]
    )
    score.show()
    performance.export_to_midi_file("CarolOfTheOldOnes.midi")
    score.export_music_xml("CarolOfTheOldOnes.musicxml")


def play():
    session = sc.Session()
    main(session)


def play_repeatly():
    while True:
        play()


# s.print_default_soundfont_presets()

# show_score()

# play_repeatly()
# play()
