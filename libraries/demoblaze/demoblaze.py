import os
import re
import time
import random
import string
from datetime import datetime
from typing import Tuple

from playwright.sync_api import Browser, expect, Locator
from libraries import CONFIG, logger


class DemoBlaze:
    HOME_URL = "https://www.demoblaze.com/index.html"

    def __init__(self, browser: Browser, username: str, password: str) -> None:
        self.browser = browser
        self._context = self.browser.new_context()
        self._page = self._context.new_page()
        self._username: str = username
        self._password: str = password
        self.dialog_message: str = ""

    def to_home_page(self) -> None:
        self._page.goto(self.HOME_URL)

    def handle_dialog(self, dialog) -> None:
        self.dialog_message = dialog.message
        dialog.accept()

    def modal_input(self, register: bool) -> Tuple[Locator, Locator, Locator]:
        if register:
            nav_signup_button = self._page.locator("#signin2")
        else:
            nav_signup_button = self._page.locator("#login2")
        nav_signup_button.click()
        if register:
            modal_div = self._page.locator("#signInModal")
            username_field = modal_div.locator("#sign-username")
            password_field = modal_div.locator("#sign-password")
            submit_button = modal_div.get_by_role("button", name="Sign up")
            cancel_button = modal_div.get_by_role("button", name="Close").get_by_text("Close")
        else:
            modal_div = self._page.locator("#logInModal")
            username_field = modal_div.locator("#loginusername")
            password_field = modal_div.locator("#loginpassword")
            submit_button = modal_div.get_by_role("button", name="Log in")
            cancel_button = modal_div.get_by_role("button", name="Close").get_by_text("Close")

        username_field.fill(self._username)
        expect(username_field).to_have_value(self._username)

        password_field.fill(self._password)
        expect(password_field).to_have_value(self._password)

        return username_field, submit_button, cancel_button

    def register(self) -> None:
        username_field, submit_button, cancel_button = self.modal_input(register=True)

        # alert handle
        self._page.once("dialog", self.handle_dialog)

        submit_button.click()

        if self.dialog_message == "This user already exist.":
            if not CONFIG.DEV:
                now = datetime.now().strftime("%d%m%Y%H%M%S")
                self._username += now
                # Setting new username for later use
                CONFIG.DemoBlaze.Username = self._username
                username_field.fill(self._username)
                submit_button.click()
                logger.info(
                    f"Successfully created account with username: " f"{self._username} and password {self._password}"
                )
            else:
                cancel_button.click()
                logger.info("Skipping register process")
        else:
            logger.info(
                f"Successfully created account with username: " f"{self._username} and password {self._password}"
            )
        self.dialog_message = ""

    def login(self) -> None:
        username_field, submit_button, cancel_button = self.modal_input(register=False)
        submit_button.click()
        welcome_user = self._page.locator("#nameofuser")
        # Assert 'Welcome <username>'
        expect(welcome_user).to_have_text(re.compile(r"Welcome .*"))
        logger.info("Successfully logged in")
        for i in range(5):
            logger.info(f"Attempting to get cookies...{i + 1}")
            if not CONFIG.DemoBlaze.Cookies:
                CONFIG.DemoBlaze.Cookies = self._context.cookies()
                time.sleep(1)
            else:
                break
        logger.debug(f"Collected cookies: {CONFIG.DemoBlaze.Cookies}")

    @staticmethod
    def log_and_raise_exc(message):
        logger.exception(message)
        raise Exception(message)

    @staticmethod
    def get_random_text():
        letters = string.ascii_letters
        random_text = "".join(random.choice(letters) for _ in range(random.randint(6, 10)))
        return random_text

    def add_cookies(self) -> None:
        self._context.add_cookies(CONFIG.DemoBlaze.Cookies)

    def handle_order_modal(self) -> None:
        expect(self._page.locator("#orderModal")).to_be_visible()
        order_modal = self._page.locator("#orderModal")

        order_modal.locator("#name").fill(self.get_random_text())
        order_modal.locator("#country").fill(self.get_random_text())
        order_modal.locator("#city").fill(self.get_random_text())
        order_modal.locator("#card").fill(self.get_random_text())
        order_modal.locator("#month").fill(self.get_random_text())
        order_modal.locator("#year").fill(self.get_random_text())

        order_modal.get_by_role("button", name="Purchase").click()

        expect(self._page.get_by_text("Thank you for your purchase!")).to_be_visible()

    def select_product_and_purchase(self, item, category, price) -> str:
        self._page.locator("#itemc").get_by_text(category).click()
        item_table = self._page.locator("#tbodyid")
        try:
            item_block = item_table.locator(".card-title").get_by_text(item)
            item_block.click()
        except Exception as ex:
            logger.exception(f"Exception trying to find item: {ex}")
        self._page.once("dialog", self.handle_dialog)
        self._page.get_by_text("Add to cart").click()
        if self.dialog_message == "Product added.":
            logger.info("Product added to cart")
        else:
            error_message = f"Dialog message differs should be 'Product added' got {self.dialog_message}"
            self.log_and_raise_exc(error_message)
        self._page.locator("#cartur").click()

        cart_table = self._page.locator("table")

        head_table = cart_table.locator("thead")
        head_titles = head_table.locator("th").all_inner_texts()
        logger.info(f"All inner texts: {head_titles}")
        title_index = head_titles.index("Title")
        price_index = head_titles.index("Price")
        body_table = cart_table.locator("#tbodyid")

        table_items = body_table.locator("tr")
        expect(table_items).to_have_count(1)
        # it can be done inside for loop,
        # but for this test decided just to pick the item instead
        first_row = table_items.nth(0)

        expect(first_row.locator("td").nth(title_index)).to_have_text(item)
        expect(first_row.locator("td").nth(price_index)).to_have_text(price)

        self._page.get_by_role("button", name="Place Order").click()
        self.handle_order_modal()

        order = self._page.locator('//p[@class="lead text-muted "]').inner_text()
        match = re.search(r"Id: (\d+)", order)
        if match:
            order_id = match.group(1)
            logger.info(f"Order id: {order_id}")
            self._page.screenshot(path=os.path.join(CONFIG.WORK_DIR, "result.png"))
            return order_id
        else:
            error_message = "Order id not found!"
            self.log_and_raise_exc(error_message)
