import utils as u
import scamp as sc
import scamp_extensions.pitch as pitch

import copy

SCALE = pitch.Scale.major(60)
SCALE = SCALE.transpose(12)


def melody(clock: sc.Clock, track, props: sc.NoteProperties):
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


def main(session: sc.Session):
    session.tempo = 140

    piano = session.new_part("piano", preset="piano")

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
