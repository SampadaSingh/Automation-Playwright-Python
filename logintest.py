from playwright.sync_api import sync_playwright

login_data = [
    ("wronguser", "SuperSecretPassword!"),
    ("tomsmith", "SuperSecretPassword!"),
    ("tomsmith", "wrongpass"),
    ("", "")
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://the-internet.herokuapp.com/login")
    for username, password in login_data:
        page.fill("#username",username)
        page.fill("#password",password)
        page.click("button[type='submit']")

        msg = page.locator("#flash").text_content()
        print(f"Login attempt with username: '{username}' and password: '{password}' - Message: {msg.strip()}")

        login_success ="secure" in page.url

        if login_success:
            page.click("a[href='/logout']")
            print("PASS")
        else:
            print("FAIL")

    browser.close()
