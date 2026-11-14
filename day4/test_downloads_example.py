from pathlib import Path

from playwright.sync_api import Download, Page, expect

FIXTURES = Path(__file__).parent / "fixtures"


def test_download_file(page: Page, base_url: str, tmp_path: Path):
    page.goto(f"{base_url}/static/download.html")

    with page.expect_download() as download_info:
        page.get_by_text("Download file").click()
    download = download_info.value

    target = tmp_path / download.suggested_filename
    download.save_as(target)

    expect(page.get_by_text("Download file")).to_be_visible()

    assert download.suggested_filename == "report.txt"
    assert "Отчёт за день 4" in target.read_text(encoding="utf-8")


def test_download_event_listener(page: Page, base_url: str):
    names: list[str] = []

    def handle_download(download: Download) -> None:
        names.append(download.suggested_filename)

    page.on("download", handle_download)
    page.goto(f"{base_url}/static/download.html")
    page.get_by_text("Download file").click()

    expect(page.get_by_text("Download file")).to_be_visible(timeout=5_000)
    page.wait_for_timeout(500)

    assert names == ["report.txt"]
    page.remove_listener("download", handle_download)
