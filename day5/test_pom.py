from playwright.sync_api import Page, expect

from day5.models.task_page import TaskPage


def test_page_object_opens_page(page: Page, fixture_url: str):
    task_page = TaskPage(page, fixture_url)
    task_page.open()

    expect(task_page.submit_button).to_be_visible()


def test_page_object_fills_form(page: Page, fixture_url: str):
    task_page = TaskPage(page, fixture_url)
    task_page.open()
    task_page.submit_name("Петрин Андрей")

    expect(task_page.name_input).to_have_value("Петрин Андрей")


def test_page_object_reads_list(page: Page, fixture_url: str):
    task_page = TaskPage(page, fixture_url)
    task_page.open()

    assert task_page.item_texts() == ["Задача A", "Задача B"]
