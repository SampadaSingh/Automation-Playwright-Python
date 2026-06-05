from playwright.sync_api import sync_playwright
data= ["hello","Automation","world","click"]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://testautomationpractice.blogspot.com/")

    #1. data in title
    for word in data:
        try:
            assert word in page.title()
            
            print(f"'{word}' is present in the title. PASS")
        except AssertionError:  
            print(f"'{word}' is NOT present in the title. FAIL")  

    #2.word count
    keyword = data[3]
    content = page.content()
    count = content.count(keyword)

    print(f"The word '{keyword}' appears {count} times in the page content.")

    browser.close()