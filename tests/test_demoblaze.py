from libraries import logger, DemoBlaze, ReportItem, Report, CONFIG


def test_register(demoblaze: DemoBlaze, report: Report, report_item: ReportItem) -> None:
    report_item.test_name = "Register"
    logger.info("Registering to website...")
    try:
        demoblaze.to_home_page()
        demoblaze.register()
        report_item.status = "Success"
        report_item.comments = f"Username= {CONFIG.DemoBlaze.Username}, password= {CONFIG.DemoBlaze.Password}"
    except Exception as ex:
        logger.info(f"Exception while processing test_register {ex}")
        report_item.comments = str(ex)
        report_item.status = "Failed"
    report.add_row(report_item)


def test_login(demoblaze: DemoBlaze, report: Report, report_item: ReportItem) -> None:
    report_item.test_name = "Login"
    logger.info("Logging in...")
    logger.debug(f"Username: {demoblaze._username}")
    try:
        demoblaze.to_home_page()
        demoblaze.login()
        report_item.status = "Success"
    except Exception as ex:
        logger.info(f"Exception while processing test_login {ex}")
        report_item.comments = str(ex)
        report_item.status = "Failed"
    report.add_row(report_item)


def test_item_buy(demoblaze: DemoBlaze, report: Report, report_item: ReportItem) -> None:
    item = "MacBook Pro"
    category = "Laptops"
    price = "1100"
    logger.info(f"Buying item {item} in category {category} with price {price}")
    report_item.test_name = "Item buy"
    try:
        demoblaze.add_cookies()
        demoblaze.to_home_page()
        order_id = demoblaze.select_product_and_purchase(item, category, price)
        report_item.status = "Success"
        report_item.comments = f"Id: {order_id}"
    except Exception as ex:
        logger.info(f"Exception while processing test_item_buy {ex}")
        report_item.comments = str(ex)
        report_item.status = "Failed"
    report.add_row(report_item)
