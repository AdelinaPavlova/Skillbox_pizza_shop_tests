import allure
from playwright.sync_api import Page


class DesertsPage:
    CARD = "//a[@title='View your shopping cart']"
    URL = "http://pizzeria.skillbox.cc/product-category/menu/deserts/"

    def __init__(self, page: Page):
        self.page = page
        self.slider = page.locator("//span[@style='left: 100%;']")
        self.submit_button = page.locator("//button[text()='Применить']")
        self.deserts = page.locator("//span[@class='price']")

    @allure.step("Получение url текущей страницы")
    def get_url(self):
        return self.page.url

    @allure.step("Открытие страницы {url}")
    def open(self, url: str = URL):
        if url is None:
            url = self.URL
        self.page.goto(url)
        return url

    @allure.step("Передвижение слайдера")
    def move_slider(self, offset_x: int, offset_y: int):
        box = self.slider.bounding_box()
        self.page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        self.page.mouse.down()
        self.page.mouse.move(
            box["x"] + box["width"] / 2 + offset_x,
            box["y"] + box["height"] / 2 + offset_y,
        )
        self.page.mouse.up()

    @allure.step("Получение цен десертов")
    def get_deserts_prices(self):
        return [
            int("".join(filter(str.isdigit, text.split(","[0]))))
            for text in self.deserts.all_inner_texts()
        ]

    @allure.step("Узнать цену десерта {desert}")
    def get_price(self, desert="Морковный каприз"):
        desert_price = self.page.locator(
            f"//a[contains(@aria-label, '{desert}')]/parent::*/span"
        ).inner_text()
        return int("".join(i for i in desert_price.split(",")[0] if i.isdigit()))

    @allure.step("Добавить в корзину десерт {desert}")
    def add_desert(self, desert="Морковный каприз"):
        self.page.locator(f"//a[contains(@aria-label, '{desert}')]").click()
