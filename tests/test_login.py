import json
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright


LOGIN_URL = "http://localhost/TCFS/auth/login.php"

DATA_FILE = Path(__file__).parent.parent / "data" / "login_users.json"


def load_users():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)["users"]


@pytest.mark.parametrize("user", load_users())
def test_login(user):

    print(f"\nTesting: {user['name']}")
    print(f"Email: {user['email']}")

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto(LOGIN_URL)

        page.locator('input[name="email"]').fill(user["email"])

        page.locator('input[name="password"]').fill(user["password"])

        page.locator('button[type="submit"]').click()

        page.wait_for_load_state("networkidle")

        if user["expected"] == "success":

            assert (
            "userDashboard.php" in page.url
            or "preferences.php" in page.url
            )
            print("Result: PASS")
            print("Message: Login successful")
            print(f"Redirected to: {page.url}")

        else:

            if user["expected"] == "failure":
                assert "login.php" in page.url
                assert page.locator(".alert-danger").is_visible()

                error_message = page.locator(".alert-danger").inner_text()
                print(f"Error message: {error_message}")
                print(f"Redirected to: {page.url}")
                
        browser.close()