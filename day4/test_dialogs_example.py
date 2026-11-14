from pathlib import Path

from playwright.sync_api import Page, expect

FIXTURES = Path(__file__).parent / "fixtures"


def open_fixture(page: Page, file_name: str) -> None:
    page.goto((FIXTURES / file_name).as_uri())


def test_alert_dialog(page: Page):
    open_fixture(page, "dialogs.html")

    page.on("dialog", lambda dialog: dialog.accept())

    page.get_by_role("button", name="Alert").click()


def test_confirm_accepted(page: Page):
    open_fixture(page, "dialogs.html")

    page.on("dialog", lambda dialog: dialog.accept())

    page.get_by_role("button", name="Confirm").click()

    expect(page.get_by_test_id("result")).to_have_text("accepted")


def test_dialog_message(page: Page):
    open_fixture(page, "dialogs.html")

    messages = []

    def handle_dialog(dialog):
        messages.append(dialog.message)
        dialog.dismiss()

    page.on("dialog", handle_dialog)

    page.get_by_role("button", name="Alert").click()

    assert messages == ["Please enter your password"]


def test_prompt_with_accept(page: Page):
    open_fixture(page, "dialogs.html")

    page.on("dialog", lambda dialog: dialog.accept("2021"))

    page.get_by_role("button", name="Prompt").click()

    expect(page.get_by_test_id("result")).to_have_text("2021")


def test_beforeunload_dialog(page: Page):
    open_fixture(page, "beforeunload.html")

    def handle_dialog(dialog):
        assert dialog.type == "beforeunload"
        dialog.dismiss()

    page.on("dialog", handle_dialog)
    page.close(run_before_unload=True)
