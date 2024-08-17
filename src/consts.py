from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

ROOT = (Path(__file__).parent.parent).resolve()

INST_ROOT = Path(os.getenv("INST_ROOT")).resolve()
VP_ORCHESTRA = INST_ROOT/"Virtual-Playing-Orchestra3"
FLUID_R3_GM = INST_ROOT/"FluidR3_GM"

MIDI_PORT_NAME = "FLUIDSYNTH"

SAMPLE_RATE = float(os.getenv("SAMPLE_RATE"))
GAIN = float(os.getenv("GAIN"))
