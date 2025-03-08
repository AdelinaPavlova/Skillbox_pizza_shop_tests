import allure
import logging.config
from pages.main_page import MainPage

logging.basicConfig(encoding="utf-8")


@allure.feature("Skillbox tests")
@allure.story("Slider assertion")
class TestSlider:

    @allure.title("Проверка функциональности левой кнопки слайдера")
    def test_slider_left(self, page):
        slider = MainPage(page)
        slider.open()
        slider.hover_over_slider()
        slider.click_slider(direction="left")
        with allure.step("Проверка корректной работы левой кнопки слайдера"):
            slider.expect_pizza_hidden("ham", "true")

    @allure.title("Проверка функциональности правой кнопки слайдера")
    def test_slider_right(self, page):
        slider = MainPage(page)
        slider.open()
        slider.hover_over_slider()
        slider.click_slider(direction="right")
        with allure.step("Проверка корректной работы правой кнопки слайдера"):
            slider.expect_pizza_hidden("4in1", "true")
