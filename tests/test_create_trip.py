import json
from pathlib import Path

from playwright.sync_api import sync_playwright


LOGIN_URL = "http://localhost/TCFS/auth/login.php"
CREATE_TRIP_URL = "http://localhost/TCFS/user/createTrip.php"

USERS_FILE = Path(__file__).parent.parent / "data" / "users.json"
TRIPS_FILE = Path(__file__).parent.parent / "data" / "new_trips.json"
IMAGE_DIR = Path(__file__).parent.parent / "img"


def load_users():
    with open(USERS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)["users"]


def load_trips():
    with open(TRIPS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)["trips"]


users = load_users()
trips = load_trips()


def test_create_trips():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for trip in trips:

            user = next(
                user for user in users
                if user["email"] == trip["creator_email"]
            )

            page.goto(LOGIN_URL)

            page.locator('input[name="email"]').fill(
                user["email"]
            )

            page.locator('input[name="password"]').fill(
                user["password"]
            )

            page.locator('button[type="submit"]').click()

            page.wait_for_load_state("networkidle")

            assert "userDashboard.php" in page.url

            page.goto(CREATE_TRIP_URL)
            page.wait_for_load_state("networkidle")

            page.locator('input[name="name"]').fill(
                trip["name"]
            )

            page.locator('input[name="destination"]').fill(
                trip["destination"]
            )

            page.locator('input[name="start_place"]').fill(
                trip["start_place"]
            )

            page.locator('input[name="end_place"]').fill(
                trip["end_place"]
            )

            page.locator('textarea[name="description"]').fill(
                trip["description"]
            )

            if trip.get("image"):
                image_path = IMAGE_DIR / trip["image"]

                assert image_path.exists(), (
                    f"Image not found: {image_path}"
                )

                page.locator(
                    'input[name="trip_image"]'
                ).set_input_files(image_path)

            page.locator('input[name="start_date"]').fill(
                trip["start_date"]
            )

            page.locator('input[name="end_date"]').fill(
                trip["end_date"]
            )

            page.locator(
                'select[name="budget_range"]'
            ).select_option(
                trip["budget_range"]
            )

            page.locator(
                'select[name="travel_mode"]'
            ).select_option(
                trip["travel_mode"]
            )

            page.locator(
                'input[name="group_size_min"]'
            ).fill(
                trip["group_size_min"]
            )

            page.locator(
                'input[name="group_size_max"]'
            ).fill(
                trip["group_size_max"]
            )

            page.locator(
                'input[name="age_min"]'
            ).fill(
                trip["age_min"]
            )

            page.locator(
                'input[name="age_max"]'
            ).fill(
                trip["age_max"]
            )

            page.locator(
                'select[name="preferred_gender"]'
            ).select_option(
                trip["preferred_gender"]
            )

            page.locator(
                'select[name="trip_style"]'
            ).select_option(
                trip["trip_style"]
            )

            page.locator(
                'button[type="submit"]:has-text("Create Trip")'
            ).click()

            page.wait_for_load_state("networkidle")

            print(f"\nCreator: {user['name']}")
            print(
                f"Trip Creation: {trip['name']} (PASS)"
            )

        browser.close()