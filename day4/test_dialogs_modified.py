from pathlib import Path

from playwright.sync_api import Page, expect

FIXTURES = Path(__file__).parent / "fixtures"


def test_dialog_type_and_message(page: Page):
    page.goto((FIXTURES / "dialogs.html").as_uri())

    seen = {}

    def handle_dialog(dialog):
        seen["type"] = dialog.type
        seen["message"] = dialog.message
        dialog.dismiss()

    page.on("dialog", handle_dialog)

    page.get_by_role("button", name="Confirm").click()
    expect(page.get_by_test_id("result")).to_have_text("dismissed")

    assert seen["type"] == "confirm"
    assert seen["message"] == "Are you sure?"


def test_once_listener_answers_one_prompt(page: Page):
    page.goto((FIXTURES / "dialogs.html").as_uri())

    page.once("dialog", lambda dialog: dialog.accept("2021"))

    page.get_by_role("button", name="Prompt").click()
    expect(page.get_by_test_id("result")).to_have_text("2021")


def test_dialog_is_dismissed_without_a_listener(page: Page):
    page.goto((FIXTURES / "dialogs.html").as_uri())

    page.get_by_role("button", name="Confirm").click()

    expect(page.get_by_test_id("result")).to_have_text("dismissed")
