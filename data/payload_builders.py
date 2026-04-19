import random
import string
from datetime import date, timedelta


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_chars = []
    current_length = 0
    while current_length < length:
        random_chars.append(random.choice(letters))
        current_length += 1
    return "".join(random_chars)


def build_courier_payload():
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10),
    }


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
