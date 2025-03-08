import allure
import logging.config
from pages.cart_page import CartPage, CookieHandler
from pages.main_page import MainPage

logging.basicConfig(encoding="utf-8")


@allure.feature("Skillbox tests")
@allure.story("Go to product page assertion")
class TestTransferMain:
    @allure.title("Проверка перехода на страницу описания пиццы")
    def test_go_to_product_page(self, page):
        transfer_main = MainPage(page)
        transfer_main.open()
        transfer_main.pizza_ham.click()
        with allure.step("Проверка корректного перехода на страницу описания пиццы"):
            assert "http://pizzeria.skillbox.cc/product/" in transfer_main.get_url()

    @allure.title("Проверка перехода на страницу корзины")
    def test_go_to_cart_page(self, page):
        transfer_main = MainPage(page)
        transfer_main.open()
        transfer_main.card_main.click()
        with allure.step("Проверка корректного перехода на страницу корзины"):
            assert "http://pizzeria.skillbox.cc/cart/" in transfer_main.get_url()

    @allure.title("Проверка перехода на страницу авторизации")
    def test_go_to_login_page(self, page):
        transfer_main = CartPage(page)
        cookie_handler = CookieHandler(page)
        cookie_handler.add_item_cookies()
        transfer_main.open_cart()
        transfer_main.checkout_button.click()
        with allure.step(
            "Проверка корректного перехода на страницу авторизации из корзины"
        ):
            assert "http://pizzeria.skillbox.cc/checkout/" in transfer_main.get_url()

    @allure.title("Проверка перехода на страницу c десертами из выпадающего меню")
    def test_go_to_desert_page(self, page):
        transfer_main = CartPage(page)
        transfer_main.open_cart()
        transfer_main.go_to_deserts()
        with allure.step("Проверка корректного перехода на страницу десертов"):
            assert (
                "http://pizzeria.skillbox.cc/product-category/menu/deserts/"
                in transfer_main.get_url()
            )
