import pytest
from playwright.sync_api import Error, Page, expect


def test_request_and_response_events(page: Page, fixture_url: str):
    requests = []
    responses = []

    page.on("request", lambda request: requests.append(request.url))
    page.on("response", lambda response: responses.append(response.status))

    page.goto(f"{fixture_url}/mock.html")
    expect(page.locator("#fruits li")).to_have_count(2)

    assert any("mock.html" in url for url in requests)
    assert any("/api/v1/fruits" in url for url in requests)
    assert responses.count(200) >= 1


def test_request_method_and_headers(page: Page, fixture_url: str):
    methods = []
    page.on("request", lambda request: methods.append(request.method))

    page.goto(f"{fixture_url}/aria.html")

    assert methods[0] == "GET"


def test_block_static_files(page: Page, fixture_url: str):
    page.route("**/*.css", lambda route: route.abort())
    page.route("**/*.{png,jpg,svg}", lambda route: route.abort())

    page.goto(f"{fixture_url}/aria.html")
    expect(page.get_by_role("heading", level=1)).to_be_visible()


def test_offline_mode(context, fixture_url: str):
    context.set_offline(True)
    other_page = context.new_page()

    with pytest.raises(Error):
        other_page.goto(f"{fixture_url}/aria.html")

    context.set_offline(False)
    other_page.goto(f"{fixture_url}/aria.html")
    expect(other_page.get_by_role("heading", level=1)).to_be_visible()
