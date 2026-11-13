import pytest
from playwright.sync_api import Page, expect
from pytest_playwright.pytest_playwright import CreateContextCallback


def test_typings_for_auto_completion(page: Page):
    page.goto("https://playwright.dev/python/docs/test-runners")

    expect(page.get_by_role("heading", level=1)).to_have_text("Pytest Plugin Reference")


def test_using_multiple_contexts(page: Page, new_context: CreateContextCallback) -> None:
    page.goto("https://example.com")

    context = new_context()
    page2 = context.new_page()
    page2.goto("https://example.com")

    expect(page2).to_have_title("Example Domain")
    assert page2 is not page


@pytest.mark.only_browser("chromium")
def test_only_on_chromium(page: Page):
    page.goto("https://example.com")
    assert page.title() == "Example Domain"


@pytest.mark.skip_browser("firefox")
def test_skipped_on_firefox(page: Page):
    page.goto("https://example.com")
    assert page.title() == "Example Domain"


@pytest.mark.browser_context_args(timezone_id="Europe/Berlin", locale="de-DE")
def test_browser_context_args_marker(page: Page):
    timezone_id = page.evaluate("Intl.DateTimeFormat().resolvedOptions().timeZone")
    language = page.evaluate("window.navigator.language")

    assert timezone_id == "Europe/Berlin"
    assert language == "de-DE"


def test_viewport_from_conftest(page: Page):
    assert page.viewport_size == {"width": 1280, "height": 720}


def test_session_scope_fixtures(
    browser, browser_name: str, is_chromium: bool, is_firefox: bool, is_webkit: bool
):
    assert browser.is_connected()
    assert browser_name in {"chromium", "firefox", "webkit"}
    assert sum([is_chromium, is_firefox, is_webkit]) == 1


def test_base_url_from_command_line(page: Page, base_url: str):
    if not base_url:
        pytest.skip("запускать с аргументом --base-url")

    page.goto("/python/docs/intro")

    expect(page.get_by_role("heading", level=1)).to_have_text("Installation")
