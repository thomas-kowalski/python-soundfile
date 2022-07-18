#%%
import os
import numpy as np
import soundfile as sf

def get_chunks(filepath):
    loopstart = 0; loopend = 0
    with sf.SoundFileEx(filepath, "r") as snd:
        chunk = snd.get_instrument_chunk()
        try:
            loopstart = chunk.loops[0][0]
            loopend = chunk.loops[0][1]
        except:
            pass
    return loopstart, loopend

def write_with_chunks(filepath, x, sr, channels, loopinfo, subtype):
        with sf.SoundFileEx(
            filepath,
            "w",
            samplerate = sr,
            channels   = channels,
            subtype    = subtype
        ) as snd:
            snd.set_instrument_chunk(loops=[(loopinfo[0], loopinfo[1])])
            snd.write(x)

f = r'/Users/thomaskowalski/Desktop/Convert/Peach De Mode/Peach De Mode-A-1.wav'
x = np.zeros(44100)

write_with_chunks("./test.wav", x, 44100, 1, (22050, 34000), sf.info(f).subtype)

