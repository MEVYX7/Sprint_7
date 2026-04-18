import allure
from helpers import register_new_courier_and_get_id
from methods.courier_methods import CourierMethods


class TestDeleteCourier:

    @allure.title("Успешное удаление курьера по id")
    def test_delete_courier_success(self):
        payload, create_response, courier_id = register_new_courier_and_get_id()
        assert create_response.status_code == 201
        assert courier_id is not None
        assert "login" in payload

        response = CourierMethods.delete_courier(courier_id)

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Удаление курьера без id возвращает ошибку")
    def test_delete_courier_without_id(self):
        response = CourierMethods.delete_courier_without_id()

        assert response.status_code == 404
        try:
            response_json = response.json()
            assert "message" in response_json
        except ValueError:
            assert response.text != ""

    @allure.title("Удаление курьера с несуществующим id возвращает ошибку")
    def test_delete_courier_with_non_existent_id(self):
        response = CourierMethods.delete_courier(999999)
        response_json = response.json()

        assert response.status_code == 404
        assert response_json["code"] == 404
        assert "message" in response_json
