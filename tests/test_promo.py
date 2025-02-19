import logging.config
import time
import allure
from final.pages.account_page import AccountPage
from final.pages.cart_page import CartPage, CookieHandler
from final.pages.main_page import MainPage
from final.pages.order_page import OrderPage

logging.basicConfig(encoding="utf-8")


@allure.feature("Skillbox tests")
@allure.story("Promo assertion")
class TestPromo:

    @allure.title("Проверка корректной работы купона")
    def test_promo_code_correct(self, page):
        cart_page = CartPage(page)
        cookie_handler = CookieHandler(page)
        cookie_handler.add_item_cookies()
        cart_page.open_cart()
        cart_page.coupon_insert(coupon="GIVEMEHALYAVA")
        with allure.step("Проверка снижения итоговой стоимости на 10%"):
            assert (
                cart_page.total_price()
                == cart_page.pizza_price() - cart_page.pizza_price() / 10
            )

    @allure.title("Проверка некорректной работы купона")
    def test_promo_code_incorrect(self, page):
        cart_page = CartPage(page)
        cookie_handler = CookieHandler(page)
        cookie_handler.add_item_cookies()
        cart_page.open_cart()
        cart_page.coupon_insert(coupon="DC120")
        with allure.step("Проверка того, что цена не уменьшилась"):
            assert cart_page.total_price() == cart_page.pizza_price()

    @allure.title("Проверка некорректной работы купона в случае блокирования запроса")
    def test_apply_coupon_blocked(self, page):
        cart_page = CartPage(page)
        cookie_handler = CookieHandler(page)
        cookie_handler.add_item_cookies()
        page.route("**/?wc-ajax=apply_coupon", lambda route: route.abort())
        cart_page.open_cart()
        cart_page.coupon_insert(coupon="GIVEMEHALYAVA")
        with allure.step("Проверка, что промокод не применился и цена не изменилась"):
            assert cart_page.total_price() == cart_page.pizza_price()

    @allure.title("Проверка невозможности применить купон дважды на одном аккаунте")
    def test_one_coupon(self, page):
        account_page = AccountPage(page)
        cart_page = CartPage(page)
        cookie_handler = CookieHandler(page)
        order_page = OrderPage(page)
        card_main = MainPage(page)
        account_page.open()
        account_page.login()
        cookie_handler.add_item_cookies()
        cart_page.open_cart()
        cart_page.coupon_insert(coupon="GIVEMEHALYAVA")
        order_page.open()
        order_page.send_data()
        order_page.payment()
        order_page.submit()
        card_main.open()
        card_main.pizza_ham_card_button.click()
        time.sleep(1)
        cart_page.open_cart()
        cart_page.coupon_insert(coupon="GIVEMEHALYAVA")
        with allure.step("Проверка, что промокод не применился во второй раз"):
            assert cart_page.total_price() == cart_page.pizza_price()
