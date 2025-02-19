import logging.config
import time
import allure
from final.pages.cart_page import CartPage

logging.basicConfig(encoding="utf-8")


@allure.feature("Skillbox tests")
@allure.story("Cart page assertion")
class TestBoardProduct:
    @allure.title("Проверка добавления в корзину пиццы с доп.бортом и без")
    def test_adding_cart(self, page):
        cart_page = CartPage(page)
        cart_page.open()
        cart_page.choice()
        cart_page.add_to_cart()
        cart_page.add_to_cart()
        cart_page.open_cart()
        cart_items_text = cart_page.cart_item.all_inner_texts()
        with allure.step("Проверка корректного количества товаров в корзине"):
            assert len(cart_items_text) == 2
        with allure.step("Проверка наличия пиццы с бортом в корзине"):
            assert any("Сырный борт" in text for text in cart_items_text)

    @allure.title("Проверка добавления в корзину дополнительной дублирующей пиццы")
    def test_duplicate_pizza(self, page):
        cart_page = CartPage(page)
        cart_page.open()
        cart_page.add_to_cart()
        cart_page.open_cart()
        price = cart_page.pizza_price()
        cart_page.input_locator.fill("2")
        cart_page.update_cart.click()
        time.sleep(1)
        with allure.step(
            "Проверка увеличения цены пиццы в 2 раза при добавлении дублирующей пиццы"
        ):
            assert price * 2 == cart_page.pizza_price()

    @allure.title("Проверка удаления пиццы с бортом")
    def test_delete_pizza(self, page):
        cart_page = CartPage(page)
        cart_page.open()
        cart_page.choice()
        cart_page.add_to_cart()
        cart_page.add_to_cart()
        cart_page.open_cart()
        cart_page.remove_button.click()
        time.sleep(1)
        cart_items_text = cart_page.cart_item.all_inner_texts()
        with allure.step("Проверка корректного удаления"):
            assert len(cart_items_text) == 1
        with allure.step("Проверка отсутствия пиццы с бортом в корзине"):
            assert not any("Сырный борт" in text for text in cart_items_text)
