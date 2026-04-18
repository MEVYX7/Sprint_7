import requests
import random
import string
from datetime import date, timedelta
from urls import BASE_URL, CREATE_COURIER
from methods.courier_methods import CourierMethods


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_chars = []
    current_length = 0
    while current_length < length:
        random_chars.append(random.choice(letters))
        current_length += 1
    return "".join(random_chars)


def register_new_courier():
    payload = {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }

    response = requests.post(BASE_URL + CREATE_COURIER, data=payload)
    return payload, response


def login_courier_and_get_id(payload):
    response = CourierMethods.login_courier(
        {"login": payload["login"], "password": payload["password"]}
    )
    return response.json().get("id")


def register_new_courier_and_get_id():
    payload, create_response = register_new_courier()
    courier_id = None
    if create_response.status_code == 201:
        courier_id = login_courier_and_get_id(payload)
    return payload, create_response, courier_id


def build_order_payload(color=None):
    delivery_date = (date.today() + timedelta(days=1)).isoformat()
    payload = {
        "firstName": "Ivan",
        "lastName": "Petrov",
        "address": "Tverskaya St, 12, apt. 34",
        "metroStation": 4,
        "phone": "+79991234567",
        "rentTime": 5,
        "deliveryDate": delivery_date,
        "comment": "Please call 10 minutes before delivery",
    }
    if color is not None:
        payload["color"] = color
    return payload
