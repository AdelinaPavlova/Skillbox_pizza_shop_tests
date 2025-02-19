import time
import allure
import logging.config
from final.pages.main_page import MainPage

logging.basicConfig(encoding="utf-8")


@allure.feature("Skillbox tests")
@allure.story("Main page card insert assertion")
class TestCardMain:

    @allure.title('Проверка видимости кнопки "в корзину" при наведении на пиццу')
    def test_cart_button(self, page):
        card_main = MainPage(page)
        card_main.open()
        card_main.pizza_hover("ham")
        with allure.step(
            'Проверка видимости кнопки "в корзину" при наведении на пиццу'
        ):
            assert card_main.card_button_status("ham").is_visible()

    @allure.title("Проверка добавления пиццы в корзину")
    def test_add_to_cart_main(self, page):
        card_main = MainPage(page)
        card_main.open()
        card_main.pizza_ham_card_button.click()
        time.sleep(1)
        with allure.step("Проверка добавления пиццы в корзину"):
            assert card_main.pizza_price("ham") == card_main.card_cost()

    @allure.title("Проверка добавления второй пиццы в корзину после прокрутки слайдера")
    def test_add_to_cart_after_slider(self, page):
        card_main = MainPage(page)
        card_main.open()
        card_main.pizza_ham_card_button.click()
        previous_cost = card_main.card_cost()
        card_main.hover_over_slider()
        card_main.click_slider(direction="right")
        card_main.pizza_peperoni_card_button.click()
        card_main.check_change_card_cost(previous_cost)
        with allure.step(
            "Проверка добавления второй пиццы в корзину после прокрутки слайдера"
        ):
            assert (
                card_main.pizza_price("ham") + card_main.pizza_price("peperoni")
            ) == card_main.card_cost()
