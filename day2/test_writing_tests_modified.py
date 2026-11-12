import re

import pytest
from playwright.sync_api import Page, expect

DOCS_URL = "https://playwright.dev/python/docs"

DOC_PAGES = [
    ("/intro", "Installation"),
    ("/writing-tests", "Writing tests"),
    ("/locators", "Locators"),
]


@pytest.fixture(scope="function", autouse=True)
def open_docs_home(page: Page):
    page.goto(DOCS_URL + "/intro")
    expect(page).to_have_title(re.compile("Playwright"))
    yield
    print("page closed with the test")


@pytest.mark.parametrize(("path", "heading"), DOC_PAGES)
def test_docs_page_has_heading(page: Page, path: str, heading: str):
    page.goto(DOCS_URL + path)

    expect(page.get_by_role("heading", level=1)).to_have_text(heading)


def test_sidebar_has_locators_link(page: Page):
    locators_link = page.get_by_role("link", name="Locators", exact=True)

    expect(locators_link.first).to_be_visible()


def test_installation_page_has_commands(page: Page):
    page.goto(DOCS_URL + "/intro")

    expect(page.get_by_text("pip install pytest-playwright").first).to_be_visible()


def test_page_isolation(page: Page):
    page.goto(DOCS_URL + "/intro")
    page.evaluate("window.localStorage.setItem('key', 'value')")

    expect(page).to_have_url(DOCS_URL + "/intro")


def test_another_page_is_isolated(page: Page):
    page.goto(DOCS_URL + "/intro")

    assert page.evaluate("window.localStorage.getItem('key')") is None
