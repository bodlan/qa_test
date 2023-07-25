import os
from datetime import datetime


class CONFIG:
    DEV = False
    WORK_DIR = os.path.join(os.getcwd(), "work_dir")
    if not os.path.exists(WORK_DIR):
        os.mkdir(WORK_DIR)
    log_filename = datetime.now().strftime("%d-%m-%Y") + ".log"
    LOG_FILE = os.path.join(WORK_DIR, log_filename)
    report_filename = "Report" + datetime.now().strftime("%d-%m-%Y %H%M%S") + ".xlsx"
    REPORT_FILE = os.path.join(WORK_DIR, report_filename)

    class DemoBlaze:
        # If using ENV variables
        Username = os.environ.get("DEMOBLAZEUSERNAME")
        Password = os.environ.get("DEMOBLAZEPASSWORD")
        # If no ENV variables found
        if not Username:
            Username = "BodlanTest"
        if not Password:
            Password = "Testpassword123"
        Cookies = []
