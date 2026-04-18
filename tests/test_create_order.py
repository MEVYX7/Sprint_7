import allure
import pytest
from helpers import build_order_payload
from methods.order_methods import OrderMethods


class TestCreateOrder:

    @pytest.mark.parametrize(
        "color",
        [
            ["BLACK"],
            ["GREY"],
            ["BLACK", "GREY"],
        ],
    )
    @allure.title("Создание заказа с цветом")
    def test_create_order_with_color(self, color):
        response = OrderMethods.create_order(build_order_payload(color))
        response_json = response.json()
        track = response_json.get("track")

        try:
            assert response.status_code == 201
            assert track is not None
        finally:
            if track is not None:
                OrderMethods.cancel_order(track)

    @allure.title("Создание заказа без цвета")
    def test_create_order_without_color(self):
        response = OrderMethods.create_order(build_order_payload())
        response_json = response.json()
        track = response_json.get("track")

        try:
            assert response.status_code == 201
            assert track is not None
        finally:
            if track is not None:
                OrderMethods.cancel_order(track)
