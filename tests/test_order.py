import allure
import pytest
from assertions.response_assertions import (
    assert_create_order_success_response,
    assert_json_error_response,
    assert_ok_response,
    assert_text_error_response,
)
from methods.order_methods import OrderMethods


class TestOrder:
    @pytest.mark.parametrize(
        "created_order_response",
        [
            ["BLACK"],
            ["GREY"],
            ["BLACK", "GREY"],
        ],
        indirect=True,
    )
    @allure.title("Создание заказа с цветом")
    def test_create_order_with_color(self, created_order_response):
        response, track = created_order_response

        assert_create_order_success_response(response)
        assert response.json()["track"] == track

    @allure.title("Создание заказа без цвета")
    def test_create_order_without_color(self, created_order_response):
        response, track = created_order_response

        assert_create_order_success_response(response)
        assert response.json()["track"] == track

    @pytest.mark.parametrize("created_order_response", [[]], indirect=True)
    @allure.title("Создание заказа, когда не выбран ни один цвет")
    def test_create_order_with_empty_color_list(self, created_order_response):
        response, track = created_order_response

        assert_create_order_success_response(response)
        assert response.json()["track"] == track

    @allure.title("Получение списка заказов")
    def test_get_orders(self):
        response = OrderMethods.get_orders()
        response_json = response.json()

        assert response.status_code == 200
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert "orders" in response_json
        assert "pageInfo" in response_json
        assert "availableStations" in response_json
        assert isinstance(response_json["orders"], list)
        assert isinstance(response_json["pageInfo"], dict)
        assert isinstance(response_json["availableStations"], list)

    @allure.title("Получение заказа по валидному номеру")
    def test_get_order_by_number_success(self, created_order):
        track, order_id = created_order
        response = OrderMethods.get_order_by_track(track)
        response_json = response.json()

        assert response.status_code == 200
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert set(response_json.keys()) == {"order"}
        assert isinstance(response_json["order"], dict)
        assert "id" in response_json["order"]
        assert isinstance(response_json["order"]["id"], int)

    @allure.title("Получение заказа без номера возвращает ошибку")
    def test_get_order_by_number_without_number(self):
        response = OrderMethods.get_order_by_track_without_number()
        assert_json_error_response(
            response,
            expected_status_code=400,
            expected_code=400,
            expected_message="Недостаточно данных для поиска",
        )

    @allure.title("Получение заказа по несуществующему номеру возвращает ошибку")
    def test_get_order_by_number_non_existent(self):
        response = OrderMethods.get_order_by_track(999999999)
        assert_json_error_response(
            response,
            expected_status_code=404,
            expected_code=404,
            expected_message="Заказ не найден",
        )

    @allure.title("Успешное принятие заказа курьером")
    def test_accept_order_success(self, courier, created_order):
        courier_id = courier[1]
        track, order_id = created_order

        response = OrderMethods.accept_order(order_id, courier_id)
        assert_ok_response(response)

    @allure.title("Принятие заказа без courierId возвращает ошибку")
    def test_accept_order_without_courier_id(self, created_order):
        track, order_id = created_order
        response = OrderMethods.accept_order(order_id)
        assert_json_error_response(
            response,
            expected_status_code=400,
            expected_code=400,
            expected_message="Недостаточно данных для поиска",
        )

    @allure.title("Принятие заказа с неверным courierId возвращает ошибку")
    def test_accept_order_with_wrong_courier_id(self, created_order):
        track, order_id = created_order
        response = OrderMethods.accept_order(order_id, 999999)
        assert_json_error_response(
            response,
            expected_status_code=404,
            expected_code=404,
            expected_message="Курьера с таким id не существует",
        )

    @allure.title("Принятие заказа без orderId возвращает ошибку")
    def test_accept_order_without_order_id(self, courier):
        courier_id = courier[1]
        response = OrderMethods.accept_order_without_id(courier_id)
        assert_text_error_response(response, expected_status_code=404, expected_text="Not Found.")

    @allure.title("Принятие заказа с неверным orderId возвращает ошибку")
    def test_accept_order_with_wrong_order_id(self, courier):
        courier_id = courier[1]
        response = OrderMethods.accept_order(999999, courier_id)
        assert_json_error_response(
            response,
            expected_status_code=404,
            expected_code=404,
            expected_message="Заказа с таким id не существует",
        )
