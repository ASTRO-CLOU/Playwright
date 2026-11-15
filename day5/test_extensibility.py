from playwright.sync_api import Page, Playwright, expect

TAG_SELECTOR = """
{
  query(root, selector) {
    return root.querySelector(selector);
  },
  queryAll(root, selector) {
    return Array.from(root.querySelectorAll(selector));
  }
}
"""


def test_custom_selector_engine(page: Page, playwright: Playwright, fixture_url: str):
    playwright.selectors.register("tag", TAG_SELECTOR)
    page.goto(f"{fixture_url}/locators_ext.html")

    buttons = page.locator("tag=button")
    expect(buttons).to_have_count(6)
    buttons.first.click()


def test_custom_selector_combined_with_text(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/locators_ext.html")

    promo = page.locator("tag=div").filter(has_text="Promo")
    expect(promo).to_have_count(1)
