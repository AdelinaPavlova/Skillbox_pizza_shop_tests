import allure
import logging.config
from pages.product_page import ProductPage

logging.basicConfig(encoding="utf-8")


@allure.feature("Skillbox tests")
@allure.story("Pizza product page assertion")
class TestBoardProduct:
    @allure.title("Проверка корректного увеличения стоимости пиццы на цену борта")
    def test_pizza_board_cost(self, page):
        board_product = ProductPage(page)
        board_product.open()
        previous_price = board_product.pizza_price()
        board_product.choice()
        board_cost = board_product.pizza_price() - previous_price
        board_product.add_to_card()
        with allure.step("Проверка увеличения стоимости пиццы на стоимость борта"):
            assert board_cost == 55 or board_cost == 65

    @allure.title("Проверка корректного добавления в корзину пиццы с бортом")
    def test_pizza_board_add_cart(self, page):
        board_product = ProductPage(page)
        board_product.open()
        board_product.choice()
        pizza_with_board_price = board_product.pizza_price()
        board_product.add_to_card()
        with allure.step(
            "Проверка увеличения стоимости корзины на стоимость пиццы с бортом"
        ):
            assert board_product.card_cost() == pizza_with_board_price
