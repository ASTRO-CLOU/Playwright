from playwright.sync_api import Page, Route, expect


def test_mock_the_fruit_api(page: Page, fixture_url: str):
    def handle(route: Route):
        route.fulfill(json=[{"name": "Strawberry", "id": 21}])

    page.route("**/api/v1/fruits", handle)
    page.goto(f"{fixture_url}/mock.html")

    expect(page.get_by_text("Strawberry")).to_be_visible()


def test_modify_api_response(page: Page, fixture_url: str):
    def handle(route: Route):
        response = route.fetch()
        data = response.json()
        data.append({"name": "Loquat", "id": 100})
        route.fulfill(response=response, json=data)

    page.route("**/api/v1/fruits", handle)
    page.goto(f"{fixture_url}/mock.html")

    expect(page.get_by_text("Loquat", exact=True)).to_be_visible()
    expect(page.get_by_text("Banana")).to_be_visible()


def test_abort_request(page: Page, fixture_url: str):
    page.route("**/api/v1/fruits", lambda route: route.abort())
    page.goto(f"{fixture_url}/mock.html")

    expect(page.locator("#fruits li")).to_have_count(0)


def test_mock_with_status_and_headers(page: Page, fixture_url: str):
    def handle(route: Route):
        route.fulfill(status=500, content_type="application/json", body='{"error": "broken"}')

    page.route("**/api/v1/fruits", handle)
    page.goto(f"{fixture_url}/mock.html")

    expect(page.locator("#fruits li")).to_have_count(0)
