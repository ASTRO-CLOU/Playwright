# Практическая работа: Playwright на Python

Петрин Андрей Андреевич

Документация, по которой делаю работу: https://playwright.dev/python/docs

## День 1, 11.11.2026

Начал с раздела "Installation" на странице https://playwright.dev/python/docs/intro.

Установил Playwright, pytest и плагин pytest-playwright через uv, потом скачал
браузер Chromium командой `uv run playwright install chromium`.

### Первый тест

Взял пример из раздела "Add Example Test" и запустил его командой
`uv run pytest day1/test_example.py`. Тест открывает сайт playwright.dev,
проверяет заголовок вкладки, потом нажимает ссылку "Get started" и проверяет,
что на новой странице есть заголовок "Installation".

Оба теста прошли:

```
day1/test_example.py::test_has_title[chromium] PASSED
day1/test_example.py::test_get_started_link[chromium] PASSED
======================== 2 passed in 2.98s =========================
```

Скриншот запуска тестов: `docs/screens/day1_test.PNG`

Потом я переделал этот пример:

1. В первом тесте добавил проверку, что открылся нужный адрес страницы.
2. Во втором тесте после нажатия ссылки тоже добавил проверку адреса.
3. Добавил свой третий тест: проверяет, что ссылка "Get started" вообще есть
   на главной странице.

Зачем: тесты из документации проверяют только текст на странице. Мои ещё
смотрят на адрес, поэтому если что-то сломается, будет понятнее, что именно.

При первом запуске два моих теста упали, и я понял две вещи:

- если передать в `to_have_title` обычную строку "Playwright", Playwright ищет
  точное совпадение и тест падает, потому что настоящий заголовок длиннее;
  поэтому `re.compile` в этом месте я оставил;
- сайт после нажатия "Get started" открывает адрес `https://playwright.dev/docs/intro`,
  а не `/python/docs/intro`.

После исправлений все три теста прошли:

```
day1/test_example_modified.py::test_has_title[chromium] PASSED
day1/test_example_modified.py::test_get_started_link[chromium] PASSED
day1/test_example_modified.py::test_get_started_link_is_visible[chromium] PASSED
======================== 3 passed in 5.26s =========================
```

### Пример со скриптом

Ещё я взял пример из раздела "Usage" на странице
https://playwright.dev/python/docs/library и запустил его как есть. Этот код
не использует pytest: он сам запускает браузер, открывает сайт playwright.dev
и печатает заголовок страницы.

```
Fast and reliable end-to-end testing for modern web apps | Playwright
```

Потом переделал и его:

1. Добавил ожидание, пока страница загрузится полностью, и только после этого
   читаю заголовок.
2. Вместо печати заголовка поставил проверку, что в заголовке есть слово
   "Playwright". Если слова нет, скрипт остановится с ошибкой.
3. Браузер теперь закрывается в блоке finally. Так он закроется в любом случае
   и не останется висеть в памяти.

Зачем это нужно: первый вариант просто показывал заголовок, а второй проверяет,
что страница открылась правильно, и всегда закрывает браузер.

Скриншот этого запуска: `docs/screens/day1.PNG`

## Что лежит в папке

- `day1/test_example.py` — тест из документации как есть.
- `day1/test_example_modified.py` — мой переделанный тест.
- `day1/pytest_run.log` — вывод запуска обоих тестов.
- `day1/copied_example.py` — скрипт из документации как есть.
- `day1/modified_example.py` — мой переделанный скрипт.
- `day1/run.log` — вывод запуска обоих скриптов.
- `docs/screens` — скриншоты запуска.
