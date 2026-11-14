import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

FIXTURES = Path(__file__).parent.parent / "fixtures"
CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".png": "image/png",
    ".txt": "text/plain; charset=utf-8",
}


class IssueStore:
    def __init__(self) -> None:
        self._issues: list[dict] = []
        self._lock = threading.Lock()

    def create(self, title: str, body: str) -> dict:
        with self._lock:
            issue = {"id": len(self._issues) + 1, "title": title, "body": body}
            self._issues.append(issue)
            return issue

    def all(self) -> list[dict]:
        with self._lock:
            return list(reversed(self._issues))

    def get(self, issue_id: int) -> dict | None:
        with self._lock:
            for issue in self._issues:
                if issue["id"] == issue_id:
                    return issue
            return None

    def delete(self, issue_id: int) -> bool:
        with self._lock:
            for index, issue in enumerate(self._issues):
                if issue["id"] == issue_id:
                    self._issues.pop(index)
                    return True
            return False


UI_PAGE = """<!DOCTYPE html>
<html lang="ru">
<head><meta charset="utf-8"><title>Issues</title></head>
<body>
  <h1>Issues</h1>
  <form method="post" action="/issues-ui">
    <label>Title <input name="title" required></label>
    <label>Body <input name="body"></label>
    <button type="submit">Add issue</button>
  </form>
  <ul id="issues">{items}</ul>
</body>
</html>
"""

LOGIN_PAGE = """<!DOCTYPE html>
<html lang="ru">
<head><meta charset="utf-8"><title>Sign in</title></head>
<body>
  <h1>Sign in</h1>
  <form method="post" action="/login">
    <label>Username <input name="username" required></label>
    <label>Password <input name="password" type="password" required></label>
    <button type="submit">Sign in</button>
  </form>
</body>
</html>
"""


def build_handler(store: IssueStore):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args) -> None:
            pass

        def _send(self, status: int, body: bytes, content_type: str, headers: dict | None = None) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            for name, value in (headers or {}).items():
                self.send_header(name, value)
            self.end_headers()
            self.wfile.write(body)

        def _json(self, status: int, payload) -> None:
            self._send(status, json.dumps(payload).encode("utf-8"), "application/json")

        def _redirect(self, location: str, headers: dict | None = None) -> None:
            self._send(302, b"", "text/html", {"Location": location, **(headers or {})})

        def _read_body(self) -> bytes:
            length = int(self.headers.get("Content-Length") or 0)
            return self.rfile.read(length)

        def do_GET(self) -> None:
            path = urlparse(self.path).path
            if path.startswith("/static/"):
                file_path = FIXTURES / path.rsplit("/", 1)[-1]
                if file_path.is_file():
                    content_type = CONTENT_TYPES.get(file_path.suffix, "application/octet-stream")
                    self._send(200, file_path.read_bytes(), content_type)
                else:
                    self._json(404, {"message": "Not found"})
                return
            if path in ("/", "/ui"):
                items = "".join(
                    f"<li data-testid='issue'>{issue['title']}: {issue['body']}</li>"
                    for issue in store.all()
                )
                self._send(200, UI_PAGE.format(items=items).encode("utf-8"), "text/html; charset=utf-8")
                return
            if path == "/login":
                self._send(200, LOGIN_PAGE.encode("utf-8"), "text/html; charset=utf-8")
                return
            if path == "/profile":
                cookie = self.headers.get("Cookie") or ""
                if "session=ok" in cookie:
                    self._send(200, b"<h1>Welcome, student</h1>", "text/html; charset=utf-8")
                else:
                    self._send(401, b"<h1>Please sign in</h1>", "text/html; charset=utf-8")
                return
            if path == "/issues":
                self._json(200, store.all())
                return
            if path.startswith("/issues/"):
                issue = store.get(int(path.rsplit("/", 1)[-1]))
                if issue is None:
                    self._json(404, {"message": "Not found"})
                else:
                    self._json(200, issue)
                return
            self._json(404, {"message": "Not found"})

        def do_POST(self) -> None:
            path = urlparse(self.path).path
            body = self._read_body()
            if path == "/issues":
                data = json.loads(body or b"{}")
                self._json(201, store.create(data.get("title", ""), data.get("body", "")))
                return
            if path == "/issues-ui":
                form = parse_qs(body.decode("utf-8"))
                store.create(form.get("title", [""])[0], form.get("body", [""])[0])
                self._redirect("/ui")
                return
            if path == "/login":
                form = parse_qs(body.decode("utf-8"))
                if form.get("password", [""])[0] == "secret":
                    self._redirect("/profile", {"Set-Cookie": "session=ok; Path=/"})
                else:
                    self._send(401, b"<h1>Wrong password</h1>", "text/html; charset=utf-8")
                return
            self._json(404, {"message": "Not found"})

        def do_DELETE(self) -> None:
            path = urlparse(self.path).path
            if path.startswith("/issues/"):
                if store.delete(int(path.rsplit("/", 1)[-1])):
                    self._json(204, {})
                else:
                    self._json(404, {"message": "Not found"})
                return
            self._json(404, {"message": "Not found"})

    return Handler


class ApiServer:
    def __init__(self) -> None:
        self.store = IssueStore()
        self._server = ThreadingHTTPServer(("127.0.0.1", 0), build_handler(self.store))
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    @property
    def base_url(self) -> str:
        host, port = self._server.server_address[:2]
        return f"http://{host}:{port}"

    def start(self) -> "ApiServer":
        self._thread.start()
        return self

    def stop(self) -> None:
        self._server.shutdown()
        self._server.server_close()
