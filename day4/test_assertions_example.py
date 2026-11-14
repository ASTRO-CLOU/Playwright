from pathlib import Path

from playwright.sync_api import Page, expect

FIXTURES = Path(__file__).parent / "fixtures"


def open_fixture(page: Page, file_name: str) -> None:
    page.goto((FIXTURES / file_name).as_uri())


def test_auto_retrying_assertion(page: Page):
    open_fixture(page, "assertions.html")

    expect(page.get_by_test_id("status")).to_have_text("Submitted")


def test_checkbox_assertion(page: Page):
    open_fixture(page, "assertions.html")

    subscribe = page.get_by_label("Subscribe")

    expect(subscribe).not_to_be_checked()

    subscribe.check()

    expect(subscribe).to_be_checked()


def test_element_state_assertions(page: Page):
    open_fixture(page, "assertions.html")

    expect(page.get_by_role("button", name="Disabled")).to_be_disabled()

    expect(page.get_by_test_id("hidden")).to_be_hidden()


def test_list_assertion(page: Page):
    open_fixture(page, "assertions.html")

    expect(page.locator("li")).to_have_count(3)

    expect(page.locator("li")).to_have_text(["apple", "banana", "orange"])


def test_input_value_assertion(page: Page):
    open_fixture(page, "assertions.html")

    name = page.get_by_label("Name")

    name.fill("Андрей")

    expect(name).to_have_value("Андрей")
