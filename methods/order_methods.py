import requests
import allure
from urls import (
    BASE_URL,
    CREATE_ORDER,
    GET_ORDERS,
    ACCEPT_ORDER,
    CANCEL_ORDER,
    ORDER_BY_TRACK,
)


class OrderMethods:

    @staticmethod
    @allure.step("Создать заказ")
    def create_order(payload):
        return requests.post(BASE_URL + CREATE_ORDER, json=payload)

    @staticmethod
    @allure.step("Получить список заказов")
    def get_orders():
        return requests.get(BASE_URL + GET_ORDERS)

    @staticmethod
    @allure.step("Принять заказ: order_id={order_id}, courier_id={courier_id}")
    def accept_order(order_id, courier_id=None):
        params = {}
        if courier_id is not None:
            params["courierId"] = courier_id
        return requests.put(BASE_URL + ACCEPT_ORDER + str(order_id), params=params)

    @staticmethod
    @allure.step("Принять заказ без order_id: courier_id={courier_id}")
    def accept_order_without_id(courier_id=None):
        params = {}
        if courier_id is not None:
            params["courierId"] = courier_id
        return requests.put(BASE_URL + ACCEPT_ORDER, params=params)

    @staticmethod
    @allure.step("Отменить заказ: track={track}")
    def cancel_order(track):
        return requests.put(BASE_URL + CANCEL_ORDER, params={"track": track})

    @staticmethod
    @allure.step("Отменить заказ без track")
    def cancel_order_without_track():
        return requests.put(BASE_URL + CANCEL_ORDER)

    @staticmethod
    @allure.step("Получить заказ по треку: track={track}")
    def get_order_by_track(track):
        return requests.get(BASE_URL + ORDER_BY_TRACK, params={"t": track})

    @staticmethod
    @allure.step("Получить заказ без номера")
    def get_order_by_track_without_number():
        return requests.get(BASE_URL + ORDER_BY_TRACK)
