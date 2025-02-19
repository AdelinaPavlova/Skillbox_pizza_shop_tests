import json
import allure
from playwright.sync_api import Page
import time


class CartPage:
    CART = "//a[@title='View your shopping cart']"
    CART_BUTTON = "//a[contains(@class, 'add_to_cart')]"
    URL = "http://pizzeria.skillbox.cc/"
    URL_CART = "http://pizzeria.skillbox.cc/cart/"
    BOARD_SELECTOR = "//select[@name='board_pack']"
    CART_ITEMS = "//tr[contains(@class, 'woocommerce-cart-form')]"
    MENU_BUTTON = "//li[contains(@class, 'has-children menu')]"
    DECERTS_SUB_MENU = (
        "//li[contains(@class, 'has-children menu')]//a[text()='Десерты']"
    )

    def __init__(self, page: Page):
        self.page = page
        self.cart_main = page.locator(self.CART)
        self.add_button = page.locator("//button[@name='add-to-cart']")
        self.pizzas_cost = page.locator("//td[@class='product-subtotal']")
        self.pizzas_cost_total = page.locator("//td[@data-title='Сумма']")
        self.cart_item = page.locator(self.CART_ITEMS)
        self.input_locator = page.locator("//input[@type='number']")
        self.update_cart = page.locator("//button[@name='update_cart']")
        self.remove_button = page.locator(
            "//dd//ancestor::tr//a[@aria-label='Remove this item']"
        )
        self.checkout_button = page.locator(
            "//a[@class='checkout-button button alt wc-forward']"
        )
        self.coupon_input = page.locator("//input[@name='coupon_code']")
        self.coupon_submit_button = page.locator("//button[@name='apply_coupon']")

    @allure.step("Переход к десертам")
    def go_to_deserts(self):
        self.page.locator(self.MENU_BUTTON).click()
        self.page.locator(self.DECERTS_SUB_MENU).click()

    @allure.step("Получение url текущей страницы")
    def get_url(self):
        return self.page.url

    @allure.step("Добавление купона")
    def coupon_insert(self, coupon):
        with allure.step(f"Добавление в строку текста {coupon}"):
            self.coupon_input.fill(coupon)
        with allure.step("Нажатие кнопки добавление купона"):
            self.coupon_submit_button.click()
        time.sleep(1)

    @allure.step("Получение стоимости корзины")
    def cart_cost(self):
        return int(
            "".join(i for i in self.cart_main.inner_text().split(",")[0] if i.isdigit())
        )

    @allure.step("Открытие страницы продукта {pizza}")
    def open(self, pizza: str = "пицца-ветчина-и-грибы", url: str = None):
        if url is None:
            url = f"{self.URL}{pizza}/"
        self.page.goto(url)

    @allure.step("Открытие страницы корзины {url}")
    def open_cart(self, url: str = URL_CART):
        if url is None:
            url = self.URL
        self.page.goto(url)
        return url

    @allure.step("Выбор сырного или колбасного борта {b_type}")
    def choice(self, b_type: str = "Сырный - 55.00 р."):
        self.page.select_option(self.BOARD_SELECTOR, label=b_type)

    @allure.step("Получение стоимости пиццы в корзине")
    def pizza_price(self):
        return int(
            "".join(
                i for i in self.pizzas_cost.inner_text().split(",")[0] if i.isdigit()
            )
        )
        time.sleep(1)

    @allure.step("Получение итоговой стоимости корзины")
    def total_price(self):
        return int(
            "".join(
                i
                for i in self.pizzas_cost_total.inner_text().split(",")[0]
                if i.isdigit()
            )
        )

    @allure.step("Добавление в корзину")
    def add_to_cart(self):
        self.add_button.click()


class CookieHandler:
    def __init__(self, page: Page):
        self.page = page
        self.current_cookies = None
        self.load_cookies()

    def cart_is_empty(self):
        cart_page = CartPage(self.page)
        cart_page.open_cart()
        cart_items = cart_page.cart_item.count()
        return cart_items == 0

    @allure.step("Генерация новых cookies")
    def generate_cookies(self):
        cart_page = CartPage(self.page)
        cart_page.open()
        cart_page.add_to_cart()
        cookies = self.page.context.cookies()
        new_cookie = {
            "name": cookies[1]["name"],
            "value": cookies[1]["value"],
            "domain": cookies[1]["domain"],
            "path": cookies[1]["path"],
            "expires": cookies[1]["expires"],
            "httpOnly": cookies[1]["httpOnly"],
            "secure": cookies[1]["secure"],
            "sameSite": cookies[1]["sameSite"],
        }
        self.current_cookies = new_cookie
        self.save_cookies()
        print(f"Сгенерированы новые куки: {new_cookie}")
        return new_cookie

    @allure.step("Сохранение cookies")
    def save_cookies(self):
        with open("cookies.json", "w") as f:
            json.dump(self.current_cookies, f)

    @allure.step("Загрузка cookies из файла")
    def load_cookies(self):
        try:
            with open("cookies.json", "r") as f:
                self.current_cookies = json.load(f)
                print(f"Загружены куки: {self.current_cookies}")
        except FileNotFoundError:
            print("Файл с куками не найден. Требуется сгенерировать новый")

    @allure.step("Добавление cookies")
    def are_cookies_valid(self):
        if not self.current_cookies:
            return False
        expires = self.current_cookies.get("expires", -1)
        if expires == -1:
            return True
        current_time = time.time()
        if expires < current_time:
            return False
        return True

    @allure.step("Добавление cookies")
    def add_item_cookies(self):
        if self.cart_is_empty():
            print("Корзина пуста, генерируем новые cookies...")
            self.generate_cookies()

        if not self.are_cookies_valid():
            print("Текущие куки недействительны. Генерируем новые...")
            self.generate_cookies()

        self.page.context.add_cookies([self.current_cookies])
        self.page.reload()
        print("Cookies добавлены и страница обновлена.")
