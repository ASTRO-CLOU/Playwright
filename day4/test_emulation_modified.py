from pathlib import Path

from playwright.sync_api import Browser, Page, expect

FIXTURES = Path(__file__).parent / "fixtures"


def test_iphone_with_own_user_agent(browser: Browser):
    context = browser.new_context(
        viewport={"width": 390, "height": 664},
        device_scale_factor=3,
        is_mobile=True,
        has_touch=True,
        user_agent="Practice iPhone",
    )
    page = context.new_page()
    page.goto((FIXTURES / "emulation.html").as_uri())

    expect(page.get_by_test_id("viewport")).to_have_text("390x664")
    expect(page.get_by_test_id("user-agent")).to_have_text("Practice iPhone")

    context.close()


def test_permissions_can_be_granted_and_cleared(page: Page, base_url: str):
    page.goto(f"{base_url}/ui")

    page.context.grant_permissions(["geolocation"], origin=base_url)
    page.context.clear_permissions()

    expect(page.get_by_role("heading", name="Issues")).to_be_visible()


def test_forced_colors_and_reduced_motion(browser: Browser):
    context = browser.new_context(reduced_motion="reduce", forced_colors="active")
    page = context.new_page()
    page.goto((FIXTURES / "emulation.html").as_uri())

    expect(page.get_by_test_id("color-scheme")).to_be_visible()

    context.close()
