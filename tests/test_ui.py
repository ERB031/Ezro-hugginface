from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def playwright_context():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        yield context
        context.close()
        browser.close()


@pytest.fixture()
def page(playwright_context):
    page = playwright_context.new_page()
    yield page
    page.close()


def test_settings_page_inputs_are_editable(page):
    page.goto((ROOT / "settings.html").as_uri())
    name_input = page.locator("label:has-text('Full Name') + input")
    name_input.fill("Jamie Doe")
    assert name_input.input_value() == "Jamie Doe"


def test_tasks_page_add_task_button_opens_modal(page):
    page.goto((ROOT / "tasks.html").as_uri())
    page.get_by_role("button", name="Add Task").click()
    modal_class_list = page.eval_on_selector("#task-modal", "el => el.className")
    assert "hidden" not in modal_class_list.split()
