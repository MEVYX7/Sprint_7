from data.payload_builders import build_courier_payload
from methods.courier_methods import CourierMethods


def register_new_courier():
    payload = build_courier_payload()
    response = CourierMethods.create_courier(payload)
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
