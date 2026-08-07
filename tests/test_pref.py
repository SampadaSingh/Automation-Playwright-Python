import json
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright


LOGIN_URL = "http://localhost/TCFS/auth/login.php"

USERS_FILE = Path(__file__).parent.parent / "data" / "users.json"
PREFERENCES_FILE = Path(__file__).parent.parent / "data" / "test_pref.json"


def load_users():
    with open(USERS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)["users"]


def load_preferences():
    with open(PREFERENCES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)["users"]


users = load_users()
preferences = load_preferences()


@pytest.mark.parametrize("user", users)
def test_pref(user):

    preference = next(
        item for item in preferences
        if item["email"] == user["email"]
    )

    print(f"\nTesting: {user['name']}")

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(LOGIN_URL)

        page.locator('input[name="email"]').fill(user["email"])
        page.locator('input[name="password"]').fill(user["password"])

        page.locator('button[type="submit"]').click()

        page.wait_for_load_state("networkidle")

        assert "preferences.php" in page.url

        print("Login: PASS")
        print("Preferences page: PASS")

        page.locator("#destination").fill(
            preference["preferred_destination"]
        )

        for style in preference["trip_styles"]:
            page.locator(f"#style_{style}").check()

        page.locator("#available_from").fill(
            preference["available_from"]
        )

        page.locator("#available_to").fill(
            preference["available_to"]
        )

        page.locator("#budget_min").fill(
            preference["budget_min"]
        )

        page.locator("#budget_max").fill(
            preference["budget_max"]
        )

        page.locator("#travel_mode").select_option(
            preference["travel_mode"]
        )

        page.locator("#age_min").fill(
            preference["age_min"]
        )

        page.locator("#age_max").fill(
            preference["age_max"]
        )

        page.locator("#preferred_gender").select_option(
            preference["preferred_gender"]
        )

        page.locator('button[type="submit"]').click()

        page.wait_for_load_state("networkidle")

        errors = page.locator(".alert.alert-danger")

        if errors.count() > 0:
            print("Validation Error:")
            print(errors.first.inner_text().strip())
        else:
            assert "userDashboard.php" in page.url
            print("Preferences: PASS")
            print("Dashboard redirect: PASS")

        browser.close()