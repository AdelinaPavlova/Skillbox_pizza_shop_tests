import logging.config
from pages.main_page import MainPage
import allure
from pages.deserts_page import DesertsPage

logging.basicConfig(encoding="utf-8")


@allure.feature("Skillbox tests")
@allure.story("Pizza desert page assertion")
class TestDeserts:
    @allure.title("Проверка корректной работы фильтра по цене десерта")
    def test_desert_filter(self, page):
        desert_page = DesertsPage(page)
        desert_page.open()
        desert_page.move_slider(offset_x=-190, offset_y=0)
        desert_page.submit_button.click()
        with allure.step("Проверка корректного количества десертов на странице"):
            assert len(desert_page.deserts.all_inner_texts()) == 2
        with allure.step("Проверка отсутствия на странице десертов ценой свыше 135 р"):
            assert all(price <= 135 for price in desert_page.get_deserts_prices())

    @allure.title("Проверка добавления десерта в корзину")
    def test_desert_add(self, page):
        desert_page = DesertsPage(page)
        main_page = MainPage(page)
        desert_page.open()
        desert_page.add_desert()
        with allure.step("Проверка добавления десерта в корзину"):
            assert desert_page.get_price() == main_page.card_cost()
