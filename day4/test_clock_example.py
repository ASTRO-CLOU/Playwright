import datetime
from pathlib import Path

from playwright.sync_api import Page, expect

FIXTURES = Path(__file__).parent / "fixtures"
SCREENS = FIXTURES.parent.parent / "docs" / "screens"


def test_predefined_time(page: Page):
    page.clock.set_fixed_time(datetime.datetime(2024, 2, 2, 10, 0, 0))
    page.goto((FIXTURES / "clock.html").as_uri())

    expect(page.get_by_test_id("current-time")).to_have_text("2/2/2024, 10:00:00 AM")

    page.clock.set_fixed_time(datetime.datetime(2024, 2, 2, 10, 30, 0))

    expect(page.get_by_test_id("current-time")).to_have_text("2/2/2024, 10:30:00 AM")


def test_consistent_time_and_timers(page: Page):
    page.clock.install(time=datetime.datetime(2024, 2, 2, 8, 0, 0))
    page.goto((FIXTURES / "clock.html").as_uri())

    page.clock.pause_at(datetime.datetime(2024, 2, 2, 10, 0, 0))

    expect(page.get_by_test_id("current-time")).to_have_text("2/2/2024, 10:00:00 AM")

    page.clock.fast_forward("30:00")

    expect(page.get_by_test_id("current-time")).to_have_text("2/2/2024, 10:30:00 AM")


def test_inactivity_monitoring(page: Page):
    page.clock.install()
    page.goto((FIXTURES / "clock.html").as_uri())
    page.get_by_role("button").click()

    page.clock.fast_forward("05:00")

    expect(page.get_by_text("You have been logged out due to inactivity.")).to_be_visible()


def test_tick_through_time_manually(page: Page):
    page.clock.install(time=datetime.datetime(2024, 2, 2, 8, 0, 0))
    page.goto((FIXTURES / "clock.html").as_uri())
    locator = page.get_by_test_id("current-time")

    page.clock.pause_at(datetime.datetime(2024, 2, 2, 10, 0, 0))
    expect(locator).to_have_text("2/2/2024, 10:00:00 AM")

    page.clock.run_for(2000)

    expect(locator).to_have_text("2/2/2024, 10:00:02 AM")
