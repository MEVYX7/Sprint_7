from datetime import date, timedelta
from data.test_data import faker, COURIER_CREDENTIAL_LENGTH, ORDER_BASE_PAYLOAD


def build_courier_payload():
    return {
        "login": faker.pystr(min_chars=COURIER_CREDENTIAL_LENGTH, max_chars=COURIER_CREDENTIAL_LENGTH).lower(),
        "password": faker.pystr(min_chars=COURIER_CREDENTIAL_LENGTH, max_chars=COURIER_CREDENTIAL_LENGTH),
        "firstName": faker.first_name(),
    }


def build_order_payload(color=None):
    delivery_date = (date.today() + timedelta(days=1)).isoformat()
    payload = dict(ORDER_BASE_PAYLOAD)
    payload["deliveryDate"] = delivery_date
    if color is not None:
        payload["color"] = color
    return payload
