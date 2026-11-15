from playwright.sync_api import Browser, expect


def test_service_worker_blocked(browser: Browser, fixture_url: str):
    context = browser.new_context(service_workers="block")
    page = context.new_page()

    page.goto(f"{fixture_url}/sw/index.html")

    assert context.service_workers == []
    context.close()


def test_wait_for_service_worker(browser: Browser, fixture_url: str):
    context = browser.new_context()
    page = context.new_page()

    with context.expect_event("serviceworker") as worker_info:
        page.goto(f"{fixture_url}/sw/index.html")

    service_worker = worker_info.value
    assert service_worker.url.endswith("/sw.js")
    assert len(context.service_workers) == 1

    context.close()


def test_page_reports_registration(browser: Browser, fixture_url: str):
    context = browser.new_context()
    page = context.new_page()

    page.goto(f"{fixture_url}/sw/index.html")
    expect(page.locator("#status")).to_have_text("registered")

    context.close()
