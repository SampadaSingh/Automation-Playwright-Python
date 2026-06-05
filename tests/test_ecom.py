import pytest
def test_ecom(page):
    page.goto("https://automationexercise.com/login")

    assert page.locator("[data-qa='login-email']").is_visible()
    assert page.locator("[data-qa='login-password']").is_visible()