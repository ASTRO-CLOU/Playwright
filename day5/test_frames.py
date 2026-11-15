import re

from playwright.sync_api import Page, expect


def test_frame_locator(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/frames.html")

    username = page.frame_locator(".frame-class").get_by_label("User Name")
    username.fill("John")

    expect(username).to_have_value("John")


def test_frame_object_by_name(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/frames.html")

    frame = page.frame("frame-login")
    assert frame is not None
    frame.fill("#user", "Mary")

    expect(frame.locator("#user")).to_have_value("Mary")


def test_frame_by_url(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/frames.html")

    frame = page.frame(url=re.compile(r".*frame\.html"))
    assert frame is not None
    expect(frame.get_by_role("heading")).to_have_text("Страница внутри рамки")


def test_second_frame(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/frames.html")

    send_button = page.frame_locator("#second").get_by_role("button", name="Send")
    expect(send_button).to_be_visible()
