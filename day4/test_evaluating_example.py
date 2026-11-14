from pathlib import Path

from playwright.sync_api import Page, expect

FIXTURES = Path(__file__).parent / "fixtures"


def open_fixture(page: Page, file_name: str) -> None:
    page.goto((FIXTURES / file_name).as_uri())


def test_evaluate_returns_href(page: Page):
    open_fixture(page, "evaluate.html")

    href = page.evaluate("() => document.location.href")

    assert href.endswith("evaluate.html")


def test_evaluate_with_argument(page: Page):
    open_fixture(page, "evaluate.html")

    assert page.evaluate("num => num", 42) == 42
    assert page.evaluate("array => array.length", [1, 2, 3]) == 3
    assert page.evaluate("object => object.foo", {"foo": "bar"}) == "bar"


def test_evaluate_handle(page: Page):
    open_fixture(page, "evaluate.html")

    button = page.evaluate_handle("window.button1")

    text = page.evaluate("button => button.textContent", button)

    assert text == "First"

    assert button.evaluate("(button, from) => button.textContent.substring(from)", 0) == "First"


def test_evaluate_two_handles(page: Page):
    open_fixture(page, "evaluate.html")

    button1 = page.evaluate_handle("window.button1")
    button2 = page.evaluate_handle("window.button2")

    text = page.evaluate(
        """({ button1, button2 }) => button1.textContent + " " + button2.textContent""",
        {"button1": button1, "button2": button2},
    )

    assert text == "First Second"


def test_init_script(page: Page):
    page.add_init_script("window.greeting = 'Hello from init script'")

    open_fixture(page, "evaluate.html")

    assert page.evaluate("() => window.greeting") == "Hello from init script"


def test_expose_function(page: Page):
    received = []

    page.expose_function("callApp", lambda message: received.append(message))
    open_fixture(page, "evaluate.html")

    page.get_by_role("button", name="Call app").click()

    expect(page.get_by_test_id("result")).to_have_text("empty")

    assert received == ["hello from page"]
