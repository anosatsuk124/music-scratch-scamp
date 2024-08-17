from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

ROOT = (Path(__file__).parent.parent).resolve()

INST_ROOT = Path(os.getenv("INST_ROOT")).resolve()
VP_ORCHESTRA = INST_ROOT/"Virtual-Playing-Orchestra3"
FLUID_R3_GM = INST_ROOT/"FluidR3_GM"

MIDI_PORT_NAME = os.getenv("MIDI_PORT_NAME") if os.getenv(
    "MIDI_PORT_NAME") else "FLUIDSYNTH"

SAMPLE_RATE = float(
    os.getenv("SAMPLE_RATE") if os.getenv("SAMPLE_RATE") else 44100
)
GAIN = float(
    os.getenv("GAIN") if os.getenv("GAIN") else 0.3
)
EXPORT_GAIN = float(
    os.getenv("EXPORT_GAIN") if os.getenv("EXPORT_GAIN") else 1.0
)
