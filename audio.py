import asyncio
import numpy as np
import sounddevice as sd
import sys
from time import time as now

# Configuration options.
SAMPLE_WINDOW_SIZE = 20  # How many audio frames to keep in the buffer for analysis.
SECONDS_BETWEEN_UPDATES = 0.5  # How many seconds to wait before updating the server.
PRINT_VOLUMES = True

# Persistent data.
VOLUME_HISTORY = [0.0] * SAMPLE_WINDOW_SIZE
LAST_UPDATE_TIME = now() - SECONDS_BETWEEN_UPDATES  # So first update is immediate.


def update_server():
    """TODO: Send the volume history (or average) to the server."""


def append_volume(indata, frames, time, status):
    global VOLUME_HISTORY
    global PRINT_VOLUMES
    global LAST_UPDATE_TIME
    volume_norm = np.linalg.norm(indata)*10
    VOLUME_HISTORY.append(volume_norm)
    VOLUME_HISTORY.pop(0)  # Remove oldest frame.
    if now() - LAST_UPDATE_TIME >= SECONDS_BETWEEN_UPDATES:
        LAST_UPDATE_TIME = now()
        update_server()
    if PRINT_VOLUMES:
        print(volume_norm)
        print("|" * int(volume_norm))


async def main():
    with sd.InputStream(callback=append_volume) as stream:
        while True:
            sd.sleep(10)
            await asyncio.sleep(0)  # Release CPU.


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
