import asyncio
import numpy as np
import sounddevice as sd
import sys

def print_volume(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    print(volume_norm)
    print("|" * int(volume_norm))

async def main():
    with sd.InputStream(callback=print_volume) as stream:
        while True:
            sd.sleep(1000)
            await asyncio.sleep(0)  # Release CPU.

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
