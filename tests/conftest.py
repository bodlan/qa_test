import pytest
from playwright.sync_api import Browser
from libraries.demoblaze.demoblaze import DemoBlaze
from libraries import CONFIG, Report, ReportItem


@pytest.fixture()
def demoblaze(browser: Browser):
    return DemoBlaze(
        browser,
        username=CONFIG.DemoBlaze.Username,
        password=CONFIG.DemoBlaze.Password,
    )


@pytest.fixture(scope="session")
def report(request):
    report_obj = Report()
    # Store the Report object in the config object
    request.config.report_object = report_obj
    return report_obj


@pytest.fixture()
def report_item():
    return ReportItem()


def pytest_sessionfinish(session, exitstatus):
    # Access the Report object from the config object
    report_object = session.config.report_object

    report_object.generate_xlsx(CONFIG.REPORT_FILE)
