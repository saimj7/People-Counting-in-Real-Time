import logging
import os
import threading

from dotenv import load_dotenv
from flask import Flask
import time
from pytradfri.api import libcoap_api
from pytradfri import gateway
from pytradfri import error

import db
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
current_wave = waves.WaveType.FLASH  # Start with a sine wave for now
song_started_at = time.time()  # The time the song started playing
currently_playing_tempo = 60  # The tempo of the current song. Start with 60 BPM for now
current_volume = 0
current_people_in_party = 0
max_measured_volume = 0
max_seen_people = 0
max_lower_popularity_bound = 80
max_lower_energy_bound = 0.9

@app.route("/input_volume/<volume>", methods=["POST"])
def input_volume(volume):
    global current_volume
    global max_measured_volume
    volume = float(volume)
    current_volume = volume
    if volume > max_measured_volume:
        max_measured_volume = volume
    logger.info(f"Volume: {volume}")
    logger.info(f"Max volume: {max_measured_volume}")
    return "k"


@app.route("/input_people/<people>", methods=["POST"])
def input_people(people):
    global num_of_people
    global max_seen_people
    if people > max_seen_people:
        max_seen_people = people

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
    devices_commands = None
    devices = None
    while True:
        try:
            devices_commands = devices_commands or api(connection.get_devices(), timeout=2)
            devices = devices or api(devices_commands, timeout=2)
        except error.RequestTimeout:
            logger.error("Request timed out")
            continue
        else:
            break
    lights = [dev for dev in devices if dev.has_light_control]
    logger.info(lights)
    office_light = lights[3]  # Used for testing in the office

    change_lighting(api, currently_playing_tempo, office_light, song_started_at)


def change_lighting(api, currently_playing_tempo, office_light, song_started_at):
    while True:
        light_value = round(
            waves.lighting_step(current_wave, currently_playing_tempo, song_started_at)
        )
        # We should never set the value below 30 so it doesn't go off
        light_value = max(light_value, 30)
        logger.info(f"Light value: {str(light_value)}")
        try:
            threading.Thread(
                target=lambda: api(
                    office_light.light_control.set_dimmer(light_value), timeout=1
                )
            ).start()
            # api(office_light.light_control.set_dimmer(light_value), timeout=1)
        except error.RequestTimeout:
            # This sometimes fails with a timeout error, so we'll just ignore it for now
            continue
        time.sleep(1/ 10)


def music_control():
    global song_started_at
    global currently_playing_tempo
    song_started_at = time.time()
    position_in_song = 0
    currently_playing_tempo = spotify.get_currently_playing_tempo()

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
        # When the song is about to end (30 seconds left), choose a new song

        time.sleep(1)
        logger.info(f"Current song position: {(current_song_position)}")

def choose_new_song():
    global current_volume
    global current_people_in_party
    global max_measured_volume
    global max_seen_people
    global max_lower_popularity_bound
    global max_lower_energy_bound
    min_popularity = (current_people_in_party / max_seen_people) * max_lower_popularity_bound
    min_energy = (current_volume / max_measured_volume) * max_lower_energy_bound
    track = db.find_track(popularity=min_popularity, energy=min_energy)
    spotify.add_to_queue(track)



threading.Thread(
    target=lambda: app.run(host="0.0.0.0", port=3000, debug=False, use_reloader=False)
).start()
# threading.Thread(target=light_control).start()
# threading.Thread(target=music_control).start()
