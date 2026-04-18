import requests
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
    def create_order(payload):
        return requests.post(BASE_URL + CREATE_ORDER, json=payload)

    @staticmethod
    def get_orders():
        return requests.get(BASE_URL + GET_ORDERS)

    @staticmethod
    def accept_order(order_id, courier_id=None):
        params = {}
        if courier_id is not None:
            params["courierId"] = courier_id
        return requests.put(BASE_URL + ACCEPT_ORDER + str(order_id), params=params)

    @staticmethod
    def accept_order_without_id(courier_id=None):
        params = {}
        if courier_id is not None:
            params["courierId"] = courier_id
        return requests.put(BASE_URL + ACCEPT_ORDER, params=params)

    @staticmethod
    def cancel_order(track):
        return requests.put(BASE_URL + CANCEL_ORDER, params={"track": track})

    @staticmethod
    def cancel_order_without_track():
        return requests.put(BASE_URL + CANCEL_ORDER)

    @staticmethod
    def get_order_by_track(track):
        return requests.get(BASE_URL + ORDER_BY_TRACK, params={"t": track})

    @staticmethod
    def get_order_by_track_without_number():
        return requests.get(BASE_URL + ORDER_BY_TRACK)
