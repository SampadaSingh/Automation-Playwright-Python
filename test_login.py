from playwright.sync_api import sync_playwright
from config.credentials import get_students

URL = "https://erpstudent.ican.org.np/Login"
with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    students = get_students()

    contexts = []

    for student in students:

        context = browser.new_context()

        page = context.new_page()

        page.goto(URL)

        page.fill("#username", student["username"])
        page.fill("#password", student["password"])

        page.click("button[type='submit']")

        print(f"Logged in as {student['username']}")

        contexts.append(context)

    input("All students are logged in. Press Enter to close.")

    browser.close()