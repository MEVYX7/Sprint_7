import allure
from methods.courier_methods import CourierMethods


class TestCreateCourier:
    @allure.title("Создание курьера с валидными данными")
    def test_create_courier_success(self, created_courier_id):
        response, payload, courier_id = created_courier_id
        response_json = response.json()

        assert response.status_code == 201
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert set(response_json.keys()) == {"ok"}
        assert response_json["ok"] is True

    @allure.title("Нельзя создать дубликат курьера")
    def test_create_duplicate_courier(self, duplicate_courier_setup):
        payload, first_response, courier_id = duplicate_courier_setup
        assert first_response.status_code == 201

        response = CourierMethods.create_courier(payload)
        response_json = response.json()

        assert response.status_code == 409
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert set(response_json.keys()) == {"code", "message"}
        assert response_json["code"] == 409
        assert response_json["message"] == "Этот логин уже используется. Попробуйте другой."

    @allure.title("Нельзя создать курьера без логина")
    def test_create_courier_without_login(self, courier_payload):
        payload = dict(courier_payload)
        del payload["login"]
        response = CourierMethods.create_courier(payload)
        response_json = response.json()

        assert response.status_code == 400
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert set(response_json.keys()) == {"code", "message"}
        assert response_json["code"] == 400
        assert response_json["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Нельзя создать курьера без пароля")
    def test_create_courier_without_password(self, courier_payload):
        payload = dict(courier_payload)
        del payload["password"]
        response = CourierMethods.create_courier(payload)
        response_json = response.json()

        assert response.status_code == 400
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert set(response_json.keys()) == {"code", "message"}
        assert response_json["code"] == 400
        assert response_json["message"] == "Недостаточно данных для создания учетной записи"
