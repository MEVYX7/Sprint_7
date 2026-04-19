import requests
import allure
from urls import BASE_URL, CREATE_COURIER, LOGIN_COURIER, DELETE_COURIER


class CourierMethods:

    @staticmethod
    @allure.step("Создать курьера")
    def create_courier(payload):
        return requests.post(BASE_URL + CREATE_COURIER, data=payload)

    @staticmethod
    @allure.step("Логин курьера")
    def login_courier(payload):
        return requests.post(BASE_URL + LOGIN_COURIER, data=payload)

    @staticmethod
    @allure.step("Удалить курьера по id: {courier_id}")
    def delete_courier(courier_id):
        return requests.delete(BASE_URL + DELETE_COURIER + str(courier_id))

    @staticmethod
    @allure.step("Удалить курьера без id")
    def delete_courier_without_id():
        return requests.delete(BASE_URL + DELETE_COURIER)
