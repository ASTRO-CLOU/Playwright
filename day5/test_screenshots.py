import base64
from pathlib import Path

from playwright.sync_api import Page, expect

SCREENS = Path(__file__).parent.parent / "docs" / "screens"


def test_page_screenshot(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/aria.html")
    expect(page.get_by_role("heading", level=1)).to_be_visible()

    page.screenshot(path=str(SCREENS / "day5_page.png"))
    assert (SCREENS / "day5_page.png").stat().st_size > 0


def test_full_page_screenshot(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/locators_ext.html")

    page.screenshot(path=str(SCREENS / "day5_full_page.png"), full_page=True)
    assert (SCREENS / "day5_full_page.png").stat().st_size > 0


def test_element_screenshot(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/locators_ext.html")

    page.locator("#box").screenshot(path=str(SCREENS / "day5_element.png"))
    assert (SCREENS / "day5_element.png").stat().st_size > 0


def test_screenshot_into_buffer(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/aria.html")

    screenshot_bytes = page.screenshot()
    assert base64.b64encode(screenshot_bytes).decode().startswith("iVBOR")
