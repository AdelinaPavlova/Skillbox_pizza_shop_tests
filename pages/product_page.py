import allure
from playwright.sync_api import Page


class ProductPage:
    CARD = "//a[@title='View your shopping cart']"
    CARD_BUTTON = "//a[contains(@class, 'add_to_cart')]"
    URL = "http://pizzeria.skillbox.cc/product/"
    BOARD_SELECTOR = "//select[@name='board_pack']"

    def __init__(self, page: Page):
        self.page = page
        self.card_main = page.locator(self.CARD)
        self.add_button = page.locator("//button[@name='add-to-cart']")
        self.pizza_cost = page.locator("//p[@class='price']//bdi")

    @allure.step("Получение стоимости корзины")
    def card_cost(self):
        return int(
            "".join(i for i in self.card_main.inner_text().split(",")[0] if i.isdigit())
        )

    @allure.step("Открытие страницы продукта {pizza}")
    def open(self, pizza: str = "пицца-ветчина-и-грибы", url: str = None):
        if url is None:
            url = f"{self.URL}{pizza}/"
        self.page.goto(url)

    @allure.step("Выбор сырного или колбасного борта {b_type}")
    def choice(self, b_type: str = "Сырный - 55.00 р."):
        self.page.select_option(self.BOARD_SELECTOR, label=b_type)

    @allure.step("Получение стоимости пиццы")
    def pizza_price(self):
        return int(
            "".join(
                i for i in self.pizza_cost.inner_text().split(",")[0] if i.isdigit()
            )
        )

    @allure.step("Добавление в корзину")
    def add_to_card(self):
        self.add_button.click()
