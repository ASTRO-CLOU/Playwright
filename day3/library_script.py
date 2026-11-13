import asyncio

from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

SCREENSHOT_PATH = "docs/screens/day3_webkit.png"


def usage_example() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://playwright.dev")
        print("Usage:", page.title())
        browser.close()


def first_script_example() -> None:
    with sync_playwright() as p:
        browser = p.webkit.launch()
        page = browser.new_page()
        page.goto("https://playwright.dev/")
        page.screenshot(path=SCREENSHOT_PATH)
        print("First script: скриншот сохранён в", SCREENSHOT_PATH)
        browser.close()


def repl_style_example() -> None:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto("https://playwright.dev/")
    print("REPL:", page.title())
    page.wait_for_timeout(300)
    browser.close()
    playwright.stop()


async def async_example() -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://playwright.dev")
        print("Async:", await page.title())
        await browser.close()


if __name__ == "__main__":
    usage_example()
    first_script_example()
    repl_style_example()
    asyncio.run(async_example())
