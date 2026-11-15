from playwright.sync_api import Page, expect


def pan(locator, delta_x=0, delta_y=0, steps=5):
    bounds = locator.bounding_box()
    center_x = bounds["x"] + bounds["width"] / 2
    center_y = bounds["y"] + bounds["height"] / 2

    touches = [{"identifier": 0, "clientX": center_x, "clientY": center_y}]
    locator.dispatch_event(
        "touchstart",
        {"touches": touches, "changedTouches": touches, "targetTouches": touches},
    )

    for step in range(1, steps + 1):
        touches = [
            {
                "identifier": 0,
                "clientX": center_x + delta_x * step / steps,
                "clientY": center_y + delta_y * step / steps,
            }
        ]
        locator.dispatch_event(
            "touchmove",
            {"touches": touches, "changedTouches": touches, "targetTouches": touches},
        )

    locator.dispatch_event("touchend")


def test_pan_gesture(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/touch.html")

    pan(page.locator("#pad"), 100, 50, steps=3)

    expect(page.locator("#log")).to_have_text("start: 1, move: 3, end: 1")


def test_pan_gesture_in_mobile_context(browser, fixture_url: str):
    context = browser.new_context(has_touch=True, is_mobile=True, viewport={"width": 390, "height": 844})
    page = context.new_page()
    page.goto(f"{fixture_url}/touch.html")

    pan(page.locator("#pad"), 60, 60, steps=2)

    expect(page.locator("#log")).to_have_text("start: 1, move: 2, end: 1")
    context.close()
