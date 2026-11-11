# ФИО: Петрин Андрей Андреевич
# Дата: 2026-11-11
# Время: 17:26
# Источник: https://playwright.dev/python/docs/library — раздел "Usage"
# Описание: пример скопирован из документации без изменений.
# Скрипт запускает браузер Chromium, открывает сайт playwright.dev
# и печатает заголовок страницы в консоль.

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # sync_playwright() поднимает драйвер Playwright,
    # оператор with гарантирует его корректную остановку в конце блока.
    browser = p.chromium.launch()  # запуск Chromium в headless-режиме (без окна)
    page = browser.new_page()      # новая вкладка — с неё и идёт вся работа
    page.goto("https://playwright.dev")  # переход по адресу, ждём события load
    print(page.title())            # читаем <title> открытой страницы и печатаем
    browser.close()                # закрываем браузер, освобождаем процессы
