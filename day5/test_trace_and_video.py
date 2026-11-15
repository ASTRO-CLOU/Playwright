from pathlib import Path

from playwright.sync_api import Browser, expect

ARTIFACTS = Path(__file__).parent / "artifacts"


def test_record_trace(browser: Browser, fixture_url: str):
    ARTIFACTS.mkdir(exist_ok=True)
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()
    page.goto(f"{fixture_url}/aria.html")
    expect(page.get_by_role("heading", level=1)).to_be_visible()

    trace_path = ARTIFACTS / "trace.zip"
    context.tracing.stop(path=str(trace_path))
    context.close()

    assert trace_path.stat().st_size > 0


def test_record_video(browser: Browser, fixture_url: str):
    ARTIFACTS.mkdir(exist_ok=True)
    context = browser.new_context(
        record_video_dir=str(ARTIFACTS / "raw"),
        record_video_size={"width": 640, "height": 480},
    )

    page = context.new_page()
    page.goto(f"{fixture_url}/aria.html")
    expect(page.get_by_role("heading", level=1)).to_be_visible()

    video_path = page.video.path()
    context.close()

    saved_path = ARTIFACTS / "day5_video.webm"
    saved_path.write_bytes(Path(video_path).read_bytes())

    assert saved_path.stat().st_size > 0
