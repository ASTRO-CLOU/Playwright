import datetime
from pathlib import Path

from playwright.sync_api import Page, expect

FIXTURES = Path(__file__).parent / "fixtures"
SCREENS = Path(__file__).parent.parent / "docs" / "screens"


def test_clock_screenshot_with_fixed_time(page: Page):
    page.clock.set_fixed_time(datetime.datetime(2024, 2, 2, 10, 0, 0))
    page.goto((FIXTURES / "clock.html").as_uri())

    expect(page.get_by_test_id("current-time")).to_have_text("2/2/2024, 10:00:00 AM")

    page.screenshot(path=str(SCREENS / "day4_clock.png"))


def test_activity_resets_the_logout_timer(page: Page):
    page.clock.install()
    page.goto((FIXTURES / "clock.html").as_uri())

    page.clock.fast_forward("04:00")
    page.get_by_role("button").click()
    page.clock.fast_forward("04:00")

    expect(page.get_by_text("You have been logged out due to inactivity.")).to_be_hidden()

    page.clock.fast_forward("02:00")

    expect(page.get_by_text("You have been logged out due to inactivity.")).to_be_visible()


def test_timer_keeps_running_after_pause(page: Page):
    page.clock.install(time=datetime.datetime(2024, 2, 2, 9, 0, 0))
    page.goto((FIXTURES / "clock.html").as_uri())
    locator = page.get_by_test_id("current-time")

    page.clock.run_for(3000)

    expect(locator).to_have_text("2/2/2024, 9:00:03 AM")
