import time
import allure
from playwright.sync_api import Page


class AccountPage:
    URL = "http://pizzeria.skillbox.cc/my-account/"
    FIELDS = "//input[@id="

    def __init__(self, page: Page):
        self.page = page
        self.registration_button = page.locator("//button[text()='Зарегистрироваться']")
        self.username = page.locator(f"{self.FIELDS}'reg_username']")
        self.email = page.locator(f"{self.FIELDS}'reg_email']")
        self.password = page.locator(f"{self.FIELDS}'reg_password']")
        self.submit_button = page.locator("//button[text()='Зарегистрироваться']")
        self.info = page.locator("//div[@class='content-page']")
        self.login_button = page.locator("//button[@name='login']")
        self.remember_user = page.locator("//input[@value='forever']")
        self.error = page.locator("//ul[@class='woocommerce-error']")
        self.login_username = page.locator("//input[@name='username']")
        self.login_password = page.locator("//input[@name='password']")
        self.account_content = page.locator(
            "//div[@class='woocommerce-MyAccount-content']"
        )

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

    @allure.step("Нажатие кнопки 'Зарегистрироваться'")
    def submit(self):
        self.submit_button.click()
        time.sleep(1)

    @allure.step("Подстановка данных в формы")
    def send_data(
        self, username="user_24_name", email="email24@mail.ru", password="password"
    ):
        self.username.fill(username)
        self.email.fill(email)
        self.password.fill(password)

    def is_error(self):
        if self.error.is_visible():
            return True
        return False

    @allure.step("Вход в аккаунт...")
    def login(self, username="user_24_name", password="password"):
        self.login_username.fill(username)
        self.login_password.fill(password)
        self.remember_user.click()
        self.login_button.click()
        if self.is_error():
            time.sleep(1)
            self.registration_button.click()
            self.send_data()
            self.submit()
            self.open()
        time.sleep(2)
        return username
