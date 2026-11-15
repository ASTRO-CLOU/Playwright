from playwright.sync_api import Browser, BrowserContext, Page, expect


def test_two_isolated_contexts(browser: Browser, fixture_url: str):
    admin_context = browser.new_context()
    user_context = browser.new_context()

    admin_page = admin_context.new_page()
    user_page = user_context.new_page()

    admin_page.goto(f"{fixture_url}/aria.html")
    admin_page.evaluate("() => localStorage.setItem('role', 'admin')")

    user_page.goto(f"{fixture_url}/aria.html")
    assert user_page.evaluate("() => localStorage.getItem('role')") is None

    admin_context.close()
    user_context.close()


def test_cookies_do_not_leak(browser: Browser, fixture_url: str):
    first_context = browser.new_context()
    second_context = browser.new_context()

    first_context.add_cookies([{"name": "session", "value": "ok", "url": fixture_url}])
    first_page = first_context.new_page()
    second_page = second_context.new_page()

    first_page.goto(f"{fixture_url}/aria.html")
    second_page.goto(f"{fixture_url}/aria.html")

    assert first_page.evaluate("() => document.cookie") == "session=ok"
    assert second_page.evaluate("() => document.cookie") == ""

    first_context.close()
    second_context.close()


def test_several_pages_in_one_context(context: BrowserContext, fixture_url: str):
    first_page = context.new_page()
    second_page = context.new_page()

    first_page.goto(f"{fixture_url}/aria.html")
    second_page.goto(f"{fixture_url}/locators_ext.html")

    expect(first_page.get_by_role("heading", level=1)).to_have_text("Мои задачи")
    expect(second_page).to_have_title("Day5 locators")
    assert len(context.pages) == 2


def test_shared_storage_state(page: Page, browser: Browser, context: BrowserContext, fixture_url: str):
    page.goto(f"{fixture_url}/aria.html")
    page.evaluate("() => localStorage.setItem('theme', 'dark')")

    state = context.storage_state()
    other_context = browser.new_context(storage_state=state)
    other_page = other_context.new_page()
    other_page.goto(f"{fixture_url}/aria.html")

    assert other_page.evaluate("() => localStorage.getItem('theme')") == "dark"
    other_context.close()
