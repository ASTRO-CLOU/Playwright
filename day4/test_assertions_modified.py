from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

FIXTURES = Path(__file__).parent / "fixtures"


def open_fixture(page: Page, file_name: str) -> None:
    page.goto((FIXTURES / file_name).as_uri())


def test_soft_assertions_do_not_stop_the_test(page: Page):
    open_fixture(page, "assertions.html")

    expect.soft(page.get_by_test_id("status")).to_have_text("Submitted")
    expect.soft(page.get_by_label("Subscribe")).not_to_be_checked()

    page.get_by_label("Name").fill("Андрей")

    expect(page.get_by_label("Name")).to_have_value("Андрей")


def test_custom_message(page: Page):
    open_fixture(page, "assertions.html")

    with pytest.raises(AssertionError) as error:
        expect(page.get_by_text("Name"), "пользователь должен быть в системе",
               ).to_be_visible(timeout=1_000)

    assert "пользователь должен быть в системе" in str(error.value)


def test_timeout_per_assertion(page: Page):
    open_fixture(page, "assertions.html")

    expect(page.get_by_test_id("status")).to_have_text("Submitted", timeout=5_000)


def test_attributes_and_classes(page: Page):
    open_fixture(page, "assertions.html")

    expect(page.get_by_label("Name")).to_have_attribute("value", "")

    expect(page.get_by_role("button", name="Disabled")).to_have_attribute(
        "disabled", ""
    )
