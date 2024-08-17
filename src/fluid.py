import fluidsynth
import consts as c

FLUID = fluidsynth.Synth(gain=c.GAIN, samplerate=c.SAMPLE_RATE)

FLUID.setting("midi.portname", c.MIDI_PORT_NAME)
