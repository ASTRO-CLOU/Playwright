from pathlib import Path

from playwright.sync_api import Page, expect

FIXTURES = Path(__file__).parent / "fixtures"


def test_profile_is_closed_without_cookie(page: Page, base_url: str) -> None:
    page.goto(f"{base_url}/profile")

    expect(page.get_by_role("heading")).to_have_text("Please sign in")


def test_wrong_password_keeps_the_user_out(page: Page, base_url: str) -> None:
    page.goto(f"{base_url}/login")

    page.get_by_label("Username").fill("student")
    page.get_by_label("Password").fill("wrong")
    page.get_by_role("button", name="Sign in").click()

    expect(page.get_by_role("heading")).to_have_text("Wrong password")


def test_cookie_from_login_opens_the_profile(page: Page, base_url: str) -> None:
    page.goto(f"{base_url}/login")

    page.get_by_label("Username").fill("student")
    page.get_by_label("Password").fill("secret")
    page.get_by_role("button", name="Sign in").click()

    expect(page).to_have_url(f"{base_url}/profile")
    expect(page.get_by_role("heading")).to_have_text("Welcome, student")

    cookies = page.context.cookies()
    names = [cookie["name"] for cookie in cookies]

    assert "session" in names
