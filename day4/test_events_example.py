from pathlib import Path

from playwright.sync_api import Page, expect

FIXTURES = Path(__file__).parent / "fixtures"


def open_fixture(page: Page, file_name: str) -> None:
    page.goto((FIXTURES / file_name).as_uri())


def test_waiting_for_request(page: Page, base_url: str):
    with page.expect_request("**/logo.png") as first:
        page.goto(f"{base_url}/static/events.html")

    print(first.value.url)


def test_waiting_for_popup(page: Page):
    open_fixture(page, "events.html")

    with page.expect_popup() as popup:
        page.get_by_text("open the popup").click()

    child_page = popup.value

    expect(child_page.get_by_role("heading")).to_have_text("Popup page")


def test_add_and_remove_listener(page: Page):
    requests: list[str] = []

    def print_request_finished(request):
        requests.append(request.url)

    page.on("requestfinished", print_request_finished)
    open_fixture(page, "events.html")

    page.remove_listener("requestfinished", print_request_finished)
    page.goto((FIXTURES / "popup.html").as_uri())

    assert len(requests) >= 1


def test_console_message(page: Page):
    open_fixture(page, "events.html")

    with page.expect_console_message() as message:
        page.get_by_role("button", name="Log message").click()

    assert message.value.text == "Button clicked"


def test_one_off_listener(page: Page):
    open_fixture(page, "dialogs.html")

    page.once("dialog", lambda dialog: dialog.accept("2021"))
    page.evaluate("prompt('Enter a number:')")
