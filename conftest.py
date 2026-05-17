import pytest
import os
import logging
import logging.config
from datetime import datetime
from playwright.sync_api import sync_playwright
import webbrowser
import allure
from pytest_html import extras
from utils.config_reader import ConfigReader
import subprocess

# Define the main reports directory using environment variables or relative paths
reports_directory = os.getenv("REPORTS_DIRECTORY", os.path.join(os.getcwd(), "reports"))


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        action="store",
        default="https://netapp2--uat.sandbox.lightning.force.com/",
        help="Base URL for the application",
    )
    parser.addoption(
        "--browser_type",
        action="store",
        default="chromium",
        help="Browser to use for tests (chromium, firefox, webkit)",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode",
    )


@pytest.fixture(scope="session")
def browser(pytestconfig):
    browser_type = pytestconfig.getoption("browser_type")
    headless = pytestconfig.getoption("headless")
    with sync_playwright() as p:
        browser_args = {"headless": headless, "slow_mo": 200}
        if browser_type == "chromium":
            browser = p.chromium.launch(**browser_args)
        elif browser_type == "firefox":
            browser = p.firefox.launch(**browser_args)
        elif browser_type == "webkit":
            browser = p.webkit.launch(**browser_args)
        elif browser_type == "edge":
            browser_args["channel"] = "msedge"
            browser = p.chromium.launch(**browser_args)
        else:
            raise ValueError(f"Unsupported browser: {browser_type}")
        yield browser
        browser.close()


@pytest.fixture(scope="session")
def config():
    return ConfigReader()  # Initialize ConfigReader here


@pytest.fixture(scope="session")
def base_url(pytestconfig):
    return pytestconfig.getoption("url")


@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


# Ensure the logs directory exists using relative paths or environment variables
log_directory = os.getenv("LOG_DIRECTORY", os.path.join(os.getcwd(), "logs"))
if not os.path.exists(log_directory):
    os.makedirs(log_directory)


# Configure logging using logging.conf
def pytest_configure(config):
    logging.config.fileConfig(os.path.join(os.getcwd(), "logging.conf"))
    logging.getLogger().setLevel(logging.DEBUG)

    # Ensure the reports directory exists
    if not os.path.exists(reports_directory):
        os.makedirs(reports_directory)

    # Get the test script name
    if config.invocation_params.args and len(config.invocation_params.args) > 0:
        script_name = os.path.basename(config.invocation_params.args[0]).replace(
            ".py", ""
        )
    else:
        script_name = "default_report"  # Fallback name if no args provided

    # Generate a unique report name using the test script name and current date and time
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_name = f"{script_name}_{current_time}.html"
    report_path = os.path.join(reports_directory, report_name)

    # Add the HTML report option to pytest
    config.option.htmlpath = report_path

    # Ensure the extra field is available for attaching screenshots
    if not hasattr(config, "_html"):
        config._html = {"extra": []}


# Open the report in the default web browser after the test session ends
def pytest_sessionfinish(session, exitstatus):
    # Find the generated report file
    report_files = [f for f in os.listdir(reports_directory) if f.endswith(".html")]
    if report_files:
        latest_report = max(
            report_files,
            key=lambda f: os.path.getctime(os.path.join(reports_directory, f)),
        )
        report_path = os.path.abspath(os.path.join(reports_directory, latest_report))

        if os.path.exists(report_path):
            webbrowser.open(f"file://{report_path}")
        else:
            print("Report not found. Please check the path and try again.")
    else:
        print("No report files found in the reports directory.")


# Capture screenshots on test failure with date and time
def pytest_runtest_makereport(item, call):
    # Hook to add extra information to the report
    browser = item.funcargs.get("browser")  # Get the browser instance
    page = item.funcargs.get("page")  # Get the main page instance

    # Prepare screenshot directory using relative paths or environment variables
    screenshot_dir = os.getenv(
        "SCREENSHOT_DIRECTORY", os.path.join(os.getcwd(), "screenshots")
    )
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    # Generate screenshot filename
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    script_name = os.path.basename(item.nodeid).replace(".py", "").replace("::", "_")
    script_name = script_name.replace("[", "_").replace("]", "_")
    screenshot_filename = f"{script_name}_{current_time}.png"
    screenshot_path = os.path.join(screenshot_dir, screenshot_filename)

    # Capture screenshot from the active page
    if call.when == "call":
        try:
            # Check if the browser and its contexts are valid
            if browser and browser.contexts:
                active_context = browser.contexts[-1]  # Get the last browser context
                if active_context.pages:
                    active_page = active_context.pages[-1]  # Get the last opened page
                else:
                    active_page = page  # Fallback to the main page
            else:
                active_page = page  # Fallback to the main page

            # Capture screenshot
            active_page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")

            # Attach screenshot to the report
            if not hasattr(item, "extra"):
                item.extra = []
            item.extra.append(extras.image(screenshot_path))
            allure.attach.file(
                screenshot_path,
                name="screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception as e:
            print(f"Failed to capture screenshot: {e}")

    # Attach logs if the test failed
    if call.when == "call" and call.excinfo is not None:
        log_file = os.path.join(log_directory, "test_log.log")
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                log_content = f.read()
            if not hasattr(item, "extra"):
                item.extra = []
            item.extra.append(extras.text(log_content, "Test Log"))
            allure.attach(
                log_content,
                name="log",
                attachment_type=allure.attachment_type.TEXT,
            )

    # Ensure the extra field is linked to the request node so pytest-html can pick it up
    request = item.funcargs.get("request")
    if request:
        if not hasattr(request.node, "extra"):
            request.node.extra = []
        request.node.extra.extend(item.extra)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_protocol(item, nextitem):
    reruns = item.config.getoption("--reruns")
    item.add_marker(pytest.mark.flaky(reruns=reruns))
