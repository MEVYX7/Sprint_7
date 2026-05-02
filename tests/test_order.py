import allure
import pytest
from data.test_data import ORDER_COLOR_VARIANTS
from methods.order_methods import OrderMethods


class TestCreateOrder:
    @pytest.mark.parametrize(
        "created_order_response",
        ORDER_COLOR_VARIANTS,
        indirect=True,
    )
    @allure.title("Создание заказа с вариантами цвета")
    def test_create_order_with_color_options(self, created_order_response):
        response, track = created_order_response
        response_json = response.json()

        assert response.status_code == 201
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert set(response_json.keys()) == {"track"}
        assert isinstance(response_json["track"], int)
        assert response_json["track"] == track

    @allure.title("Создание заказа без поля color")
    def test_create_order_without_color(self, created_order_response):
        response, track = created_order_response
        response_json = response.json()

        assert response.status_code == 201
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert set(response_json.keys()) == {"track"}
        assert isinstance(response_json["track"], int)
        assert response_json["track"] == track


class TestGetOrders:
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


class TestGetOrderByNumber:
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
        response_json = response.json()

        assert response.status_code == 400
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert set(response_json.keys()) == {"code", "message"}
        assert response_json["code"] == 400
        assert response_json["message"] == "Недостаточно данных для поиска"

    @allure.title("Получение заказа по несуществующему номеру возвращает ошибку")
    def test_get_order_by_number_non_existent(self):
        response = OrderMethods.get_order_by_track(999999999)
        response_json = response.json()

        assert response.status_code == 404
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert set(response_json.keys()) == {"code", "message"}
        assert response_json["code"] == 404
        assert response_json["message"] == "Заказ не найден"


class TestAcceptOrder:
    @allure.title("Успешное принятие заказа курьером")
    def test_accept_order_success(self, courier, created_order):
        courier_id = courier[1]
        track, order_id = created_order
        response = OrderMethods.accept_order(order_id, courier_id)
        response_json = response.json()

        assert response.status_code == 200
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert set(response_json.keys()) == {"ok"}
        assert response_json["ok"] is True

    @allure.title("Принятие заказа без courierId возвращает ошибку")
    def test_accept_order_without_courier_id(self, created_order):
        track, order_id = created_order
        response = OrderMethods.accept_order(order_id)
        response_json = response.json()

        assert response.status_code == 400
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert set(response_json.keys()) == {"code", "message"}
        assert response_json["code"] == 400
        assert response_json["message"] == "Недостаточно данных для поиска"

    @allure.title("Принятие заказа с неверным courierId возвращает ошибку")
    def test_accept_order_with_wrong_courier_id(self, created_order):
        track, order_id = created_order
        response = OrderMethods.accept_order(order_id, 999999)
        response_json = response.json()

        assert response.status_code == 404
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert set(response_json.keys()) == {"code", "message"}
        assert response_json["code"] == 404
        assert response_json["message"] == "Курьера с таким id не существует"

    @allure.title("Принятие заказа без orderId возвращает ошибку")
    def test_accept_order_without_order_id(self, courier):
        courier_id = courier[1]
        response = OrderMethods.accept_order_without_id(courier_id)

        assert response.status_code == 404
        assert response.text is not None
        assert "Not Found." in response.text

    @allure.title("Принятие заказа с неверным orderId возвращает ошибку")
    def test_accept_order_with_wrong_order_id(self, courier):
        courier_id = courier[1]
        response = OrderMethods.accept_order(999999, courier_id)
        response_json = response.json()

        assert response.status_code == 404
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert set(response_json.keys()) == {"code", "message"}
        assert response_json["code"] == 404
        assert response_json["message"] == "Заказа с таким id не существует"
