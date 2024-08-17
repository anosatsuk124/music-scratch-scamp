from main import play_midi

from fluid import FLUID
import sys

FLUID.start()

seek = float(sys.argv[1] if len(sys.argv) > 1 else 0)
seek_method = sys.argv[2] if len(sys.argv) > 2 else "seconds"
play_midi(seek, seek_method)

FLUID.delete()
