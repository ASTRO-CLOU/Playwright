from playwright.sync_api import Page, expect


class TaskPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.name_input = page.get_by_label("Name")
        self.submit_button = page.get_by_role("button", name="Submit")
        self.items = page.locator("main ul li")

    def open(self):
        self.page.goto(f"{self.base_url}/aria.html")
        expect(self.page.get_by_role("heading", name="Мои задачи")).to_be_visible()

    def submit_name(self, name: str):
        self.name_input.fill(name)
        self.submit_button.click()

    def item_texts(self):
        return self.items.all_text_contents()
