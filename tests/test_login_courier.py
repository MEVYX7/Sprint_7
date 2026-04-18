import allure
from methods.courier_methods import CourierMethods
from helpers import generate_random_string


class TestLoginCourier:

    @allure.title("Успешный логин курьера")
    def test_login_success(self, courier):
        payload = courier[0]

        response = CourierMethods.login_courier(
            {"login": payload["login"], "password": payload["password"]}
        )

        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Логин с неверным паролем возвращает ошибку")
    def test_login_wrong_password(self, courier):
        payload = courier[0]

        response = CourierMethods.login_courier(
            {"login": payload["login"], "password": generate_random_string(10)}
        )
        response_json = response.json()

        assert response.status_code == 404
        assert response_json["code"] == 404
        assert "message" in response_json

    @allure.title("Логин с неверным логином возвращает ошибку")
    def test_login_wrong_login(self, courier):
        payload = courier[0]

        response = CourierMethods.login_courier(
            {"login": generate_random_string(10), "password": payload["password"]}
        )
        response_json = response.json()

        assert response.status_code == 404
        assert response_json["code"] == 404
        assert "message" in response_json

    @allure.title("Логин без поля login возвращает ошибку")
    def test_login_without_login(self, courier):
        payload = courier[0]

        response = CourierMethods.login_courier({"password": payload["password"]})
        response_json = response.json()

        assert response.status_code == 400
        assert response_json["code"] == 400
        assert "message" in response_json

    @allure.title("Логин без поля password возвращает ошибку")
    def test_login_without_password(self):
        response = CourierMethods.login_courier({"login": generate_random_string(10)})

        assert response.status_code == 400
        try:
            response_json = response.json()
            assert "message" in response_json
            if "code" in response_json:
                assert response_json["code"] == 400
        except ValueError:
            assert response.text != ""

    @allure.title("Логин несуществующего курьера возвращает ошибку")
    def test_login_non_existent_courier(self):
        response = CourierMethods.login_courier(
            {"login": generate_random_string(10), "password": generate_random_string(10)}
        )
        response_json = response.json()

        assert response.status_code == 404
        assert response_json["code"] == 404
        assert "message" in response_json
