import allure
from helpers import build_order_payload
from methods.order_methods import OrderMethods


def create_order_and_get_id():
    create_response = OrderMethods.create_order(build_order_payload(["GREY"]))
    assert create_response.status_code == 201
    track = create_response.json().get("track")
    assert track is not None

    order_response = OrderMethods.get_order_by_track(track)
    assert order_response.status_code == 200
    order_id = order_response.json()["order"]["id"]
    return track, order_id


class TestAcceptOrder:

    @allure.title("Успешное принятие заказа курьером")
    def test_accept_order_success(self, courier):
        courier_id = courier[1]
        track, order_id = create_order_and_get_id()

        try:
            response = OrderMethods.accept_order(order_id, courier_id)

            assert response.status_code == 200
            assert response.json() == {"ok": True}
        finally:
            if track is not None:
                OrderMethods.cancel_order(track)

    @allure.title("Принятие заказа без courierId возвращает ошибку")
    def test_accept_order_without_courier_id(self):
        track, order_id = create_order_and_get_id()
        try:
            response = OrderMethods.accept_order(order_id)
            response_json = response.json()

            assert response.status_code == 400
            assert response_json["code"] == 400
            assert "message" in response_json
        finally:
            if track is not None:
                OrderMethods.cancel_order(track)

    @allure.title("Принятие заказа с неверным courierId возвращает ошибку")
    def test_accept_order_with_wrong_courier_id(self):
        track, order_id = create_order_and_get_id()
        try:
            response = OrderMethods.accept_order(order_id, 999999)
            response_json = response.json()

            assert response.status_code == 404
            assert response_json["code"] == 404
            assert "message" in response_json
        finally:
            if track is not None:
                OrderMethods.cancel_order(track)

    @allure.title("Принятие заказа без orderId возвращает ошибку")
    def test_accept_order_without_order_id(self, courier):
        courier_id = courier[1]
        response = OrderMethods.accept_order_without_id(courier_id)

        assert response.status_code == 404
        try:
            response_json = response.json()
            assert "message" in response_json
        except ValueError:
            assert response.text != ""

    @allure.title("Принятие заказа с неверным orderId возвращает ошибку")
    def test_accept_order_with_wrong_order_id(self, courier):
        courier_id = courier[1]
        response = OrderMethods.accept_order(999999, courier_id)
        response_json = response.json()

        assert response.status_code == 404
        assert response_json["code"] == 404
        assert "message" in response_json
