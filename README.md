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

## День 2, 12.11.2026

Сегодня два раздела документации: "Writing tests"
(https://playwright.dev/python/docs/writing-tests) и "Locators"
(https://playwright.dev/python/docs/locators).

### Writing tests

Из этого раздела я взял примеры действий, проверок, изоляции тестов и своих
заготовок (fixtures). Тесты открывают сайт playwright.dev.

```
day2/test_writing_tests_example.py::test_navigation_and_interaction PASSED
day2/test_writing_tests_example.py::test_assertion_waits_for_expected_state PASSED
day2/test_writing_tests_example.py::test_example_test PASSED
day2/test_writing_tests_example.py::test_another_test PASSED
day2/test_writing_tests_example.py::test_main_navigation PASSED
```

Главное, что понял из раздела: перед каждым действием ничего ждать не нужно,
Playwright сам проверяет, что элемент готов. А проверки `expect` умеют ждать,
пока условие не выполнится, поэтому тесты не "мигают".

Ещё понял про изоляцию: каждый тест получает свою чистую вкладку, как новый
профиль браузера. Поэтому данные, которые один тест записал в localStorage, во
втором тесте уже не видны.

### Locators

Здесь вся страница документации про поиск элементов: по роли, по тексту, по
подписи к полю, по placeholder, по alt картинки, по title, по test id, по CSS
и XPath.

В документации примеры показаны на странице `localhost:3000`, которой у меня
нет. Поэтому я сделал пять своих html-страниц с тем же HTML, что в примерах
(папка `day2/fixtures`), и открываю их прямо из файла. Код из документации от
этого не меняется, он просто ищет элементы на этой странице.

Запуск всех примеров:

```
day2/test_locators_example.py — 22 теста PASSED
======================== 40 passed, 1 warning in 15.02s =========================
```

Скриншот страницы с элементами: `docs/screens/day2_fixture_page.png`
Скриншот, который сделал сам тест с фильтрами: `docs/screens/day2_chained_filter.png`

Потом я написал свои варианты и вот что изменил:

1. В поиске заголовка "Sign up" добавил `level=3` и регулярное выражение, чтобы
   не поймать другой заголовок с похожим текстом.
2. Добавил проверку своего test id: переключил атрибут с `data-testid` на
   `data-pw` через `playwright.selectors.set_test_id_attribute`, а в конце
   вернул обратно, иначе сломались бы остальные тесты.
3. Показал `locator.within`: кнопок "Save" на странице две, и только `within`
   берёт ту, что внутри окна настроек.
4. Добавил `or_`: ждём либо кнопку "New", либо окно с текстом "Confirm security
   settings", смотря что появится первым.
5. Сделал свой тест на список товаров: три товара всего, два в наличии, и это
   проверяется через `filter(has_not_text=...)`.
6. В тестах Writing tests перешёл с одного адреса на `parametrize`: три страницы
   документации проверяются одним и тем же тестом, а заголовок страницы
   сравнивается полностью.

Зачем: примеры из документации показывают по одной возможности. В своих тестах
я проверяю то, что чаще ломается на живом сайте: похожие элементы, одинаковые
кнопки в разных блоках, списки с разным набором данных.

Что заметил при запуске:

- если локатор находит несколько кнопок, Playwright не угадывает, а падает с
  ошибкой strict mode violation. Это защита от случайного клика не туда;
- `page.locator("button").visible` в Python действительно есть (проверил на
  версии 1.65.0), и он оставляет только видимые кнопки;
- текст `pip install pytest-playwright` на странице встречается дважды, поэтому
  пришлось добавить `.first`.

## Что лежит в папке

- `day1/test_example.py` — тест из документации как есть.
- `day1/test_example_modified.py` — мой переделанный тест.
- `day1/pytest_run.log` — вывод запуска обоих тестов.
- `day1/copied_example.py` — скрипт из документации как есть.
- `day1/modified_example.py` — мой переделанный скрипт.
- `day1/run.log` — вывод запуска обоих скриптов.
- `day2/test_writing_tests_example.py` — примеры из раздела Writing tests.
- `day2/test_writing_tests_modified.py` — мой вариант с parametrize.
- `day2/test_locators_example.py` — примеры локаторов из документации.
- `day2/test_locators_modified.py` — мои варианты локаторов.
- `day2/fixtures` — html-страницы с тем же HTML, что в примерах.
- `day2/pytest_run.log` — вывод запуска всех тестов дня 2.
- `docs/screens` — скриншоты страниц и запусков.
