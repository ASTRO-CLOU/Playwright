from playwright.sync_api import BrowserContext, Page, expect


def test_multiple_pages(context: BrowserContext, fixture_url: str):
    page_one = context.new_page()
    page_two = context.new_page()

    page_one.goto(f"{fixture_url}/aria.html")
    page_two.goto(f"{fixture_url}/popup.html")

    expect(page_one).to_have_title("Aria")
    expect(page_two).to_have_title("Popup")
    assert len(context.pages) == 2


def test_handling_new_page(page: Page, context: BrowserContext, fixture_url: str):
    page.goto(f"{fixture_url}/locators_ext.html")

    with context.expect_page() as new_page_info:
        page.get_by_text("open new tab").click()

    new_page = new_page_info.value
    new_page.wait_for_load_state()
    expect(new_page.get_by_role("heading")).to_have_text("Popup page")
    new_page.close()


def test_page_event(context: BrowserContext, fixture_url: str):
    opened = []
    context.on("page", lambda new_page: opened.append(new_page))

    second_page = context.new_page()
    second_page.goto(f"{fixture_url}/popup.html")

    assert len(opened) == 1
    assert opened[0].url.endswith("/popup.html")
