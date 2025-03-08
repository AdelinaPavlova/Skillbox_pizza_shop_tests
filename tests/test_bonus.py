import logging.config
import allure
from pages.bonus_page import BonusPage

logging.basicConfig(encoding="utf-8")


@allure.feature("Skillbox tests")
@allure.story("Bonus assertion")
class TestPromo:

    @allure.title("Проверка страницы бонусной системы")
    def test_bonus(self, page):
        bonus_page = BonusPage(page)
        bonus_page.open()
        bonus_page.send_data()
        with allure.step("Проверка успешного оформления карты"):
            assert "Ваша карта оформлена!" in bonus_page.bonus_card.inner_text()

    @allure.title("Проверка валидации имени пользователя")
    def test_bonus_validation_name(self, page):
        bonus_page = BonusPage(page)
        bonus_page.open()
        with allure.step("Проверка наличия ошибки имени пользователя"):
            bonus_page.send_data(username="user123.:Пщл)" * 20, phone="+78927754312")
            assert bonus_page.validation_error.is_visible()

    @allure.title("Проверка валидации номера телефона")
    def test_bonus_validation_phone(self, page):
        bonus_page = BonusPage(page)
        bonus_page.open()
        with allure.step("Проверка наличия ошибки некорректного номера телефона"):
            bonus_page.send_data(username="user123", phone="12345")
            assert (
                "Введен неверный формат телефона" in bonus_page.get_validation_error()
            )

    @allure.title("Проверка валидации пустых полей формы")
    def test_bonus_validation_empty(self, page):
        bonus_page = BonusPage(page)
        bonus_page.open()
        with allure.step("Проверка наличия ошибки пустых полей"):
            bonus_page.send_data(username="", phone="")
            assert (
                'Поле "Имя" обязательно для заполнения'
                in bonus_page.get_validation_error()
            )
            assert (
                'Поле "Телефон" обязательно для заполнения'
                in bonus_page.get_validation_error()
            )
