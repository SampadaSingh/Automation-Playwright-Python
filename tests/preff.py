from playwright.sync_api import sync_playwright

LOGIN_URL = "http://localhost/TCFS/auth/login.php"

EMAIL = "sampada@example.com"
PASSWORD = "Test@12345"


def test_invalid_preferences():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Login
        page.goto(LOGIN_URL)

        page.locator('input[name="email"]').fill(EMAIL)
        page.locator('input[name="password"]').fill(PASSWORD)
        page.locator('button[type="submit"]').click()

        page.wait_for_load_state("networkidle")

        # 1. Invalid Date Range

        page.locator("#available_from").fill("2026-12-20")
        page.locator("#available_to").fill("2026-12-10")

        page.locator('button[type="submit"]').click()
        page.wait_for_load_state("networkidle")

        errors = page.locator(".alert.alert-danger")

        print("\n--- Invalid Date Test ---")

        if errors.count() > 0:
            print("Status: PASS")
            print("Input: Available From > Available To")
            print(f"Error: {errors.first.inner_text().strip()}")
        else:
            print("Status: FAIL")
            print("No error message displayed")
        # 2. Invalid Age Range

        page.goto(page.url)

        page.locator("#age_min").fill("45")
        page.locator("#age_max").fill("20")

        page.locator('button[type="submit"]').click()
        page.wait_for_load_state("networkidle")

        errors = page.locator(".alert.alert-danger")

        print("\n--- Invalid Age Test ---")

        if errors.count() > 0:
            print("Status: PASS")
            print("Input: Minimum Age > Maximum Age")
            print(f"Error: {errors.first.inner_text().strip()}")
        else:
            print("Status: FAIL")
            print("No error message displayed")

        # 3. Invalid Budget Range

        page.goto(page.url)

        page.locator("#budget_min").fill("50000")
        page.locator("#budget_max").fill("1000")

        page.locator('button[type="submit"]').click()
        page.wait_for_load_state("networkidle")

        errors = page.locator(".alert.alert-danger")

        print("\n--- Invalid Budget Test ---")

        if errors.count() > 0:
            print("Status: PASS")
            print("Input: Minimum Budget > Maximum Budget")
            print(f"Error: {errors.first.inner_text().strip()}")
        else:
            print("Status: FAIL")
            print("No error message displayed")

        browser.close()