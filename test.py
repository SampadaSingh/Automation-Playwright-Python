from playwright.sync_api import sync_playwright
from tabulate import tabulate

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://testautomationpractice.blogspot.com/")

    # Get all rows
    rows = page.locator("table[name='BookTable'] tr")

    table_data = []

    headers = []

    for i in range(rows.count()):
        row = rows.nth(i)

        # Get headers (first row)
        ths = row.locator("th")
        if ths.count() > 0:
            for j in range(ths.count()):
                headers.append(ths.nth(j).text_content().strip())
            continue

        # Get normal cells
        cells = row.locator("td")
        row_data = []

        for j in range(cells.count()):
            text = cells.nth(j).text_content()
            row_data.append(text.strip() if text else "")

        table_data.append(row_data)

    browser.close()

print(tabulate(table_data, headers=headers, tablefmt="grid"))