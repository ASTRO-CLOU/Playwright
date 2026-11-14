from pathlib import Path

from playwright.sync_api import Playwright, expect

FIXTURES = Path(__file__).parent / "fixtures"
EXTENSION = Path(__file__).parent / "extension" / "my-extension"


def test_browser_type_versions(playwright: Playwright):
    versions = {}

    for browser_name in ("chromium", "firefox", "webkit"):
        browser = getattr(playwright, browser_name).launch()
        versions[browser_name] = browser.version
        browser.close()

    print(versions)

    assert versions["firefox"] != versions["webkit"]


def test_extension_popup_from_a_persistent_context(playwright: Playwright, tmp_path: Path):
    context = playwright.chromium.launch_persistent_context(
        str(tmp_path),
        channel="chromium",
        args=[
            f"--disable-extensions-except={EXTENSION}",
            f"--load-extension={EXTENSION}",
        ],
    )

    service_worker = (
        context.service_workers[0]
        if context.service_workers
        else context.wait_for_event("serviceworker")
    )
    extension_id = service_worker.url.split("/")[2]
    print(f"идентификатор расширения: {extension_id}")

    page = context.new_page()
    page.goto(f"chrome-extension://{extension_id}/popup.html")

    expect(page.locator("body")).to_have_text("my-extension popup")
    page.screenshot(path=str(FIXTURES.parent.parent / "docs" / "screens" / "day4_extension_popup.png"))

    context.close()
