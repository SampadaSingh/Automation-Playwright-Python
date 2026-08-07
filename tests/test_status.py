import json
from pathlib import Path
from datetime import datetime, date

import pytest
from playwright.sync_api import sync_playwright


LOGIN_URL = "http://localhost/TCFS/auth/login.php"
TRIPS_URL = "http://localhost/TCFS/admin/manageTrips.php"

ADMIN_FILE = Path(__file__).parent.parent / "data" / "admin.json"


def load_admin():
    with open(ADMIN_FILE, "r", encoding="utf-8") as file:
        return json.load(file)["admin"]


def test_complete_past_pending_trips():

    admin = load_admin()

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(LOGIN_URL)

        page.locator('input[name="email"]').fill(admin["email"])
        page.locator('input[name="password"]').fill(admin["password"])

        page.locator('button[type="submit"]').click()
        page.wait_for_load_state("networkidle")

        assert "admin" in page.url.lower()

        print("\nAdmin Login: PASS")

        page.goto(TRIPS_URL)
        page.wait_for_load_state("networkidle")

        print("Manage Trips: PASS")

        today = date.today()

        rows = page.locator("table tbody tr")

        updated = 0

        for i in range(rows.count()):

            row = rows.nth(i)
 
            trip_name = row.locator("td").nth(1).inner_text().strip()

            date_text = row.locator("td").nth(5).inner_text().strip()

            status = row.locator(".status-badge").inner_text().strip()

            # Get end date
            end_date_text = date_text.split(" - ")[1]

            end_date = datetime.strptime(
                end_date_text,
                "%b %d, %Y"
            ).date()

            # Check past + pending
            if end_date < today and status.lower() == "pending":

                print(f"\nTrip: {trip_name}")
                print(f"End date: {end_date}")
                print("Status: Pending")

                row.locator(".btn-edit").click()

                page.locator("#edit_status").select_option("completed")

                page.get_by_role("button", name="Update Trip").click()

                page.wait_for_load_state("networkidle")

                print("Status changed: Pending → Completed")

                updated += 1

        print(f"\nTotal trips updated: {updated}")

        browser.close()