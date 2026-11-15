from playwright.sync_api import Page, expect


def test_css_locator(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/locators_ext.html")

    expect(page.locator("css=#login")).to_have_text("Log in")


def test_xpath_locator(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/locators_ext.html")

    expect(page.locator("xpath=//button[@id='signin']")).to_have_text("Sign in")


def test_css_with_has_text(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/locators_ext.html")

    page.locator('button:has-text("Sign in")').click()
    expect(page.locator("#signin")).to_be_visible()


def test_nth_match(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/locators_ext.html")

    third_buy = page.locator(':nth-match(:text("Buy"), 3)')
    expect(third_buy).to_be_visible()


def test_right_of_text(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/locators_ext.html")

    page.locator('input:right-of(:text("Username"))').first.fill("student")
    expect(page.locator("#username")).to_have_value("student")


def test_near_element(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/locators_ext.html")

    button = page.locator("button:near(.promo-card)").first
    expect(button).to_have_text("Go")
