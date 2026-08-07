import json
from pathlib import Path


PREFERENCES_FILE = (
    Path(__file__).parent.parent / "data" / "pref.json"
)


def update_availability():

    with open(PREFERENCES_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    users = data["users"]

    availability = {
        "sampada@example.com": {
            "available_from": "2026-10-05",
            "available_to": "2026-10-23"
        },
        "alex@example.com": {
            "available_from": "2026-10-15",
            "available_to": "2026-11-03"
        },
        "priya@example.com": {
            "available_from": "2026-11-01",
            "available_to": "2026-11-20"
        },
        "rahul@example.com": {
            "available_from": "2026-11-15",
            "available_to": "2026-12-05"
        }
    }

    for user in users:

        email = user["email"]

        if email in availability:

            user["available_from"] = availability[email]["available_from"]
            user["available_to"] = availability[email]["available_to"]

            print(
                f"Updated: {user['name']} | "
                f"{user['available_from']} → "
                f"{user['available_to']}"
            )

    with open(PREFERENCES_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("\nAvailability updated successfully.")


if __name__ == "__main__":
    update_availability()