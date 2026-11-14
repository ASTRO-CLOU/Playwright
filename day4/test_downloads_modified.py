from pathlib import Path

from playwright.sync_api import Download, Page

FIXTURES = Path(__file__).parent / "fixtures"


def test_download_content_and_path(page: Page, base_url: str, tmp_path: Path):
    page.goto(f"{base_url}/static/download.html")

    with page.expect_download() as download_info:
        page.get_by_text("Download file").click()
    download = download_info.value

    saved = tmp_path / "copy.txt"
    download.save_as(saved)

    assert saved.read_text(encoding="utf-8").startswith("Отчёт за день 4")
    assert download.failure() is None


def test_two_downloads_in_one_test(page: Page, base_url: str, tmp_path: Path):
    page.goto(f"{base_url}/static/download.html")
    names: list[str] = []

    page.on("download", lambda download: names.append(download.suggested_filename))

    page.get_by_text("Download file").click()
    page.wait_for_timeout(300)
    page.get_by_text("Download file").click()
    page.wait_for_timeout(300)

    assert names == ["report.txt", "report.txt"]
