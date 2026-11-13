import time
from pathlib import Path

import pytest
from playwright.sync_api import Error, Page, expect

FIXTURES = Path(__file__).parent / "fixtures"


def open_fixture(page: Page, file_name: str) -> None:
    page.goto((FIXTURES / file_name).as_uri())


def test_click_waits_for_animation_to_finish(page: Page):
    open_fixture(page, "auto_waiting.html")

    started_at = time.monotonic()
    page.get_by_role("button", name="Sign Up").click()
    elapsed_seconds = time.monotonic() - started_at

    assert elapsed_seconds >= 0.5
    expect(page.get_by_role("button", name="Sign Up")).to_be_enabled()


def test_default_timeout_is_applied_to_actions(page: Page):
    open_fixture(page, "auto_waiting.html")

    page.set_default_timeout(1500)

    started_at = time.monotonic()
    with pytest.raises(Error) as click_error:
        page.get_by_role("button", name="Save").click()
    elapsed_seconds = time.monotonic() - started_at

    assert elapsed_seconds < 3
    assert "Timeout 1500ms exceeded" in str(click_error.value)


def test_inert_button_needs_force(page: Page):
    open_fixture(page, "auto_waiting.html")

    with pytest.raises(Error):
        page.get_by_role("button", name="Inert button").click(timeout=800)

    page.get_by_role("button", name="Inert button").click(force=True, timeout=800)


def test_assertion_waits_for_content(page: Page):
    open_fixture(page, "auto_waiting.html")

    expect(page.locator("#appears-later")).to_contain_text("Loaded content", timeout=3000)

    expect(page.get_by_text("Loaded content")).to_have_count(1)


def test_click_waits_for_button_to_become_enabled(page: Page):
    open_fixture(page, "auto_waiting.html")

    sign_up_button = page.get_by_role("button", name="Sign Up")

    expect(sign_up_button).to_be_visible()
    expect(sign_up_button).to_be_enabled(timeout=3000)
    sign_up_button.click()

    assert sign_up_button.is_enabled()
