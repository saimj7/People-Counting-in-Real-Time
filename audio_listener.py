import asyncio
import numpy as np
import requests
import sounddevice as sd
import sys
from time import time as now

# Configuration options.
SAMPLE_WINDOW_SIZE = 300  # How many audio frames to keep in the buffer for analysis.
SECONDS_BETWEEN_UPDATES = 1  # How many seconds to wait before updating the server.
PRINT_VOLUMES = True
MAX_VOLUME = 500

# Persistent data.
VOLUME_HISTORY = [0.0] * SAMPLE_WINDOW_SIZE
LAST_UPDATE_TIME = now() - SECONDS_BETWEEN_UPDATES  # So first update is immediate.
SAMPLES_SINCE_LAST_UPDATE = 0


def update_server():
    global VOLUME_HISTORY
    new_average = sum(VOLUME_HISTORY) / SAMPLE_WINDOW_SIZE
    requests.post(f"http://localhost:5000/input_volume/{new_average}")


def append_volume(indata, frames, time, status):
    global VOLUME_HISTORY
    global PRINT_VOLUMES
    global LAST_UPDATE_TIME
    global SAMPLES_SINCE_LAST_UPDATE
    SAMPLES_SINCE_LAST_UPDATE += 1
    volume_norm = np.linalg.norm(indata)*10
    VOLUME_HISTORY.append(volume_norm)
    VOLUME_HISTORY.pop(0)  # Remove oldest frame.
    diff = now() - LAST_UPDATE_TIME
    if diff >= SECONDS_BETWEEN_UPDATES:
        SAMPLES_SINCE_LAST_UPDATE = 0
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
