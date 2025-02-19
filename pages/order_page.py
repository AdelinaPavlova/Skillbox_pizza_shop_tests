import time
from datetime import datetime, timedelta
import allure
from playwright.sync_api import Page


class OrderPage:
    DATA = {
        "name": "username",
        "surname": "user_surname",
        "address": "my_address",
        "city": "moscow",
        "region": "msk_city",
        "index": "101000",
        "phone": "+78889992332",
        "mail": "mail_12@gmail.com",
    }

    URL = "http://pizzeria.skillbox.cc/checkout/"
    FIELDS = "//input[@id='"

    def __init__(self, page: Page):
        self.page = page
        self.current_address = None
        self.title = page.locator("//h2[@class='post-title']")
        self.name = page.locator(f"{self.FIELDS}billing_first_name']")
        self.surname = page.locator(f"{self.FIELDS}billing_last_name']")
        self.address = page.locator(f"{self.FIELDS}billing_address_1']")
        self.city = page.locator(f"{self.FIELDS}billing_city']")
        self.region = page.locator(f"{self.FIELDS}billing_state']")
        self.index = page.locator(f"{self.FIELDS}billing_postcode']")
        self.phone = page.locator(f"{self.FIELDS}billing_phone']")
        self.mail = page.locator(f"{self.FIELDS}billing_email']")
        self.date = page.locator("//input[@name='order_date']")
        self.pay_method = page.locator("//input[@id='payment_method_cod']")
        self.submit_button = page.locator("//button[@id='place_order']")
        self.terms = page.locator("//input[@type='checkbox']")
        self.order_price = page.locator(
            "//li//span[@class='woocommerce-Price-amount amount']"
        )
        self.order_email = page.locator(
            "//li[@class='woocommerce-order-overview__email email']"
        )

    @allure.step("Получение текущего url")
    def get_full_url(self):
        return self.page.evaluate("() => window.location.href")

    @allure.step("Запись в файл адреса с деталями заказа")
    def save_order(self):
        order_url = self.get_full_url()
        with open("order.txt", "w") as f:
            f.write(order_url)

    @allure.step("Считывание url заказа")
    def load_order(self):
        try:
            with open("order.txt", "r") as f:
                self.current_address = f.read()
                print(f"Адрес страницы заказа: {self.current_address}")
                self.page.goto(self.current_address)
                time.sleep(2)
        except FileNotFoundError:
            print("Ошибка")

    @allure.step("Открытие страницы {url}")
    def open(self, url: str = URL):
        if url is None:
            url = self.URL
        self.page.set_viewport_size({"width": 1920, "height": 1080})
        self.page.goto(url)
        time.sleep(1)
        return url

    @allure.step("Получение стоимости пиццы из деталей заказа")
    def price(self):
        return int(
            "".join(
                i for i in self.order_price.inner_text().split(",")[0] if i.isdigit()
            )
        )

    @allure.step("Подстановка данных в формы")
    def send_data(self, data=None):
        if data is None:
            data = self.DATA
        self.name.fill(data["name"])
        self.surname.fill(data["surname"])
        self.address.fill(data["address"])
        self.city.fill(data["city"])
        self.region.fill(data["region"])
        self.index.fill(data["index"])
        self.phone.fill(data["phone"])
        self.mail.fill(data["mail"])
        self.date.click()
        tomorrow = datetime.now() + timedelta(days=1)
        time.sleep(3)
        formatted_date = tomorrow.strftime("%d.%m.%Y")
        self.date.type(formatted_date)

    @allure.step("Выбор оплаты при получении")
    def payment(self):
        self.pay_method.click()

    @allure.step("Подтверждение данных")
    def submit(self):
        self.terms.click()
        self.submit_button.click()
        time.sleep(2)
