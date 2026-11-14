from pathlib import Path

import pytest
from playwright.sync_api import Error, Playwright

FIXTURES = Path(__file__).parent / "fixtures"


def open_popup_fixture(playwright: Playwright, browser_name: str) -> str:
    browser = getattr(playwright, browser_name).launch()
    page = browser.new_page()
    page.goto((FIXTURES / "popup.html").as_uri())
    title = page.title()
    version = browser.version
    browser.close()
    print(f"{browser_name}: {version}, заголовок страницы: {title}")
    return title


def test_all_three_browsers(playwright: Playwright):
    for browser_name in ("chromium", "firefox", "webkit"):
        assert open_popup_fixture(playwright, browser_name) == "Popup"


def test_edge_channel(playwright: Playwright):
    try:
        browser = playwright.chromium.launch(channel="msedge")
    except Error as error:
        pytest.skip(f"Microsoft Edge не установлен: {error}")

    page = browser.new_page()
    page.goto((FIXTURES / "popup.html").as_uri())

    assert page.title() == "Popup"

    browser.close()
