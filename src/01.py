import scamp as sc
import scamp_extensions.pitch as pitch

s = sc.Session(tempo=140)
# s.tempo = 150

# s.print_default_soundfont_presets()

violin = s.new_part("violin")
cello = s.new_part("cello")
piano1 = s.new_part("Piano")

# 60 is the MIDI note number for middle C (C4)
c4_major = pitch.Scale.major(60)

SCALE = pitch.Scale.major(60)


def to_pitch(list: list[float]) -> list[float]:
    """
    Converts a list of degrees to a list of pitches
    """
    return [SCALE.degree_to_pitch(p) for p in list]


melody = [0, -1, 0, -2]
dur = [1, 1/2, 1/2, 1]

# print(to_pitch(melody))
# Out: [60.0, 59.0, 60.0, 57.0]

# SCALE = pitch.Scale.major(50)
# print(to_pitch(melody))
# Out: [50.0, 49.0, 50.0, 47.0]


def play_bar(melody: list[float], dur: list[float], vol: float = 0.8):
    for i in range(len(melody)):
        # Same to: piano1.play_note(to_pitch(melody)[i], vol, dur[i])
        piano1.play_note(to_pitch(melody)[i], volume=vol, length=dur[i])


def main():
    melody = [0, -1, 0, -2]
    dur = [1, 1/2, 1/2, 1]
    for i in range(16):
        play_bar(melody, dur)


s.print_default_soundfont_presets()

main()
