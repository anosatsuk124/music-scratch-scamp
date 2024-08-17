from consts import ROOT
import os
import subprocess

for path, _, files in os.walk(ROOT):
    for file in files:
        if file.endswith(".sfz"):
            pathSfz = os.path.join(path, file)
            subprocess.run(["polyphone", "-1", pathSfz])
