from CarolOfTheOldOnes import play_midi, export_score, set_insts

from fluid import FLUID

import consts as c
import sys
from pathlib import Path

OUTPUT_FILE_NAME = str((
    Path(sys.argv[1]) if len(sys.argv) > 1 else c.ROOT/"output")
    .resolve()
)

export_score(OUTPUT_FILE_NAME)

set_insts()

FLUID.setting("audio.file.name", OUTPUT_FILE_NAME+".wav")
FLUID.start(driver="file")

play_midi(wait=True)

FLUID.delete()