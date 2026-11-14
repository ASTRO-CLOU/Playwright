from pathlib import Path

from playwright.sync_api import Page, expect

FIXTURES = Path(__file__).parent / "fixtures"


def test_evaluate_async_function(page: Page, base_url: str):
    page.goto(f"{base_url}/ui")

    status = page.evaluate(
        """async () => {
          const response = await fetch(location.href);
          return response.status;
        }"""
    )

    assert status == 200


def test_evaluate_sets_page_state(page: Page):
    page.goto((FIXTURES / "evaluate.html").as_uri())

    page.evaluate("""() => {
      document.querySelector('[data-testid="result"]').textContent = "changed by test";
    }""")

    expect(page.get_by_test_id("result")).to_have_text("changed by test")


def test_init_script_with_file(page: Page, tmp_path: Path):
    script = tmp_path / "preload.js"
    script.write_text("window.loadedBeforePage = true;", encoding="utf-8")

    page.add_init_script(path=str(script))
    page.goto((FIXTURES / "evaluate.html").as_uri())

    assert page.evaluate("() => window.loadedBeforePage") is True
