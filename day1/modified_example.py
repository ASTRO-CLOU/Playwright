# ФИО: Петрин Андрей Андреевич
# Дата: 2026-11-11
# Время: 17:31
# Источник: https://playwright.dev/python/docs/library — раздел "Usage"
# Описание: тот же пример из документации, но доработанный.
#
# Что изменено (примерно 25% строк исходного скрипта):
# 1. Добавлено явное ожидание page.wait_for_load_state("load") —
#    страница гарантированно догружена перед чтением заголовка.
# 2. print(page.title()) заменён на проверку assert: скрипт падает,
#    если в заголовке нет слова "Playwright".
# 3. Браузер закрывается в finally — даже если assert не прошёл,
#    процесс Chromium не останется висеть.
# Зачем: исходный пример только печатал заголовок. Мой вариант ведёт себя
# как тест — проверяет результат и всегда освобождает ресурсы.

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    try:
        page = browser.new_page()
        page.goto("https://playwright.dev")
        page.wait_for_load_state("load")  # добавлено: ждём полной загрузки
        title = page.title()
        print(f"Заголовок страницы: {title}")  # добавлено: печать для лога
        assert "Playwright" in title, f"Ожидалось 'Playwright' в заголовке, получено: {title}"  # изменено
    finally:
        browser.close()  # изменено: закрытие гарантировано
