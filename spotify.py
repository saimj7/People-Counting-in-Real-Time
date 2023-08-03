import os

from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import db

load_dotenv(".env")

client_id = os.environ["SPOTIFY_CLIENT_ID"]
client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]
redirect_uri = os.environ.get("SPOTIFY_REDIRECT_URI", "http://localhost:8080")
party_playlist_id = os.environ["SPOTIFY_PARTY_PLAYLIST_ID"]



def initialize_spotipy_client():
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=[
                "user-library-read",
                "playlist-read-private",
                "playlist-modify-private",
                "user-modify-playback-state",
                "user-read-playback-state",
                "user-read-currently-playing",
            ],
        )
    )


sp = initialize_spotipy_client()

db.initialize_db()


def get_track_artist(track: dict) -> str:
    return track["artists"][0]["name"]


def get_track_album(track: dict) -> str:
    return track["album"]["name"]


def build_track_dict(track_from_playlist: dict, track_features: dict) -> dict:
    return {
        "id": track_from_playlist["id"],
        "name": track_from_playlist["name"],
        "artist": get_track_artist(track_from_playlist),
        "album": get_track_album(track_from_playlist),
        "danceability": track_features["danceability"],
        "energy": track_features["energy"],
        "key": track_features["key"],
        "loudness": track_features["loudness"],
        "mode": track_features["mode"],
        "speechiness": track_features["speechiness"],
        "acousticness": track_features["acousticness"],
        "instrumentalness": track_features["instrumentalness"],
        "liveness": track_features["liveness"],
        "valence": track_features["valence"],
        "tempo": track_features["tempo"],
        "popularity": track_from_playlist["popularity"],
        "duration_ms": track_features["duration_ms"],
        "time_signature": track_features["time_signature"],
    }


def get_playlist_tracks():
    results = sp.playlist(playlist_id=party_playlist_id)
    all_tracks = []
    tracks = results["tracks"]
    all_tracks.extend(tracks["items"])
    while tracks["next"]:
        tracks = sp.next(tracks)
        all_tracks.extend(tracks["items"])
    for track in all_tracks:
        features = sp.audio_features(track["track"]["id"])[0]
        track_dict = build_track_dict(track["track"], features)
        db.insert_track(track_dict, party_playlist_id)


# get_playlist_tracks()

def get_currently_playing_tempo() -> float:
    current_track = sp.currently_playing()
    features = sp.audio_features(current_track["item"]["id"])[0]
    return float(features["tempo"])

def get_current_song_position() -> int:
    return int(sp.currently_playing()["progress_ms"])

def add_to_queue(track: tuple) -> None:
    sp.add_to_queue(track[0])

# tempo = get_currently_playing_tempo()
# track = find_track(tempo)
# print(track)
# sp.add_to_queue("2M2WJ7gBlcKNxdhyfPp9zY")
# # sp.add_to_queue(track[0])