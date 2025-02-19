import time
import allure
from playwright.sync_api import Page, expect


class MainPage:
    CARD = "//a[@title='View your shopping cart']"
    CONTAINER = "//section[@id='product1']"
    CARD_BUTTON = "//a[contains(@class, 'add_to_cart')]"
    PIZZA_HAM = CONTAINER + "//li[@data-slick-index='3']"
    PIZZA_4_IN_1 = CONTAINER + "//li[@data-slick-index='0']"
    PIZZA_PEPERONI = CONTAINER + "//li[@data-slick-index='4']"
    PIZZA_PRICE = "//span[contains(@class, 'Price-amoun')]"
    URL = "http://pizzeria.skillbox.cc/"

    def __init__(self, page: Page):
        self.page = page
        self.container = page.locator(self.CONTAINER)
        self.card_main = page.locator(self.CARD)
        self.pizza_ham = page.locator(self.PIZZA_HAM)
        self.pizza_4_in_1 = page.locator(self.PIZZA_4_IN_1)
        self.slider_left = page.locator(f"{self.CONTAINER}//a[@class='slick-prev']")
        self.slider_right = page.locator(f"{self.CONTAINER}//a[@class='slick-next']")
        self.pizza_ham_card_button = page.locator(f"{self.PIZZA_HAM}{self.CARD_BUTTON}")
        self.pizza_4_in_1_card_button = page.locator(
            f"{self.PIZZA_4_IN_1}{self.CARD_BUTTON}"
        )
        self.pizza_peperoni_card_button = page.locator(
            f"{self.PIZZA_PEPERONI}{self.CARD_BUTTON}"
        )
        self.pizza_ham_price = page.locator(f"{self.PIZZA_HAM}{self.PIZZA_PRICE}")
        self.pizza_peperoni_price = page.locator(
            f"{self.PIZZA_PEPERONI}{self.PIZZA_PRICE}"
        )
        self.pizza_4_in_1_price = page.locator(f"{self.PIZZA_4_IN_1}{self.PIZZA_PRICE}")

    @allure.step("Получение url текущей страницы")
    def get_url(self):
        return self.page.url

    @allure.step("Открытие страницы {url}")
    def open(self, url: str = URL):
        if url is None:
            url = self.URL
        self.page.goto(url)
        return url

    @allure.step("Получение стоимости корзины")
    def card_cost(self):
        return int(
            "".join(i for i in self.card_main.inner_text().split(",")[0] if i.isdigit())
        )

    @allure.step("Проверка изменения стоимости корзины")
    def check_change_card_cost(self, previous_cost: int):
        self.card_main.wait_for(state="attached", timeout=5000)
        current_cost = self.card_cost()
        time.sleep(1)
        assert current_cost != previous_cost

    @allure.step("Получение элемента кнопки корзины пиццы {pizza}")
    def card_button_status(self, pizza):
        if pizza == "ham":
            return self.pizza_ham_card_button
        elif pizza == "4in1":
            return self.pizza_4_in_1_card_button
        else:
            raise ValueError("Pizza must be 'ham' or '4in1'")

    @allure.step("Получение стоимости пиццы {pizza}")
    def pizza_price(self, pizza):
        if pizza == "ham":
            price = self.pizza_ham_price
        elif pizza == "4in1":
            price = self.pizza_4_in_1_price
        elif pizza == "peperoni":
            price = self.pizza_peperoni_price
        else:
            raise ValueError("Pizza must be 'ham' or '4in1' or 'peperoni'")
        return int("".join(i for i in price.inner_text().split(",")[0] if i.isdigit()))

    @allure.step("Наведение курсора на область элемента пиццы {pizza}")
    def pizza_hover(self, pizza):
        if pizza == "ham":
            pizza_locator = self.pizza_ham
        elif pizza == "4in1":
            pizza_locator = self.pizza_4_in_1
        else:
            raise ValueError("Pizza must be 'ham' or '4in1'")
        return pizza_locator.hover()

    @allure.step("Наведение курсора на контейнер для появления кнопки слайдера")
    def hover_over_slider(self):
        self.container.hover()

    @allure.step("Нажатие на слайдер в {direction}")
    def click_slider(self, direction: str):
        if direction == "left":
            slider = self.slider_left
        elif direction == "right":
            slider = self.slider_right
        else:
            raise ValueError("Direction must be 'left' or 'right'")
        slider.click()

    @allure.step("Проверка видимости пиццы в слайдере")
    def get_pizza_state(self, pizza: str):
        if pizza == "ham":
            pizza_locator = self.pizza_ham
        elif pizza == "4in1":
            pizza_locator = self.pizza_4_in_1
        else:
            raise ValueError("Pizza must be 'ham' or '4in1'")
        return pizza_locator.get_attribute("aria-hidden")

    @allure.step("Проверка того, что пицца скрыта в слайдере")
    def expect_pizza_hidden(self, pizza: str, expected_value: str):
        if pizza == "ham":
            pizza_locator = self.pizza_ham
        elif pizza == "4in1":
            pizza_locator = self.pizza_4_in_1
        else:
            raise ValueError("Pizza must be 'ham' or '4in1'")
        expect(pizza_locator).to_have_attribute("aria-hidden", expected_value)
