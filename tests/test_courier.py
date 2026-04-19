import allure
import pytest
from assertions.response_assertions import (
    assert_json_error_response,
    assert_login_success_response,
    assert_ok_response,
    assert_text_error_response,
)
from data.payload_builders import generate_random_string
from methods.courier_methods import CourierMethods


class TestCourier:
    @allure.title("Создание курьера с валидными данными")
    def test_create_courier_success(self, created_courier_id):
        response, payload, courier_id = created_courier_id
        assert response.status_code == 201
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert response.json() == {"ok": True}

    @allure.title("Нельзя создать дубликат курьера")
    def test_create_duplicate_courier(self, duplicate_courier_setup):
        payload, first_response, courier_id = duplicate_courier_setup
        assert first_response.status_code == 201

        response = CourierMethods.create_courier(payload)
        assert_json_error_response(
            response,
            expected_status_code=409,
            expected_code=409,
            expected_message="Этот логин уже используется. Попробуйте другой.",
        )

    @allure.title("Нельзя создать курьера без логина")
    def test_create_courier_without_login(self, courier_payload_without_login):
        response = CourierMethods.create_courier(courier_payload_without_login)
        assert_json_error_response(
            response,
            expected_status_code=400,
            expected_code=400,
            expected_message="Недостаточно данных для создания учетной записи",
        )

    @allure.title("Нельзя создать курьера без пароля")
    def test_create_courier_without_password(self, courier_payload_without_password):
        response = CourierMethods.create_courier(courier_payload_without_password)
        assert_json_error_response(
            response,
            expected_status_code=400,
            expected_code=400,
            expected_message="Недостаточно данных для создания учетной записи",
        )

    @allure.title("Успешный логин курьера")
    def test_login_success(self, courier):
        payload = courier[0]
        response = CourierMethods.login_courier(
            {"login": payload["login"], "password": payload["password"]}
        )
        assert_login_success_response(response)

    @allure.title("Логин с неверным паролем возвращает ошибку")
    def test_login_wrong_password(self, courier):
        payload = courier[0]
        response = CourierMethods.login_courier(
            {"login": payload["login"], "password": generate_random_string(10)}
        )
        assert_json_error_response(
            response,
            expected_status_code=404,
            expected_code=404,
            expected_message="Учетная запись не найдена",
        )

    @allure.title("Логин с неверным логином возвращает ошибку")
    def test_login_wrong_login(self, courier):
        payload = courier[0]
        response = CourierMethods.login_courier(
            {"login": generate_random_string(10), "password": payload["password"]}
        )
        assert_json_error_response(
            response,
            expected_status_code=404,
            expected_code=404,
            expected_message="Учетная запись не найдена",
        )

    @allure.title("Логин без поля login возвращает ошибку")
    def test_login_without_login(self, courier):
        payload = courier[0]
        response = CourierMethods.login_courier({"password": payload["password"]})
        assert_json_error_response(
            response,
            expected_status_code=400,
            expected_code=400,
            expected_message="Недостаточно данных для входа",
        )

    @allure.title("Логин без поля password возвращает ошибку")
    def test_login_without_password(self):
        response = CourierMethods.login_courier({"login": generate_random_string(10)})
        assert_json_error_response(
            response,
            expected_status_code=400,
            expected_code=400,
            expected_message="Недостаточно данных для входа",
        )

    @allure.title("Логин несуществующего курьера возвращает ошибку")
    def test_login_non_existent_courier(self):
        response = CourierMethods.login_courier(
            {"login": generate_random_string(10), "password": generate_random_string(10)}
        )
        assert_json_error_response(
            response,
            expected_status_code=404,
            expected_code=404,
            expected_message="Учетная запись не найдена",
        )

    @allure.title("Успешное удаление курьера по id")
    @pytest.mark.skip_registered_courier_cleanup
    def test_delete_courier_success(self, registered_courier):
        payload, create_response, courier_id = registered_courier
        assert create_response.status_code == 201
        assert courier_id is not None
        assert "login" in payload

        response = CourierMethods.delete_courier(courier_id)
        assert_ok_response(response)

    @allure.title("Удаление курьера без id возвращает ошибку")
    def test_delete_courier_without_id(self):
        response = CourierMethods.delete_courier_without_id()
        assert_text_error_response(response, expected_status_code=404, expected_text="Not Found.")

    @allure.title("Удаление курьера с несуществующим id возвращает ошибку")
    def test_delete_courier_with_non_existent_id(self):
        response = CourierMethods.delete_courier(999999)
        assert_json_error_response(
            response,
            expected_status_code=404,
            expected_code=404,
            expected_message="Курьера с таким id нет.",
        )
