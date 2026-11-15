import re

from playwright.sync_api import Page, expect


def test_basic_navigation(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/aria.html")

    expect(page).to_have_url(re.compile(r".*/aria\.html$"))


def test_wait_for_url_after_click(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/aria.html")

    page.get_by_role("link", name="Фрукты").click()
    page.wait_for_url("**/mock.html")

    expect(page.get_by_role("heading", level=1)).to_have_text("Фрукты")


def test_back_forward_and_reload(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/aria.html")
    page.goto(f"{fixture_url}/locators_ext.html")

    page.go_back()
    expect(page).to_have_title("Aria")

    page.go_forward()
    expect(page).to_have_title("Day5 locators")

    page.reload()
    expect(page).to_have_title("Day5 locators")


def test_load_states(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/aria.html", wait_until="domcontentloaded")
    page.wait_for_load_state("load")

    expect(page.get_by_role("heading", level=1)).to_be_visible()
    assert page.evaluate("() => document.readyState") == "complete"
