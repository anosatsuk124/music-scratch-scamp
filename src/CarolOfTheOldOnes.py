import scamp as sc
import scamp_extensions.pitch as pitch

import copy
import typing as t

SCALE = pitch.Scale.major(60)
SCALE = SCALE.transpose(12)

Score = list[t.Union[float, list[float]]]

s = sc.Session()
# s.fast_forward_to_beat(100)
# s.tempo = 150


def to_pitch(score: Score, scale: pitch.Scale) -> Score:
    """
    Converts a list of degrees to a list of pitches
    """

    pitch_list = []

    for el in score:
        if isinstance(el, list):
            pitch_list.append([scale.degree_to_pitch(p) for p in el])
        else:
            pitch_list.append(scale.degree_to_pitch(el))

    return pitch_list


def play_score(track: sc.ScampInstrument, score: Score, dur: list[float], scale: pitch.Scale = SCALE, vol: float = 0.8, props: sc.NoteProperties = None):
    count = 0
    for note in to_pitch(score, scale):
        # Same to: piano1.play_note(to_pitch(score)[i], vol, dur[i])
        if isinstance(note, list):
            track.play_chord(note, volume=vol,
                             length=dur[count], properties=props)
        else:
            track.play_note(note, volume=vol,
                            length=dur[count], properties=props)

        count += 1


def melody(clock: sc.Clock, track,):
    # props = "length * 1.25"
    props = None

    scale = copy.deepcopy(SCALE)
    melody1 = [0, -1, 0, -2]
    melody2 = [el+2 for el in melody1]
    dur = [1, 1/2, 1/2, 1]
    for i in range(16):
        play_score(track, melody1, dur, scale, props=props)
    for i in range(4):
        play_score(track, melody2, dur, scale, props=props)


def song(clock: sc.Clock, track: sc.ScampInstrument):
    # props = "length * 1"
    props = None

    scale = copy.deepcopy(SCALE)

    melody1 = [0, 0, -1, 0, -2]
    melody2 = [el+2 for el in melody1]
    dur = [1/2, 1/2, 1/2, 1/2, 1]
    for i in range(16):
        play_score(track, melody1, dur, scale, props=props)
    for i in range(4):
        play_score(track, melody2, dur, scale, props=props)


def acommpany(clock: sc.Clock, track):
    scale = copy.deepcopy(SCALE)  # scale.transpose(12)

    # props = "length * 1.5"
    props = None

    ac1 = [-2, -3, -4, -5]

    ac2 = [[]]

    dur = [3 for _ in range(4)]

    for _ in range(4):
        clock.wait(3)  # Wait 3 beats
    for i in range(2):
        play_score(track, [n-i for n in ac1], dur, scale, props=props)


def main():
    s.tempo = 160
    piano = s.new_part("song", preset="piano")
    harp = s.new_part("harp")
    organ1 = s.new_part("organ")

    s.wait(3)
    s.fork(acommpany, args=[organ1])
    s.fork(melody, args=[harp])
    s.fork(song, args=[piano])


def show_score():
    main()
    s.start_transcribing()
    s.wait_for_children_to_finish()
    performance = s.stop_transcribing()
    score = performance.to_score(
        title="Carol of the Old Ones (Japanese version)",
        composer="",
        time_signature=["3/4"]
    )
    score.show()
    performance.export_to_midi_file("CarolOfTheOldOnes.midi")
    score.export_music_xml("CarolOfTheOldOnes.musicxml")


show_score()


def play_repeatly():
    while True:
        main()
        s.wait_for_children_to_finish()


s.print_default_soundfont_presets()

# play_repeatly()
