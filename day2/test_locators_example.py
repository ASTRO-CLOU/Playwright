import re
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

FIXTURES = Path(__file__).parent / "fixtures"


def open_fixture(page: Page, file_name: str) -> None:
    page.goto((FIXTURES / file_name).as_uri())


def test_locate_by_role(page: Page):
    open_fixture(page, "locators.html")
    expect(page.get_by_role("heading", name="Sign up")).to_be_visible()

    page.get_by_role("checkbox", name="Subscribe").check()

    page.get_by_role("button", name=re.compile("submit", re.IGNORECASE)).click()


def test_locate_by_label(page: Page):
    open_fixture(page, "locators.html")
    page.get_by_label("Password").fill("secret")


def test_locate_by_placeholder(page: Page):
    open_fixture(page, "locators.html")
    page.get_by_placeholder("name@example.com").fill("playwright@microsoft.com")


def test_locate_by_text(page: Page):
    open_fixture(page, "locators.html")
    expect(page.get_by_text("Welcome, John")).to_be_visible()
    expect(page.get_by_text("Welcome, John", exact=True)).to_be_visible()
    expect(page.get_by_text(re.compile("welcome, john", re.IGNORECASE))).to_be_visible()


def test_locate_by_alt_text(page: Page):
    open_fixture(page, "locators.html")
    page.get_by_alt_text("playwright logo").click()


def test_locate_by_title(page: Page):
    open_fixture(page, "locators.html")
    expect(page.get_by_title("Issues count")).to_have_text("25 issues")


def test_locate_by_test_id(page: Page):
    open_fixture(page, "locators.html")
    page.get_by_test_id("directions").click()


def test_locate_by_css_or_xpath(page: Page):
    open_fixture(page, "locators.html")
    page.locator("css=button").first.click()
    page.locator("xpath=//button").first.click()
    page.locator("button").first.click()


def test_matching_only_visible_elements(page: Page):
    open_fixture(page, "visible_buttons.html")
    page.locator("button").visible.click()


def test_filter_by_text(page: Page):
    open_fixture(page, "products.html")
    page.get_by_role("listitem").filter(has_text="Product 2").get_by_role(
        "button", name="Add to cart"
    ).click()


def test_filter_by_text_with_regex(page: Page):
    open_fixture(page, "products.html")
    page.get_by_role("listitem").filter(has_text=re.compile("Product 2")).get_by_role(
        "button", name="Add to cart"
    ).click()


def test_filter_by_not_having_text(page: Page):
    open_fixture(page, "products.html")
    expect(
        page.get_by_role("listitem").filter(has_not_text="Out of stock")
    ).to_have_count(2)


def test_filter_by_child(page: Page):
    open_fixture(page, "products.html")
    page.get_by_role("listitem").filter(
        has=page.get_by_role("heading", name="Product 2")
    ).get_by_role("button", name="Add to cart").click()

    expect(
        page.get_by_role("listitem").filter(
            has=page.get_by_role("heading", name="Product 2")
        )
    ).to_have_count(1)


def test_filter_by_not_having_child(page: Page):
    open_fixture(page, "products.html")
    expect(
        page.get_by_role("listitem").filter(
            has_not=page.get_by_role("heading", name="Product 2")
        )
    ).to_have_count(2)


def test_matching_inside_locator(page: Page):
    open_fixture(page, "products.html")
    product = page.get_by_role("listitem").filter(has_text="Product 2")

    product.get_by_role("button", name="Add to cart").click()


def test_matching_two_locators(page: Page):
    open_fixture(page, "locators.html")
    button = page.get_by_role("button").and_(page.get_by_title("Bookmark"))
    expect(button).to_have_text("Save")


def test_count_items_in_list(page: Page):
    open_fixture(page, "lists.html")
    expect(page.get_by_role("listitem")).to_have_count(3)


def test_assert_all_text_in_list(page: Page):
    open_fixture(page, "lists.html")
    expect(page.get_by_role("listitem")).to_have_text(["apple", "banana", "orange"])


def test_get_specific_item(page: Page):
    open_fixture(page, "lists.html")
    page.get_by_text("orange").click()
    page.get_by_role("listitem").filter(has_text="orange").click()
    page.get_by_test_id("orange").click()

    banana = page.get_by_role("listitem").nth(1)
    expect(banana).to_have_text("banana")


def test_iterate_list(page: Page, capsys):
    open_fixture(page, "lists.html")
    for row in page.get_by_role("listitem").all():
        print(row.text_content())

    rows = page.get_by_role("listitem")
    count = rows.count()
    for i in range(count):
        print(rows.nth(i).text_content())

    texts = rows.evaluate_all("list => list.map(element => element.textContent)")
    assert texts == ["apple", "banana", "orange"]
    assert "banana" in capsys.readouterr().out


def test_chaining_filters(page: Page):
    open_fixture(page, "rows.html")
    row_locator = page.get_by_role("listitem")

    row_locator.filter(has_text="Mary").filter(
        has=page.get_by_role("button", name="Say goodbye")
    ).screenshot(path="docs/screens/day2_chained_filter.png")


def test_strictness(page: Page):
    open_fixture(page, "products.html")
    expect(page.get_by_role("button")).to_have_count(2)

    with pytest.raises(Exception):
        page.get_by_role("button").click()
