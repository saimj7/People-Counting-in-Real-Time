import numpy as np
import sounddevice as sd

def print_volume(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    print(volume_norm)
    print("|" * int(volume_norm))

def main():
    stream = sd.InputStream(callback=print_volume)
    with stream:
        while True:
            sd.sleep(1000)
main()