import logging
import os
import threading

from dotenv import load_dotenv
from flask import Flask
import time
from pytradfri.api import libcoap_api
from pytradfri import gateway
from pytradfri import error

import spotify
import waves

logger = logging.getLogger(__name__)

app = Flask(__name__)

load_dotenv(".env")

TRADFRI_IDENTITY = os.environ["TRADFRI_IDENTITY"]
TRADFRI_PSK = os.environ["TRADFRI_PSK"]
TRADFRI_IP = os.environ["TRADFRI_IP"]

volumes_entries = []
num_of_people = []
current_wave = waves.WaveType.SINE  # Start with a sine wave for now
song_started_at = time.time()  # The time the song started playing
currently_playing_tempo = 0  # The tempo of the current song


@app.route("/input_volume/<volume>", methods=["POST"])
def input_volume(volume):
    global volumes_entries
    volumes_entries.append(volume)

    # We'll get 30 volume entries per second, and we only want to store the last 2 minutes of data
    # (120 * 30 = 3600 - We'll keep the last 3600 entries, and discard the rest.
    if len(volumes_entries) > 3600:
        volumes_entries = volumes_entries[-3600:]

    return "k"


@app.route("/input_people/<people>", methods=["POST"])
def input_people(people):
    global num_of_people
    num_of_people.append(people)
    # We'll get 30 people entries per second, and we only want to store the last 2 minutes of data
    # (120 * 30 = 3600 - We'll keep the last 3600 entries, and discard the rest.
    if len(num_of_people) > 3600:
        num_of_people = num_of_people[-3600:]

    return "k"


def light_control():
    global song_started_at
    global currently_playing_tempo
    logging.basicConfig(level=logging.INFO)

    api_factory = libcoap_api.APIFactory(
        host=TRADFRI_IP, psk_id=TRADFRI_IDENTITY, psk=TRADFRI_PSK
    )
    api = api_factory.request
    connection = gateway.Gateway()
    devices_commands = api(connection.get_devices(), timeout=2)
    try:
        devices = api(devices_commands, timeout=2)
    except error.RequestTimeout:
        # This sometimes fails with a timeout error, so we'll retry
        devices = api(devices_commands, timeout=2)
    lights = [dev for dev in devices if dev.has_light_control]
    office_light = lights[4]  # Used for testing in the office
    change_lighting(api, currently_playing_tempo, office_light, song_started_at)


def change_lighting(api, currently_playing_tempo, office_light, song_started_at):
    while True:
        light_value = round(
            waves.lighting_step(current_wave, currently_playing_tempo, song_started_at)
        )
        # We should never set the valu below 30 so it doesn't go off
        light_value = max(light_value, 30)
        logger.info(f"Light value: {str(light_value)}")
        try:
            api(office_light.light_control.set_dimmer(light_value), timeout=1)
        except error.RequestTimeout:
            # This sometimes fails with a timeout error, so we'll just ignore it for now
            continue
        time.sleep(60 / currently_playing_tempo)


def music_control():
    global song_started_at
    global currently_playing_tempo
    song_started_at = time.time()
    position_in_song = 0
    currently_playing_tempo = (
        spotify.get_currently_playing_tempo()
    )

    while True:
        current_song_position = spotify.get_current_song_position()
        if (
            current_song_position is not None
            and current_song_position < position_in_song
        ):
            # We've started a new song, so we need to reset the song start time and get the tempo of the new song
            song_started_at = time.time()  # Reset the song start time
            currently_playing_tempo = (
                spotify.get_currently_playing_tempo()
            )  # Get the tempo of the new song
        position_in_song = current_song_position
        time.sleep(1)
        logger.info(f"Current song position: {(current_song_position)}")


threading.Thread(
    target=lambda: app.run(host="0.0.0.0", port=3000, debug=False, use_reloader=False)
).start()
threading.Thread(target=light_control).start()
threading.Thread(target=music_control).start()
