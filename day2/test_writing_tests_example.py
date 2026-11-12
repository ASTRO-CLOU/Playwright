import re

import pytest
from playwright.sync_api import Page, expect


def test_navigation_and_interaction(page: Page):
    page.goto("https://playwright.dev/")

    get_started = page.get_by_role("link", name="Get started")

    get_started.click()

    expect(page.get_by_role("heading", name="Installation")).to_be_visible()


def test_assertion_waits_for_expected_state(page: Page):
    page.goto("https://playwright.dev/")

    expect(page).to_have_title(re.compile("Playwright"))
    expect(page).to_have_url(re.compile("playwright.dev"))


def test_example_test(page: Page):
    pass


def test_another_test(page: Page):
    pass


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    print("before the test runs")

    page.goto("https://playwright.dev/")
    yield

    print("after the test runs")


def test_main_navigation(page: Page):
    expect(page).to_have_url("https://playwright.dev/")
