import logging.config
import allure
from pages.account_page import AccountPage

logging.basicConfig(encoding="utf-8")


@allure.feature("Skillbox tests")
@allure.story("Account assertion")
class TestAccount:

    @allure.title("Проверка появления кнопки регистрации")
    def test_reg_button(self, page):
        account_page = AccountPage(page)
        account_page.open()
        with allure.step("Проверка появления кнопки"):
            assert account_page.registration_button.is_visible()

    @allure.title("Проверка регистрации/авторизации")
    def test_reg(self, page):
        account_page = AccountPage(page)
        account_page.open()
        username = account_page.login()
        with allure.step(
            "Проверка того, что имя в аккаунте совпадает с именем при авторизации/регистрации"
        ):
            assert f"Привет {username}" in account_page.account_content.inner_text()
