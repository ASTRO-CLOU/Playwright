# ФИО: Петрин Андрей Андреевич
# Дата: 2026-11-11
# Время: 19:05
# Источник: https://playwright.dev/python/docs/intro — раздел "Add Example Test"
# Описание: тест скопирован из документации без изменений.
# Первая проверка открывает сайт playwright.dev и убеждается, что в заголовке
# вкладки есть слово Playwright. Вторая проверка нажимает ссылку "Get started"
# и убеждается, что на новой странице виден заголовок "Installation".

import re
from playwright.sync_api import Page, expect

# page — готовая вкладка браузера, её выдаёт плагин pytest-playwright,
# самому открывать браузер не нужно.
def test_has_title(page: Page):
    page.goto("https://playwright.dev/")  # открываем главную страницу сайта

    # Expect a title "to contain" a substring.
    # expect — проверка, которая сама подождёт нужного результата
    # и упадёт, если за отведённое время условие не выполнится.
    expect(page).to_have_title(re.compile("Playwright"))

def test_get_started_link(page: Page):
    page.goto("https://playwright.dev/")

    # Click the get started link.
    # get_by_role ищет ссылку по её роли и тексту — так же, как её видит человек.
    page.get_by_role("link", name="Get started").click()

    # Expects page to have a heading with the name of Installation.
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()
