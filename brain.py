from flask import Flask

app = Flask(__name__)

volumes_entries = []
num_of_people = []

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

