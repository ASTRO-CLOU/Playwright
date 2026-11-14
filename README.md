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

## День 3, 13.11.2026

Сегодня восемь разделов документации: Generating tests, Running and debugging
tests, Trace viewer, Setting up CI, Pytest Plugin Reference, Library, Actions,
Auto-waiting.

### Generating tests

`playwright codegen` открывает браузер и записывает то, что я в нём нажимаю,
а потом отдаёт готовый код. Записывать мне нечего: окно браузера я руками не
нажимаю, поэтому сохранил справку команды в `day3/codegen_help.log`.

Главное из раздела: кнопка "Pick Locator" подбирает локатор в том же порядке,
что я использовал в день 2 — сначала роль, потом текст, потом test id.

### Running and debugging tests

Запуски, которые я реально сделал (всё в `day3/cli_run.log`):

1. Запуск только нужных тестов по имени:
   `uv run pytest day3/test_actions_example.py -k "text_input or date_and_time" -v`
   — выбралось 2 теста из 14.
2. Запуск сразу в двух браузерах:
   `uv run pytest day3/test_pytest_plugin.py -k "only_on_chromium or viewport"
   --browser firefox --browser webkit -v` — 2 passed, 2 skipped. Пропущенные —
   это тест с маркером `only_browser("chromium")`, он в других браузерах
   честно пропускается.
3. Адрес из командной строки:
   `uv run pytest day3/test_pytest_plugin.py -k base_url
   --base-url https://playwright.dev -v` — 1 passed, в тесте короткий адрес
   `/python/docs/intro`.

```
================== 41 passed, 1 skipped, 1 warning in 16.58s ==================
```

Про `PWDEBUG=1`: в PowerShell это `$env:PWDEBUG=1`, потом `uv run pytest -s`.
Открывается Inspector, где можно идти по шагам. У меня Inspector — отдельное
окно, поэтому я его не запускал.

### Trace viewer

Запустил `uv run pytest day3/test_actions_example.py::test_text_input --tracing on`
и получил `test-results/day3-test-actions-example-py-test-text-input-chromium/trace.zip`
(32 КБ). Открыть её можно командой `uv run playwright show-trace <путь>` или
перетащить файл на сайт https://trace.playwright.dev.

### Setting up CI

Добавил `.github/workflows/playwright.yml`. Документация ставит зависимости через
`pip install -r requirements.txt`, а у меня проект на uv, поэтому в файле
`uv sync` и `uv run playwright install --with-deps chromium`.

Первый запуск упал за 7 секунд: у действия `astral-sh/setup-uv` нет тега `v10`,
только полные версии. Поставил `v10.3.3`, и workflow прошёл: 1 минута 39 секунд,
тесты зелёные (вкладка Actions на GitHub).

### Pytest Plugin Reference

Из этого раздела попробовал:

1. Переопределил `browser_context_args` в `day3/conftest.py`: размер окна
   1280x720 и язык `en-GB` — и проверил это тестом.
2. `new_context` — второй чистый контекст внутри одного теста, как отдельный
   браузер.
3. Маркеры `only_browser`, `skip_browser` и `browser_context_args`
   с `timezone_id="Europe/Berlin"`.
4. Session-фикстуры `browser_name`, `is_chromium`, `is_firefox`, `is_webkit`.
5. `--base-url` из командной строки.

Заметил ошибку в документации: в примере с часовым поясом сравнивают
`window.navigator.userAgent` со строкой "Europe/Berlin". Я сравнил часовой пояс
через `Intl.DateTimeFormat().resolvedOptions().timeZone`, а язык — отдельной
проверкой.

### Library

`day3/library_script.py` — четыре способа работы без pytest: обычный
`sync_playwright`, первый скрипт на webkit со скриншотом, запуск через
`sync_playwright().start()` (как в консоли) и асинхронный вариант. Вывод:

```
Usage: Playwright
First script: скриншот сохранён в docs/screens/day3_webkit.png
REPL: Playwright
Async: Playwright
```

Вместо `time.sleep` из раздела про известные проблемы использовал
`page.wait_for_timeout(300)`.

Скриншот из webkit: `docs/screens/day3_webkit.png`

### Actions

Проверил почти всё из раздела: заполнение текста, даты, времени,
`datetime-local`, галочки и радиокнопки, `select_option`, двойной клик, клик
правой кнопкой, клик с Shift, клик по координатам, `force=True`,
`dispatch_event`, `press_sequentially`, нажатия `Enter`, `Control+ArrowRight`,
`$`, `Shift+A`, загрузку файлов (один файл, список, папка, очистка, файл из
памяти), выбор файла через `expect_file_chooser`, `focus`, перетаскивание
мышью и вручную, прокрутку.

Что пришлось поменять из-за своих страниц:

1. Текст, даты и мышь разложил по разным html-файлам. На одной странице
   `get_by_role("textbox")` находит и поле даты, и поле пароля, и тогда
   Playwright ругается на несколько совпадений.
2. У загрузки файлов добавил `exact=True`: на странице есть и "Upload file",
   и "Upload files", а поиск по подписи находит оба.

Мой вариант: сценарий заполнения заказа. Там проверки `to_have_value` и
`to_have_values`, имя загруженного файла через `evaluate`, переход по Tab
и скриншоты результата.

Скриншоты: `docs/screens/day3_order_form.png`, `docs/screens/day3_drag_drop.png`

### Auto-waiting

Шесть тестов на то, как Playwright ждёт элемент: клик по кнопке, которая
сначала выключена; проверка, что текст появился; кнопка под прозрачным слоем;
кнопка внутри `inert`; `force=True`; правила видимости.

Что выяснил:

- если элемент перекрыт, в ошибке будет `intercepts pointer events`;
- для `inert` — `element is inert`;
- элемент с `opacity: 0` считается видимым, а элемент нулевого размера — нет.

Мой вариант: замеряю время клика (ждёт примерно 0.8 секунды, пока кнопка
включится), ставлю `set_default_timeout(1500)` и проверяю текст ошибки
`Timeout 1500ms exceeded`.

## День 4, 14.11.2026

Двенадцать разделов подряд: API testing, Assertions, Authentication, Browsers,
Chrome extensions, Clock, Debugging Tests, Dialogs, Downloads, Emulation,
Evaluating JavaScript, Events.

Примеры в документации работают с сайтом задач на `localhost:3000`, которого
у меня нет. Поэтому я поднял свой маленький сервер `day4/api/server.py`: он
хранит задачи в памяти, отдаёт их как JSON и показывает простую страницу
со списком.

```
================== 69 passed, 1 warning in 26.31s ==================
```

### API testing

Взял пять примеров: создать баг-репорт, создать запрос на новую функцию,
проверить, что последняя задача первая в списке, проверить, что задача правда
лежит на сервере, и передать авторизацию из API в браузер.

Своё: вместо GitHub API использую свой сервер, потому что для GitHub нужен
токен. Адрес сервера приходит из фикстуры `api_server`, тесты пишут полный
адрес.

### Assertions

Пять примеров: проверка с повтором, галочка, состояния элемента, список,
значение поля.

Мой вариант:

1. `expect.soft` — если проверка упала, остальные всё равно выполнятся.
2. Своё сообщение об ошибке вторым аргументом `expect`, чтобы в логе было
   понятно, что именно сломалось.
3. Свой таймаут в одну секунду: когда ждать пять секунд незачем.
4. Проверки классов и атрибутов.

### Authentication

Пример: вход через форму (пароль `secret`) и повторный вход через сохранённое
состояние `storage_state`.

Мой вариант: страница профиля без куки отдаёт 401, неверный пароль не пускает,
а кука после входа профиль открывает. Так тест доказывает, что защита работает,
а не только что «зашёл».

### Browsers

Пример: три браузера (chromium, webkit, firefox) и запуск через канал `msedge`.
Все четыре варианта прошли.

Мой вариант: вывел версии браузеров и открыл расширение в постоянном контексте.

### Chrome extensions

Пример: браузер запускается с загруженным расширением, id берётся из service
worker, потом открывается всплывающее окно расширения и проверяется, что
content script вставил свой текст на страницу.

Скриншот окна расширения: `docs/screens/day4_extension_popup.png`

### Clock

Четыре примера: фиксированное время, таймеры, выход после пяти минут
бездействия, ручная прокрутка времени.

Мой вариант: скриншот часов с фиксированным временем, нажатие кнопки сбрасывает
таймер выхода, таймер продолжает идти и после паузы.

Скриншот часов: `docs/screens/day4_clock.png`

### Debugging Tests

Запустил тест с `$env:DEBUG="pw:api"` и сохранил вывод в `day4/debug_run.log` —
там видно каждый шаг Playwright: запуск браузера, переход, клик, закрытие.
Про `PWDEBUG=1` прочитал: открывается Inspector, но это отдельное окно, руками
я его не запускал.

### Dialogs

Пять примеров: alert, confirm, текст сообщения, prompt с вводом текста,
подтверждение при закрытии страницы.

Ошибка, которую встретил: если обработчик только читает сообщение и не отвечает
на диалог, клик висит до таймаута. Добавил `dialog.dismiss()` — сразу прошло.

Мой вариант: проверка типа и текста, одноразовый обработчик `page.once`,
диалог без обработчика (Playwright сам его закрывает).

### Downloads

Два примера: ожидание скачивания через `expect_download` и обработчик события
`download`.

Мой вариант: проверка содержимого скачанного файла и два скачивания подряд
в одном тесте.

### Emulation

Восемь примеров: iPhone 13, размер окна и плотность пикселей, язык и часовой
пояс, геолокация с разрешением, цветовая схема, свой user agent, выключенный
JavaScript, работа без сети.

Что выяснил: страница записывает значения один раз при загрузке. Поэтому после
смены размера окна, цветовой схемы или геолокации нужно `page.reload()`,
иначе видишь старые данные. Отдельно пришлось добавить `<meta name="viewport">`
в страницу — без него мобильный экран показывал 980 пикселей вместо 390.

Мой вариант: iPhone со своим user agent, выдача и отзыв разрешений,
принудительные цвета и уменьшенная анимация.

Скриншот страницы на iPhone: `docs/screens/day4_emulation.png`

### Evaluating JavaScript

Шесть примеров: получить адрес ссылки, передать аргумент, получить элемент
через `evaluate_handle`, два элемента, скрипт до загрузки страницы, вызов
Python-функции из JavaScript.

Ошибка: `evaluate_handle("#button1")` не работает, потому что это JavaScript,
а не селектор. Правильно — `"window.button1"`.

Мой вариант: асинхронная функция, изменение состояния страницы и скрипт
из файла.

### Events

Пять примеров: ждать нужный запрос, ждать новое окно, добавить и убрать
обработчик, поймать сообщение консоли, одноразовый обработчик.

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
- `day3/test_actions_example.py` — примеры действий из документации.
- `day3/test_actions_modified.py` — мой сценарий заполнения заказа.
- `day3/test_auto_waiting_example.py` — примеры ожиданий.
- `day3/test_auto_waiting_modified.py` — мои замеры времени и таймаутов.
- `day3/test_pytest_plugin.py` — примеры из Pytest Plugin Reference.
- `day3/conftest.py` — настройки размера окна и языка для тестов.
- `day3/library_script.py` — скрипты из раздела Library.
- `day3/fixtures` — html-страницы для действий и ожиданий.
- `day3/files` — файлы и папка для проверки загрузки.
- `day3/pytest_run.log`, `day3/cli_run.log`, `day3/library_run.log` — выводы запусков.
- `day3/codegen_help.log` — справка команды `playwright codegen`.
- `day4/test_api_example.py` — примеры из API testing.
- `day4/api/server.py` — мой маленький сервер для примеров API.
- `day4/test_assertions_example.py` / `test_assertions_modified.py` — проверки.
- `day4/test_auth_example.py` / `test_auth_modified.py` — авторизация.
- `day4/test_browsers_example.py` / `test_browsers_modified.py` — браузеры.
- `day4/test_chrome_extensions_example.py` — расширение Chrome.
- `day4/extension/my-extension` — файлы моего расширения.
- `day4/test_clock_example.py` / `test_clock_modified.py` — время.
- `day4/test_dialogs_example.py` / `test_dialogs_modified.py` — окна.
- `day4/test_downloads_example.py` / `test_downloads_modified.py` — скачивание.
- `day4/test_emulation_example.py` / `test_emulation_modified.py` — эмуляция.
- `day4/test_evaluating_example.py` / `test_evaluating_modified.py` — JavaScript.
- `day4/test_events_example.py` — события.
- `day4/fixtures` — html-страницы для этих разделов.
- `day4/pytest_run.log`, `day4/debug_run.log` — выводы запусков.
- `.github/workflows/playwright.yml` — запуск тестов на GitHub.
- `docs/screens` — скриншоты страниц и запусков.
