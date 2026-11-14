from typing import Generator

import pytest
from playwright.sync_api import APIRequestContext, Browser, Page, Playwright, expect


@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright, api_server
) -> Generator[APIRequestContext, None, None]:
    headers = {
        "Accept": "application/json",
    }
    request_context = playwright.request.new_context(
        base_url=api_server.base_url, extra_http_headers=headers
    )
    yield request_context
    request_context.dispose()


def test_should_create_bug_report(api_request_context: APIRequestContext) -> None:
    data = {
        "title": "[Bug] report 1",
        "body": "Bug description",
    }
    new_issue = api_request_context.post("/issues", data=data)
    assert new_issue.ok

    issues = api_request_context.get("/issues")
    assert issues.ok
    issues_response = issues.json()
    issue = list(filter(lambda issue: issue["title"] == "[Bug] report 1", issues_response))[0]
    assert issue
    assert issue["body"] == "Bug description"


def test_should_create_feature_request(api_request_context: APIRequestContext) -> None:
    data = {
        "title": "[Feature] request 1",
        "body": "Feature description",
    }
    new_issue = api_request_context.post("/issues", data=data)
    assert new_issue.ok

    issues = api_request_context.get("/issues")
    assert issues.ok
    issues_response = issues.json()
    issue = list(
        filter(lambda issue: issue["title"] == "[Feature] request 1", issues_response)
    )[0]
    assert issue
    assert issue["body"] == "Feature description"


def test_last_created_issue_should_be_first_in_the_list(
    api_request_context: APIRequestContext, page: Page, base_url: str
) -> None:
    def create_issue(title: str) -> None:
        data = {
            "title": title,
            "body": "Feature description",
        }
        new_issue = api_request_context.post("/issues", data=data)
        assert new_issue.ok

    create_issue("[Feature] request 1")
    create_issue("[Feature] request 2")
    page.goto(f"{base_url}/ui")
    first_issue = page.locator("#issues li").first
    expect(first_issue).to_have_text("[Feature] request 2: Feature description")


def test_last_created_issue_should_be_on_the_server(
    api_request_context: APIRequestContext, page: Page, base_url: str
) -> None:
    page.goto(f"{base_url}/ui")
    page.get_by_label("Title").fill("Bug report 1")
    page.get_by_label("Body").fill("Bug description")
    page.get_by_role("button", name="Add issue").click()

    new_issue = api_request_context.get("/issues")
    assert new_issue.ok
    titles = [issue["title"] for issue in new_issue.json()]
    assert "Bug report 1" in titles


def test_reuse_authentication_state(
    api_request_context: APIRequestContext, browser: Browser, base_url: str
) -> None:
    login = api_request_context.post(
        "/login", form={"username": "student", "password": "secret"}
    )
    assert login.ok
    state = api_request_context.storage_state()

    context = browser.new_context(storage_state=state)
    page = context.new_page()
    page.goto(f"{base_url}/profile")
    expect(page.get_by_role("heading")).to_have_text("Welcome, student")
    context.close()
