from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    page.goto("https://testautomationpractice.blogspot.com/")

    # 1. Open dropdown
    dropdown = page.get_by_placeholder("Select an item")
    dropdown.click()

    # 2. Select target item directly
    page.get_by_text("Item 20").click()

    # 3. Assertion (verify selection)
    selected_value = dropdown.input_value()

    assert "Item 20" in selected_value

    print("PASS: Item 20 selected successfully")

    page.wait_for_timeout(5000) 
    browser.close()