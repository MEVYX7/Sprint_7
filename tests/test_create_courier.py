import allure
from methods.courier_methods import CourierMethods
from helpers import generate_random_string, login_courier_and_get_id


class TestCreateCourier:

    @allure.title("Создание курьера с валидными данными")
    def test_create_courier_success(self):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10),
        }
        courier_id = None

        response = CourierMethods.create_courier(payload)

        if response.status_code == 201:
            courier_id = login_courier_and_get_id(payload)

        try:
            assert response.status_code == 201
            assert response.json() == {"ok": True}
        finally:
            if courier_id is not None:
                CourierMethods.delete_courier(courier_id)

    @allure.title("Нельзя создать дубликат курьера")
    def test_create_duplicate_courier(self):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10),
        }
        courier_id = None

        first_response = CourierMethods.create_courier(payload)
        if first_response.status_code == 201:
            courier_id = login_courier_and_get_id(payload)

        response = CourierMethods.create_courier(payload)
        response_json = response.json()

        try:
            assert response.status_code == 409
            assert response_json["code"] == 409
            assert "message" in response_json
        finally:
            if courier_id is not None:
                CourierMethods.delete_courier(courier_id)

    @allure.title("Нельзя создать курьера без логина")
    def test_create_courier_without_login(self):
        payload = {
            "password": generate_random_string(10),
            "firstName": generate_random_string(10),
        }

        response = CourierMethods.create_courier(payload)
        response_json = response.json()

        assert response.status_code == 400
        assert response_json["code"] == 400
        assert "message" in response_json

    @allure.title("Нельзя создать курьера без пароля")
    def test_create_courier_without_password(self):
        payload = {
            "login": generate_random_string(10),
            "firstName": generate_random_string(10),
        }

        response = CourierMethods.create_courier(payload)
        response_json = response.json()

        assert response.status_code == 400
        assert response_json["code"] == 400
        assert "message" in response_json
