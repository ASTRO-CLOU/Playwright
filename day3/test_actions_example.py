from pathlib import Path

from playwright.sync_api import Page, expect

FIXTURES = Path(__file__).parent / "fixtures"
FILES = Path(__file__).parent / "files"


def open_fixture(page: Page, file_name: str) -> None:
    page.goto((FIXTURES / file_name).as_uri())


def test_text_input(page: Page):
    open_fixture(page, "actions_text.html")

    page.get_by_role("textbox").fill("Peter")

    expect(page.get_by_role("textbox")).to_have_value("Peter")


def test_date_and_time_input(page: Page):
    open_fixture(page, "actions_form.html")

    page.get_by_label("Birth date").fill("2020-02-02")

    page.get_by_label("Appointment time").fill("13:15")

    page.get_by_label("Local time").fill("2020-03-02T05:15")


def test_checkboxes_and_radio_buttons(page: Page):
    open_fixture(page, "actions_form.html")

    page.get_by_label("I agree to the terms above").check()

    page.get_by_label("Subscribe to newsletter").check()
    expect(page.get_by_label("Subscribe to newsletter")).to_be_checked()

    page.get_by_label("XL").check()


def test_select_options(page: Page):
    open_fixture(page, "actions_form.html")

    page.get_by_label("Choose a color").select_option("blue")

    page.get_by_label("Choose a color").select_option(label="Blue")

    page.get_by_label("Choose multiple colors").select_option(["red", "green", "blue"])


def test_mouse_click(page: Page):
    open_fixture(page, "actions_mouse.html")

    page.get_by_role("button").click()

    page.get_by_text("Item").dblclick()

    page.get_by_text("Item").click(button="right")

    page.get_by_text("Item").click(modifiers=["Shift"])

    page.get_by_text("Item").hover()

    page.get_by_text("Item").click(position={"x": 0, "y": 0})


def test_forcing_the_click(page: Page):
    open_fixture(page, "actions_mouse.html")

    page.get_by_role("button").click(force=True)


def test_programmatic_click(page: Page):
    open_fixture(page, "actions_mouse.html")

    page.get_by_role("button").dispatch_event("click")


def test_type_characters(page: Page):
    open_fixture(page, "actions_typing.html")

    page.locator("#area").press_sequentially("Hello World!", delay=50)

    expect(page.locator("#area")).to_have_value("Hello World!")


def test_keys_and_shortcuts(page: Page):
    open_fixture(page, "actions_typing.html")

    page.get_by_text("Submit").press("Enter")

    page.locator("#name").press("Control+ArrowRight")

    page.locator("#name").press("$")

    page.locator("#name").press("Shift+A")

    page.locator("#name").press("Shift+ArrowLeft")


def test_upload_files(page: Page):
    open_fixture(page, "actions_form.html")

    page.get_by_label("Upload file", exact=True).set_input_files(str(FILES / "myfile.txt"))

    page.get_by_label("Upload files").set_input_files(
        [str(FILES / "file1.txt"), str(FILES / "file2.txt")]
    )

    page.get_by_label("Upload directory").set_input_files(str(FILES / "mydir"))

    page.get_by_label("Upload file", exact=True).set_input_files([])

    page.get_by_label("Upload file", exact=True).set_input_files(
        files=[
            {
                "name": "test.txt",
                "mimeType": "text/plain",
                "buffer": b"this is a test",
            }
        ],
    )


def test_upload_with_file_chooser(page: Page):
    open_fixture(page, "actions_form.html")

    with page.expect_file_chooser() as file_chooser_info:
        page.get_by_label("Upload file", exact=True).click()

    file_chooser = file_chooser_info.value
    file_chooser.set_files(str(FILES / "myfile.txt"))


def test_focus_element(page: Page):
    open_fixture(page, "actions_form.html")

    page.get_by_label("password").focus()

    expect(page.get_by_label("password")).to_be_focused()


def test_drag_and_drop(page: Page):
    open_fixture(page, "actions_mouse.html")

    page.locator("#item-to-be-dragged").drag_to(page.locator("#item-to-drop-at"))

    expect(page.locator("#item-to-drop-at")).to_contain_text("Dropped: dragged item")


def test_dragging_manually(page: Page):
    open_fixture(page, "actions_mouse.html")

    page.locator("#item-to-be-dragged").hover()
    page.mouse.down()
    page.locator("#item-to-drop-at").hover()
    page.locator("#item-to-drop-at").hover()
    page.mouse.up()


def test_scrolling(page: Page):
    open_fixture(page, "actions_mouse.html")

    page.get_by_role("button").click()

    page.get_by_text("Footer text").scroll_into_view_if_needed()
    expect(page.get_by_text("Footer text")).to_be_in_viewport()

    page.get_by_test_id("scrolling-container").hover()
    page.mouse.wheel(0, 10)

    page.get_by_test_id("scrolling-container").evaluate("e => e.scrollTop += 100")
    assert page.get_by_test_id("scrolling-container").evaluate("e => e.scrollTop") > 0
