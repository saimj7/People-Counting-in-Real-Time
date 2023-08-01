import random


ALL_GENRES = {
    "Alternative Rock",
    "Ambient",
    "Classical",
    "Country",
    "Dance & EDM",
    "Dancehall",
    "Deep House",
    "Disco",
    "Drum & Bass",
    "Electronic",
    "Folk & Singer-Songwriter",
    "Hip Hop & Rap",
    "House",
    "Indie",
    "Jazz & Blues",
    "Latin",
    "Metal",
    "Piano",
    "Pop",
    "R&B & Soul",
    "Reggae",
    "Rock",
    "Techno",
    "Trance",
    "Trap",
    "Trip Hop",
    "World",
}

VOLUME_RANGE_TO_GENRE = {
    (0, 10): {"Classical", "Piano", "Reggae"},
    (10, 75): {
        "Ambient",
        "Country",
        "Piano",
        "Reggae",
        "Classical",
        "Jazz & Blues",
        "Folk & Singer-Songwriter",
        "World",
    },
    (75, 175): {
        "Latin",
        "Disco",
        "Dancehall",
        "Trip Hop",
        "Metal",
        "Drum & Bass",
        "Electronic",
        "Deep House",
        "House",
        "Hip Hop & Rap",
        "R&B & Soul",
        "Rock",
        "Pop",
        "Indie",
        "Alternative Rock",
    },
}
VOLUME_RANGE_TO_GENRE[(175, None)] = VOLUME_RANGE_TO_GENRE[(75, 175)].union({
    "Dance & EDM",
    "Techno",
    "Trance",
    "Trap",
})


def get_genres(volume: float) -> set:
    """Return a set of genres that match the given volume."""
    for rang, genres in VOLUME_RANGE_TO_GENRE.items():
        if rang[0] <= volume < rang[1]:
            return genres
    return VOLUME_RANGE_TO_GENRE[(175, None)]


def random_genre(volume: float):
    """Return a random genre that matches the given volume."""
    return random.choice(list(get_genres(volume)))


if __name__ == "__main__":
    for rang, genres in VOLUME_RANGE_TO_GENRE.items():
        assert all(genre in ALL_GENRES for genre in genres)
