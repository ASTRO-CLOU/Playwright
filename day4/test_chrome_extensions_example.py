from pathlib import Path
from typing import Generator

import pytest
from playwright.sync_api import BrowserContext, Error, Page, Playwright, expect

EXTENSION = Path(__file__).parent / "extension" / "my-extension"


@pytest.fixture()
def context(playwright: Playwright, tmp_path: Path) -> Generator[BrowserContext, None, None]:
    context = playwright.chromium.launch_persistent_context(
        str(tmp_path),
        channel="chromium",
        args=[
            f"--disable-extensions-except={EXTENSION}",
            f"--load-extension={EXTENSION}",
        ],
    )
    yield context
    context.close()


@pytest.fixture()
def extension_id(context: BrowserContext) -> Generator[str, None, None]:
    service_worker = context.service_workers[0] if context.service_workers else None
    if not service_worker:
        service_worker = context.wait_for_event("serviceworker")

    yield service_worker.url.split("/")[2]


def test_example_test(context: BrowserContext, page: Page) -> None:
    try:
        page.goto("https://example.com")
    except Error as error:
        pytest.skip(f"нет доступа к example.com: {error}")

    expect(page.locator("body")).to_contain_text("Changed by my-extension")


def test_popup_page(context: BrowserContext, page: Page, extension_id: str) -> None:
    page.goto(f"chrome-extension://{extension_id}/popup.html")

    expect(page.locator("body")).to_have_text("my-extension popup")
