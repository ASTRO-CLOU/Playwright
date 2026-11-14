from pathlib import Path

from playwright.sync_api import Browser, Page, expect

FIXTURES = Path(__file__).parent / "fixtures"


def test_sign_in_before_each_test(page: Page, base_url: str) -> None:
    page.goto(f"{base_url}/login")

    page.get_by_label("Username").fill("student")
    page.get_by_label("Password").fill("secret")
    page.get_by_role("button", name="Sign in").click()

    expect(page.get_by_role("heading")).to_have_text("Welcome, student")


def test_reuse_signed_in_state(browser: Browser, base_url: str, tmp_path: Path) -> None:
    state_path = tmp_path / "state.json"

    first_context = browser.new_context()
    first_page = first_context.new_page()
    first_page.goto(f"{base_url}/login")
    first_page.get_by_label("Username").fill("student")
    first_page.get_by_label("Password").fill("secret")
    first_page.get_by_role("button", name="Sign in").click()
    expect(first_page.get_by_role("heading")).to_have_text("Welcome, student")

    first_context.storage_state(path=state_path)
    first_context.close()

    second_context = browser.new_context(storage_state=state_path)
    second_page = second_context.new_page()
    second_page.goto(f"{base_url}/profile")

    expect(second_page.get_by_role("heading")).to_have_text("Welcome, student")

    second_context.close()
