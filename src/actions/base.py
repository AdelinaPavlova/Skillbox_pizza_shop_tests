import allure
import pytest
from playwright.sync_api import Page


# @pytest.fixture
# def go_to_url():
#     @allure.step('Открытие страницы {url}')
#     def callback(url):
#         Driver.get_driver().maximize_window()
#         Driver.get_driver().get(url)
#
#     return callback


class TestBase:
    @pytest.fixture(scope="function", autouse=True)
    def close_browser(self, page: Page):
        yield page
        page.close()

    @pytest.fixture(scope="function", autouse=True)
    def go_to_url(self, page: Page, timeout=240000):
        @allure.step("Открытие страницы {url}")
        def callback(url):
            page.set_viewport_size({"width": 1920, "height": 1080})
            page.goto(url, timeout=timeout)

        self.go_to_url = callback

    @pytest.fixture(scope="function", autouse=True)
    def move_slider(self, page: Page):
        @allure.step("Передвижение слайдера на {offset_x}, {offset_y}")
        def move(locator: str, offset_x: int, offset_y: int):
            box = page.locator(locator).bounding_box()
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.mouse.down()
            page.mouse.move(
                box["x"] + box["width"] / 2 + offset_x,
                box["y"] + box["height"] / 2 + offset_y,
            )
            page.mouse.up()

        self.move_slider = move

    @pytest.fixture(scope="function", autouse=True)
    def send_keys_to_element(self, page: Page):
        @allure.step("Ввод текста {keys} в строку элемента {locator}")
        def send_keys(locator: str, keys: str, timeout: int = 15000):
            page.wait_for_selector(locator, timeout=timeout).fill(keys)

        self.send_keys_to_element = send_keys

    @pytest.fixture(scope="function", autouse=True)
    def push_key(self, page: Page):
        @allure.step("Нажатие клавиши {button}")
        def push_keys(locator: str, button: str, timeout: int = 15000):
            page.wait_for_selector(locator, timeout=timeout).press(button)

        self.push_key = push_keys

    @pytest.fixture(scope="function", autouse=True)
    def click_element(self, page: Page):
        @allure.step("Клик по элементу {locator}")
        def click(locator: str, timeout: int = 15000):
            page.wait_for_selector(locator, timeout=timeout).click()

        self.click_element = click

    @pytest.fixture(scope="function", autouse=True)
    def get_elements_text(self, page: Page):
        @allure.step("Получение текста всех элементов с локатором {locator}")
        def get_text(locator: str):
            return page.locator(locator).all_inner_texts()

        self.get_elements_text = get_text

    @pytest.fixture(scope="function", autouse=True)
    def get_element(self, page: Page):
        @allure.step("Получение элемента")
        def wait(locator: str, timeout: int = 15000):
            page.wait_for_selector(locator, timeout=timeout)

        self.get_element = wait
