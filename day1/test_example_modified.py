# ФИО: Петрин Андрей Андреевич
# Дата: 2026-11-11
# Время: 19:20
# Источник: https://playwright.dev/python/docs/intro — раздел "Add Example Test"
# Описание: тот же тест из документации, но доработанный.
#
# Что изменено (около 25% кода):
# 1. В первом тесте добавил проверку адреса страницы: expect(page).to_have_url.
#    Заголовок может совпасть, а адрес — нет, теперь тест это заметит.
# 2. Во втором тесте после нажатия ссылки добавил проверку адреса страницы.
# 3. Добавил третий тест: проверяю, что на главной есть ссылка "Get started"
#    до нажатия. Если главная сломается, это будет видно сразу.
# Зачем: исходные тесты проверяют только текст на странице. Мои ещё смотрят
# на адрес, поэтому при ошибке будет понятнее, что именно сломалось.
#
# Что выяснилось при первом запуске: если передать в to_have_title обычную
# строку "Playwright", Playwright ищет точное совпадение и тест падает,
# потому что настоящий заголовок длиннее. Поэтому re.compile оставил.

import re
from playwright.sync_api import Page, expect


def test_has_title(page: Page):
    page.goto("https://playwright.dev/")

    expect(page).to_have_title(re.compile("Playwright"))
    expect(page).to_have_url("https://playwright.dev/")  # добавлено


def test_get_started_link(page: Page):
    page.goto("https://playwright.dev/")

    page.get_by_role("link", name="Get started").click()

    expect(page.get_by_role("heading", name="Installation")).to_be_visible()
    expect(page).to_have_url("https://playwright.dev/docs/intro")  # добавлено


def test_get_started_link_is_visible(page: Page):  # добавлено: новый тест
    page.goto("https://playwright.dev/")

    expect(page.get_by_role("link", name="Get started")).to_be_visible()
