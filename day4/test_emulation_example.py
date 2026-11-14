from pathlib import Path

import pytest
from playwright.sync_api import Browser, Error, Page, Playwright, expect

FIXTURES = Path(__file__).parent / "fixtures"
SCREENS = FIXTURES.parent.parent / "docs" / "screens"


def test_devices(playwright: Playwright):
    iphone_13 = playwright.devices["iPhone 13"]
    browser = playwright.webkit.launch()
    context = browser.new_context(**iphone_13)
    page = context.new_page()

    page.goto((FIXTURES / "emulation.html").as_uri())

    expect(page.get_by_test_id("viewport")).to_have_text("390x664")
    page.screenshot(path=str(SCREENS / "day4_emulation.png"))

    context.close()
    browser.close()


def test_viewport_and_high_dpi(browser: Browser):
    context = browser.new_context(viewport={"width": 1280, "height": 1024})
    page = context.new_page()
    page.goto((FIXTURES / "emulation.html").as_uri())

    expect(page.get_by_test_id("viewport")).to_have_text("1280x1024")

    page.set_viewport_size({"width": 1600, "height": 1200})
    page.reload()

    expect(page.get_by_test_id("viewport")).to_have_text("1600x1200")
    context.close()


def test_locale_and_timezone(browser: Browser):
    context = browser.new_context(locale="de-DE", timezone_id="Europe/Berlin")
    page = context.new_page()
    page.goto((FIXTURES / "emulation.html").as_uri())

    expect(page.get_by_test_id("locale")).to_have_text("de-DE")
    expect(page.get_by_test_id("timezone")).to_have_text("Europe/Berlin")

    context.close()


def test_geolocation_with_permission(browser: Browser):
    context = browser.new_context(
        geolocation={"longitude": 41.890221, "latitude": 12.492348},
        permissions=["geolocation"],
    )
    page = context.new_page()
    page.goto((FIXTURES / "emulation.html").as_uri())

    expect(page.get_by_test_id("geolocation")).to_have_text("12.4923, 41.8902")

    context.set_geolocation({"longitude": 48.858455, "latitude": 2.294474})

    page.reload()

    expect(page.get_by_test_id("geolocation")).to_have_text("2.2945, 48.8585")

    context.close()


def test_color_scheme_and_media(browser: Browser):
    context = browser.new_context(color_scheme="dark")
    page = context.new_page()
    page.goto((FIXTURES / "emulation.html").as_uri())

    expect(page.get_by_test_id("color-scheme")).to_have_text("dark")

    page.emulate_media(color_scheme="light")
    page.reload()

    expect(page.get_by_test_id("color-scheme")).to_have_text("light")

    context.close()


def test_user_agent(browser: Browser):
    context = browser.new_context(user_agent="My user agent")
    page = context.new_page()
    page.goto((FIXTURES / "emulation.html").as_uri())

    expect(page.get_by_test_id("user-agent")).to_have_text("My user agent")

    context.close()


def test_javascript_disabled(browser: Browser):
    context = browser.new_context(java_script_enabled=False)
    page = context.new_page()
    page.goto((FIXTURES / "emulation.html").as_uri())

    expect(page.get_by_test_id("noscript")).to_be_visible()

    context.close()


def test_offline(browser: Browser):
    context = browser.new_context(offline=True)
    page = context.new_page()

    with pytest.raises(Error):
        page.goto("https://playwright.dev")

    context.close()
