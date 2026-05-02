import allure
import pytest
from methods.courier_methods import CourierMethods


class TestDeleteCourier:
    @allure.title("Успешное удаление курьера по id")
    @pytest.mark.skip_registered_courier_cleanup
    def test_delete_courier_success(self, registered_courier):
        payload, create_response, courier_id = registered_courier
        response = CourierMethods.delete_courier(courier_id)
        response_json = response.json()

        assert create_response.status_code == 201
        assert courier_id is not None
        assert "login" in payload
        assert response.status_code == 200
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert set(response_json.keys()) == {"ok"}
        assert response_json["ok"] is True

    @allure.title("Удаление курьера без id возвращает ошибку")
    def test_delete_courier_without_id(self):
        response = CourierMethods.delete_courier_without_id()

        assert response.status_code == 404
        assert response.text is not None
        assert "Not Found." in response.text

    @allure.title("Удаление курьера с несуществующим id возвращает ошибку")
    def test_delete_courier_with_non_existent_id(self):
        response = CourierMethods.delete_courier(999999)
        response_json = response.json()

        assert response.status_code == 404
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert set(response_json.keys()) == {"code", "message"}
        assert response_json["code"] == 404
        assert response_json["message"] == "Курьера с таким id нет."
