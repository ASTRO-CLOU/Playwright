from playwright.sync_api import Page, expect


def test_aria_snapshot_of_page(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/aria.html")

    expect(page.locator("header")).to_match_aria_snapshot(
        """
        - banner:
          - heading "Мои задачи" [level=1]
          - link "Фрукты":
            - /url: mock.html
        """
    )


def test_aria_snapshot_of_list(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/aria.html")

    expect(page.locator("main ul")).to_match_aria_snapshot(
        """
        - list:
          - listitem: Задача B
        """
    )


def test_aria_snapshot_partial_form(page: Page, fixture_url: str):
    page.goto(f"{fixture_url}/aria.html")

    expect(page.locator("form")).to_match_aria_snapshot(
        """
        - textbox "Name"
        """
    )
