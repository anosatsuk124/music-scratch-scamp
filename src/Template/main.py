import scamp as sc
import scamp_extensions.pitch as pitch
import typing as t

from score import TEMPO, scores, set_insts

SESSION = sc.Session()


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


def export_score(
    path: str,
    title: str = "", composer: str = "",
    time_singature: list[str] = ["4/4"]
):
    performance = create_performance()
    score = performance.to_score(
        title=title,
        composer=composer,
        time_signature=time_singature
    )

    performance.export_to_midi_file(path + ".midi")
    score.export_music_xml(path + ".musicxml")


def play_midi(
    seek=0,
    seek_method: t.Literal["seconds", "beets"] = "seconds",
    wait=False
):
    set_insts()

    global SESSION
    SESSION = sc.Session(TEMPO)
    # Seek to the beginning of the session
    if seek_method == "beets":
        SESSION.fast_forward_in_beats(seek)
    else:
        SESSION.fast_forward_in_time(seek)

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
