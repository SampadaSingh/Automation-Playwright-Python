import json
from pathlib import Path

from playwright.sync_api import sync_playwright


BASE_URL = "http://localhost/TCFS"
REGISTER_URL = f"{BASE_URL}/auth/register.php"

USERS_FILE = Path(__file__).parent.parent / "data" / "users.json"


def load_users():
    with open(USERS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)["users"]


def register_user(page, user):
    print(f"\nRegistering: {user['name']}")

    page.goto(REGISTER_URL)

    # Full Name
    page.locator('input[name="name"]').fill(user["name"])

    # Email
    page.locator('input[name="email"]').fill(user["email"])

    # Password
    page.locator('input[name="password"]').fill(user["password"])

    # Confirm Password
    page.locator('input[name="confirm_password"]').fill(
        user["confirm_password"]
    )

    # Location
    page.locator('input[name="location"]').fill(user["location"])

    # Date of Birth
    page.locator('input[name="dob"]').fill(user["dob"])

    # Gender
    page.locator('select[name="gender"]').select_option(user["gender"])

    # Bio
    page.locator('textarea[name="bio"]').fill(user["bio"])

    # Interests
    for interest_id in user["interests"]:
        page.locator(
            f'input[name="interests[]"][value="{interest_id}"]'
        ).check()

    # Submit
    page.locator('button[type="submit"]').click()

    # Verify successful registration
    page.wait_for_url("**/auth/login.php?success=1")

    print(f"PASS: {user['name']} registered successfully.")


def main():
    users = load_users()

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            slow_mo=300
        )

        page = browser.new_page()

        for user in users:
            register_user(page, user)

        print("\n================================")
        print("All users registered successfully")
        print("================================")

        browser.close()


if __name__ == "__main__":
    main()