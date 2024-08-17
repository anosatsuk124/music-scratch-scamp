from score import play_midi, set_insts

from fluid import FLUID
import sys

set_insts()

FLUID.start()

seek = float(sys.argv[1] if len(sys.argv) > 1 else 0)
play_midi(seek)

FLUID.delete()
