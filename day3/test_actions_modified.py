from pathlib import Path

from playwright.sync_api import Page, expect

FIXTURES = Path(__file__).parent / "fixtures"
FILES = Path(__file__).parent / "files"
SCREENS = Path(__file__).parent.parent / "docs" / "screens"


def open_fixture(page: Page, file_name: str) -> None:
    page.goto((FIXTURES / file_name).as_uri())


def fill_order_form(page: Page) -> None:
    page.get_by_label("Name").fill("Андрей")
    page.get_by_label("Birth date").fill("2000-05-12")
    page.get_by_label("Choose a color").select_option(label="Blue")
    page.get_by_label("I agree to the terms above").check()


def test_order_form_is_filled(page: Page):
    open_fixture(page, "actions_form.html")

    fill_order_form(page)

    expect(page.get_by_label("Name")).to_have_value("Андрей")
    expect(page.get_by_label("Birth date")).to_have_value("2000-05-12")
    expect(page.get_by_label("Choose a color")).to_have_value("blue")
    expect(page.get_by_label("I agree to the terms above")).to_be_checked()


def test_order_form_screenshot(page: Page):
    open_fixture(page, "actions_form.html")

    fill_order_form(page)
    page.get_by_label("Name").blur()

    page.screenshot(path=str(SCREENS / "day3_order_form.png"), full_page=True)


def test_multiple_selected_colors(page: Page):
    open_fixture(page, "actions_form.html")

    colors = page.get_by_label("Choose multiple colors")
    colors.select_option(["red", "blue"])

    expect(colors).to_have_values(["red", "blue"])


def test_uploaded_file_name(page: Page):
    open_fixture(page, "actions_form.html")

    upload = page.get_by_label("Upload file", exact=True)
    upload.set_input_files(
        files=[
            {
                "name": "order.txt",
                "mimeType": "text/plain",
                "buffer": b"order 42",
            }
        ],
    )

    file_names = upload.evaluate("input => Array.from(input.files).map(f => f.name)")
    assert file_names == ["order.txt"]


def test_upload_from_disk_and_clear(page: Page):
    open_fixture(page, "actions_form.html")

    upload = page.get_by_label("Upload files")
    upload.set_input_files([str(FILES / "file1.txt"), str(FILES / "file2.txt")])

    file_count = upload.evaluate("input => input.files.length")
    assert file_count == 2

    upload.set_input_files([])
    assert upload.evaluate("input => input.files.length") == 0


def test_keyboard_focus_moves_to_button(page: Page):
    open_fixture(page, "actions_typing.html")

    name_field = page.locator("#name")
    name_field.press_sequentially("Андрей", delay=30)

    page.keyboard.press("Tab")

    focused_tag = page.evaluate("document.activeElement.tagName")
    assert focused_tag == "BUTTON"


def test_drag_and_drop_with_screenshot(page: Page):
    open_fixture(page, "actions_mouse.html")

    page.locator("#item-to-be-dragged").drag_to(page.locator("#item-to-drop-at"))

    expect(page.locator("#item-to-drop-at")).to_have_text("Dropped: dragged item")

    page.screenshot(path=str(SCREENS / "day3_drag_drop.png"))


def test_scroll_to_footer(page: Page):
    open_fixture(page, "actions_mouse.html")

    page.get_by_text("Footer text").scroll_into_view_if_needed()

    expect(page.get_by_text("Footer text")).to_be_in_viewport()

    scroll_y = page.evaluate("window.scrollY")
    assert scroll_y > 0
