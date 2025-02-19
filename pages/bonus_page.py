import time
import allure
from playwright.sync_api import Page


class BonusPage:
    URL = "http://pizzeria.skillbox.cc/bonus/"

    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("//input[@name='username']")
        self.phone = page.locator("//input[@name='billing_phone']")
        self.submit_button = page.locator("//button[@name='bonus']")
        self.bonus_card = page.locator("//div[@id='bonus_main']//h3")
        self.validation_error = page.locator("//div[@id='bonus_content']")

    @allure.step("Получение url текущей страницы")
    def get_url(self):
        return self.page.url

    @allure.step("Открытие страницы {url}")
    def open(self, url: str = URL):
        if url is None:
            url = self.URL
        self.page.set_viewport_size({"width": 1920, "height": 1080})
        self.page.goto(url)
        return url

    @allure.step("Подстановка данных в формы")
    def send_data(self, username="user123", phone="+78889997654"):
        self.username.fill(username)
        self.phone.fill(phone)
        time.sleep(2)
        self.submit_button.click()

    @allure.step("Получение сообщения об ошибке валидации")
    def get_validation_error(self):
        return self.validation_error.inner_text()
