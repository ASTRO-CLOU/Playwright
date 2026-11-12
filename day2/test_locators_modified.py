import re
from pathlib import Path

from playwright.sync_api import Page, Playwright, expect

FIXTURES = Path(__file__).parent / "fixtures"


def open_fixture(page: Page, file_name: str) -> None:
    page.goto((FIXTURES / file_name).as_uri())


def test_role_with_regex_and_level(page: Page):
    open_fixture(page, "locators.html")

    expect(
        page.get_by_role("heading", name=re.compile("sign up", re.IGNORECASE), level=3)
    ).to_have_count(1)


def test_custom_test_id_attribute(page: Page, playwright: Playwright):
    playwright.selectors.set_test_id_attribute("data-pw")

    open_fixture(page, "custom_test_id.html")
    page.get_by_test_id("directions").click()

    playwright.selectors.set_test_id_attribute("data-testid")


def test_save_button_inside_dialog(page: Page):
    open_fixture(page, "dialog.html")

    save_button = page.get_by_role("button", name="Save")
    expect(save_button).to_have_count(2)

    dialog = page.get_by_test_id("settings-dialog")
    expect(save_button.within(dialog)).to_have_count(1)

    save_button.within(dialog).click()


def test_or_locator(page: Page):
    open_fixture(page, "dialog.html")

    new_email = page.get_by_role("button", name="New")
    dialog = page.get_by_text("Confirm security settings")

    expect(new_email.or_(dialog).first).to_be_visible()
    if dialog.is_visible():
        page.get_by_role("button", name="Dismiss").click()
    new_email.click()


def test_first_last_and_nth(page: Page):
    open_fixture(page, "lists.html")

    items = page.get_by_role("listitem")

    expect(items).to_have_count(3)
    expect(items.first).to_have_text("apple")
    expect(items.last).to_have_text("orange")
    expect(items.nth(1)).to_have_text("banana")


def test_filter_products_with_and_without_stock(page: Page):
    open_fixture(page, "products.html")

    all_items = page.get_by_role("listitem")
    in_stock = all_items.filter(has_not_text="Out of stock")

    expect(all_items).to_have_count(3)
    expect(in_stock).to_have_count(2)
    expect(in_stock.first).to_contain_text("Product 1")
    expect(in_stock.last).to_contain_text("Product 2")
