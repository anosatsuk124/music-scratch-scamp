import scamp as sc
import scamp_extensions.pitch as pitch

import typing as t

SCALE = pitch.Scale.major(60)
SCALE = SCALE.transpose(12)

Score = list[t.Union[t.Optional[float], list[float]]]

# s.fast_forward_to_beat(100)
# s.tempo = 150


def rest(n: int):
    sc.wait(1 * n)


def to_pitch(score: Score, scale: pitch.Scale) -> Score:
    """
    Converts a list of degrees to a list of pitches
    """

    pitch_list = []

    for el in score:
        if isinstance(el, list):
            pitch_list.append([scale.degree_to_pitch(p) for p in el])
        elif el is None:
            pitch_list.append(None)
        else:
            pitch_list.append(scale.degree_to_pitch(el))

    return pitch_list


def play_score(track: sc.ScampInstrument, score: Score, dur: list[float],
               scale: pitch.Scale = SCALE, vol: float = 0.8,
               props: t.Union[sc.NoteProperties,
                              tuple[sc.NoteProperties]] = None,
               ):
    """
    Play a score with a given duration and scale
    """
    for i, note in enumerate(to_pitch(score, scale)):
        if isinstance(props, tuple):
            props = props[i] if i < len(props) else None
        # Same to: piano1.play_note(to_pitch(score)[i], vol, dur[i])
        if isinstance(note, list):
            track.play_chord(note, volume=vol,
                             length=dur[i], properties=props)
        elif note is None:
            rest(dur[i])
        else:
            track.play_note(note, volume=vol,
                            length=dur[i], properties=props)
