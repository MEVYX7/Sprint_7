import allure
from helpers import build_order_payload
from methods.order_methods import OrderMethods


class TestGetOrderByNumber:

    @allure.title("Получение заказа по валидному номеру")
    def test_get_order_by_number_success(self):
        create_response = OrderMethods.create_order(build_order_payload(["BLACK"]))
        track = create_response.json().get("track")

        try:
            response = OrderMethods.get_order_by_track(track)

            assert response.status_code == 200
            assert "order" in response.json()
        finally:
            if track is not None:
                OrderMethods.cancel_order(track)

    @allure.title("Получение заказа без номера возвращает ошибку")
    def test_get_order_by_number_without_number(self):
        response = OrderMethods.get_order_by_track_without_number()
        response_json = response.json()

        assert response.status_code == 400
        assert response_json["code"] == 400
        assert "message" in response_json

    @allure.title("Получение заказа по несуществующему номеру возвращает ошибку")
    def test_get_order_by_number_non_existent(self):
        response = OrderMethods.get_order_by_track(999999999)
        response_json = response.json()

        assert response.status_code == 404
        assert response_json["code"] == 404
        assert "message" in response_json
