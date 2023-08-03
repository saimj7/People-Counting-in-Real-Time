import sqlite3


def initialize_db():
    con = sqlite3.connect("spotify.db")
    cur = con.cursor()
    # Create a Tracks table if it doesn't exist, with the following columns:
    # - id (primary key)
    # - name
    # - artist
    # - album
    # - danceability
    # - energy
    # - key
    # - loudness
    # - mode
    # - speechiness
    # - acousticness
    # - instrumentalness
    # - liveness
    # - valence
    # - tempo
    # - duration_ms
    # - time_signature
    # - Playlist ID
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Tracks (
            id TEXT PRIMARY KEY,
            name TEXT,
            artist TEXT,
            album TEXT,
            danceability REAL,
            energy REAL,
            key INTEGER,
            loudness REAL,
            mode INTEGER,
            speechiness REAL,
            acousticness REAL,
            instrumentalness REAL,
            liveness REAL,
            valence REAL,
            tempo REAL,
            popularity INTEGER,
            duration_ms INTEGER,
            time_signature INTEGER,
            playlist_id TEXT
        )
        """
    )


def insert_track(track: dict, playlist_id: str) -> None:
    con = sqlite3.connect("spotify.db")
    cur = con.cursor()
    # Insert a track into the Tracks table. Track is a dictionary mapped with the keys above.
    # If the track already exists, update the values.
    cur.execute(
        """
        INSERT OR IGNORE INTO Tracks (
            id, name, artist, album, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, popularity, duration_ms, time_signature, playlist_id
            )
        VALUES (
             ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
             )          
        """,
        (
            track["id"],
            track["name"],
            track["artist"],
            track["album"],
            track["danceability"],
            track["energy"],
            track["key"],
            track["loudness"],
            track["mode"],
            track["speechiness"],
            track["acousticness"],
            track["instrumentalness"],
            track["liveness"],
            track["valence"],
            track["tempo"],
            track["popularity"],
            track["duration_ms"],
            track["time_signature"],
            playlist_id,
        ),
    )
    con.commit()


def find_track(*, popularity: int, energy: float) -> tuple:
    """
    Find a track in the Tracks table that matches the given popularity and energy.
    Results will have multiple tracks if there are multiple tracks with the same popularity and energy - select one at random.
    """
    con = sqlite3.connect("spotify.db")
    cur = con.cursor()
    cur.execute(
        """
        SELECT * FROM Tracks WHERE popularity = ? AND energy = ? ORDER BY RANDOM() LIMIT 1
        """,
        (popularity, energy),
    )
    return cur.fetchone()