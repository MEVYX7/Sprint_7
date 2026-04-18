import requests
from urls import BASE_URL, CREATE_COURIER, LOGIN_COURIER, DELETE_COURIER


class CourierMethods:

    @staticmethod
    def create_courier(payload):
        return requests.post(BASE_URL + CREATE_COURIER, data=payload)

    @staticmethod
    def login_courier(payload):
        return requests.post(BASE_URL + LOGIN_COURIER, data=payload)

    @staticmethod
    def delete_courier(courier_id):
        return requests.delete(BASE_URL + DELETE_COURIER + str(courier_id))

    @staticmethod
    def delete_courier_without_id():
        return requests.delete(BASE_URL + DELETE_COURIER)
