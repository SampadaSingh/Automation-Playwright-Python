from playwright.sync_api import expect, sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://testautomationpractice.blogspot.com/")
    button = page.locator("button.start")

    button.click()

    button.wait_for()
    button.expect.to_have_text("STOP")   

    button.click()

    browser.close()