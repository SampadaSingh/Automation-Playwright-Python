def test_open_site(page):
    page.goto("https://testautomationpractice.blogspot.com/")

    assert "Automation" in page.title()

def test_form_fields(page):
    page.goto("https://testautomationpractice.blogspot.com/")

    assert page.locator("#name").is_visible()
    assert page.locator("#email").is_visible()

def test_fill_form(page):
    page.goto("https://testautomationpractice.blogspot.com/")

    page.fill("#name", "Sam")
    page.fill("#email", "sam@example.com")

    assert page.locator("#name").input_value() == "Sam"

def test_checkbox(page):
    page.goto("https://testautomationpractice.blogspot.com/")

    checkbox = page.locator("#male")

    checkbox.check()

    assert checkbox.is_checked()

def test_list_item(page):
    page.goto("https://testautomationpractice.blogspot.com/")

    list_item = page.locator("#colors")
    list_item.select_option("red")
    assert list_item.input_value() == "red"

    page.wait_for_timeout(5000)

