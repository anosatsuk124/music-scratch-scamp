from main import play_midi

from fluid import FLUID
import sys

FLUID.start()

seek = float(sys.argv[1] if len(sys.argv) > 1 else 0)
play_midi(seek)

FLUID.delete()
