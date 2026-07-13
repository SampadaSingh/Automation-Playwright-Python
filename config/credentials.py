import json
import os


def get_students():
    file_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "students.json"
    )

    with open(file_path, "r") as file:
        return json.load(file)