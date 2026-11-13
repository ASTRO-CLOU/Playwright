from pathlib import Path

import pytest
from playwright.sync_api import Error, Page, expect

FIXTURES = Path(__file__).parent / "fixtures"


def open_fixture(page: Page, file_name: str) -> None:
    page.goto((FIXTURES / file_name).as_uri())


def test_click_waits_until_button_is_enabled(page: Page):
    open_fixture(page, "auto_waiting.html")

    page.get_by_role("button", name="Sign Up").click()

    expect(page.get_by_role("button", name="Sign Up")).to_be_enabled()


def test_expect_waits_until_text_appears(page: Page):
    open_fixture(page, "auto_waiting.html")

    expect(page.get_by_text("Loaded content")).to_be_visible()


def test_covered_element_is_not_clicked(page: Page):
    open_fixture(page, "auto_waiting.html")

    with pytest.raises(Error) as click_error:
        page.get_by_role("button", name="Save").click(timeout=1000)

    assert "intercepts pointer events" in str(click_error.value)


def test_inert_element_is_not_clicked(page: Page):
    open_fixture(page, "auto_waiting.html")

    with pytest.raises(Error) as click_error:
        page.get_by_role("button", name="Inert button").click(timeout=1000)

    assert "element is inert" in str(click_error.value)


def test_visible_rules(page: Page):
    open_fixture(page, "auto_waiting.html")

    expect(page.get_by_text("Transparent text")).to_be_visible()

    expect(page.get_by_text("Zero size text")).to_be_hidden()


def test_force_click_on_covered_element(page: Page):
    open_fixture(page, "auto_waiting.html")

    page.get_by_role("button", name="Save").click(force=True)
