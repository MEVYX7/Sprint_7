import allure
from helpers import generate_random_string
from methods.courier_methods import CourierMethods


class TestLoginCourier:
    @allure.title("Успешный логин курьера")
    def test_login_success(self, courier):
        payload = courier[0]
        response = CourierMethods.login_courier(
            {"login": payload["login"], "password": payload["password"]}
        )
        response_json = response.json()

        assert response.status_code == 200
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert set(response_json.keys()) == {"id"}
        assert isinstance(response_json["id"], int)

    @allure.title("Логин с неверным паролем возвращает ошибку")
    def test_login_wrong_password(self, courier):
        payload = courier[0]
        response = CourierMethods.login_courier(
            {"login": payload["login"], "password": generate_random_string(10)}
        )
        response_json = response.json()

        assert response.status_code == 404
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert set(response_json.keys()) == {"code", "message"}
        assert response_json["code"] == 404
        assert response_json["message"] == "Учетная запись не найдена"

    @allure.title("Логин с неверным логином возвращает ошибку")
    def test_login_wrong_login(self, courier):
        payload = courier[0]
        response = CourierMethods.login_courier(
            {"login": generate_random_string(10), "password": payload["password"]}
        )
        response_json = response.json()

        assert response.status_code == 404
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert set(response_json.keys()) == {"code", "message"}
        assert response_json["code"] == 404
        assert response_json["message"] == "Учетная запись не найдена"

    @allure.title("Логин без поля login возвращает ошибку")
    def test_login_without_login(self, courier):
        payload = courier[0]
        response = CourierMethods.login_courier({"password": payload["password"]})
        response_json = response.json()

        assert response.status_code == 400
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert set(response_json.keys()) == {"code", "message"}
        assert response_json["code"] == 400
        assert response_json["message"] == "Недостаточно данных для входа"

    @allure.title("Логин без поля password возвращает ошибку")
    def test_login_without_password(self):
        response = CourierMethods.login_courier({"login": generate_random_string(10)})
        response_json = response.json()

        assert response.status_code == 400
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert set(response_json.keys()) == {"code", "message"}
        assert response_json["code"] == 400
        assert response_json["message"] == "Недостаточно данных для входа"

    @allure.title("Логин несуществующего курьера возвращает ошибку")
    def test_login_non_existent_courier(self):
        response = CourierMethods.login_courier(
            {"login": generate_random_string(10), "password": generate_random_string(10)}
        )
        response_json = response.json()

        assert response.status_code == 404
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert set(response_json.keys()) == {"code", "message"}
        assert response_json["code"] == 404
        assert response_json["message"] == "Учетная запись не найдена"
