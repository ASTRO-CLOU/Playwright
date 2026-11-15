from playwright.sync_api import Page, expect


def test_js_handle_window(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/locators_ext.html")

    js_handle = page.evaluate_handle("window")
    assert js_handle.evaluate("(w) => w.document.title") == "Day5 locators"
    js_handle.dispose()


def test_element_handle_properties(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/locators_ext.html")

    element_handle = page.wait_for_selector("#box")
    bounding_box = element_handle.bounding_box()
    assert bounding_box["width"] == 100

    style = element_handle.get_attribute("style")
    assert "height: 100px" in style


def test_handle_as_parameter(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/locators_ext.html")

    my_array_handle = page.evaluate_handle("() => { window.myArray = [1]; return window.myArray; }")
    assert page.evaluate("(a) => a.length", my_array_handle) == 1

    page.evaluate("(arg) => arg.myArray.push(arg.newElement)", {"myArray": my_array_handle, "newElement": 2})
    assert page.evaluate("(a) => a.length", my_array_handle) == 2

    my_array_handle.dispose()


def test_element_handle_from_selector(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/locators_ext.html")

    box_handle = page.evaluate_handle("() => document.querySelector('#box')")
    element_handle = box_handle.as_element()

    assert element_handle is not None
    assert element_handle.bounding_box()["width"] == 100
