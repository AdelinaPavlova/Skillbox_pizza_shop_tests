import allure
import logging.config
from pages.account_page import AccountPage
from pages.cart_page import CartPage, CookieHandler
from pages.order_page import OrderPage

logging.basicConfig(encoding="utf-8")


@allure.feature("Skillbox tests")
@allure.story("Order assertion")
class TestOrder:

    @allure.title("Проверка перехода на страницу заполнения данных заказа")
    def test_order_page(self, page):
        account_page = AccountPage(page)
        cart_page = CartPage(page)
        cookie_handler = CookieHandler(page)
        order_page = OrderPage(page)
        account_page.open()
        account_page.login()
        cookie_handler.add_item_cookies()
        cart_page.open_cart()
        order_page.open()
        with allure.step("Проверка корректного перехода на страницу заполнения данных"):
            assert "ОФОРМЛЕНИЕ ЗАКАЗА" in order_page.title.inner_text()

    @allure.title("Проверка завершения заказа")
    def test_order_finish(self, page):
        account_page = AccountPage(page)
        cart_page = CartPage(page)
        cookie_handler = CookieHandler(page)
        order_page = OrderPage(page)
        account_page.open()
        account_page.login()
        cookie_handler.add_item_cookies()
        cart_page.open_cart()
        order_page.open()
        order_page.send_data()
        order_page.payment()
        order_page.submit()
        order_page.save_order()
        with allure.step("Проверка корректного перехода на страницу с деталями заказа"):
            assert (
                "http://pizzeria.skillbox.cc/checkout/order-received/"
                in order_page.get_full_url()
            )

    @allure.title("Проверка данных заказа")
    def test_order_detail(self, page):
        account_page = AccountPage(page)
        cart_page = CartPage(page)
        cookie_handler = CookieHandler(page)
        order_page = OrderPage(page)
        account_page.open()
        account_page.login()
        cookie_handler.add_item_cookies()
        cart_page.open_cart()
        total = cart_page.pizza_price()
        order_page.load_order()
        with allure.step("Проверка корректности стоимости заказа"):
            assert order_page.price() == total
        with allure.step("Проверка корректности мейла"):
            assert (
                order_page.DATA["mail"]
                == order_page.order_email.inner_text().split("\n")[1]
            )
