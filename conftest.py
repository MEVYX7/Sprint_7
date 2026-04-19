import pytest
from data.payload_builders import build_courier_payload, build_order_payload
from flows.courier_flow import login_courier_and_get_id, register_new_courier_and_get_id
from methods.courier_methods import CourierMethods
from methods.order_methods import OrderMethods


@pytest.fixture
def registered_courier(request):
    payload, create_response, courier_id = register_new_courier_and_get_id()
    yield payload, create_response, courier_id

    skip_cleanup = request.node.get_closest_marker("skip_registered_courier_cleanup")
    if courier_id is not None and skip_cleanup is None:
        CourierMethods.delete_courier(courier_id)


@pytest.fixture
def courier(registered_courier):
    payload, create_response, courier_id = registered_courier

    if create_response.status_code != 201:
        pytest.fail(f"Не удалось создать курьера, status_code={create_response.status_code}")
    if courier_id is None:
        pytest.fail("Не удалось получить id созданного курьера")

    return payload, courier_id


@pytest.fixture
def courier_payload():
    return build_courier_payload()


@pytest.fixture
def courier_payload_without_login():
    payload = build_courier_payload()
    del payload["login"]
    return payload


@pytest.fixture
def courier_payload_without_password():
    payload = build_courier_payload()
    del payload["password"]
    return payload


@pytest.fixture
def created_courier_id(courier_payload):
    response = CourierMethods.create_courier(courier_payload)
    courier_id = None
    if response.status_code == 201:
        courier_id = login_courier_and_get_id(courier_payload)

    yield response, courier_payload, courier_id

    if courier_id is not None:
        CourierMethods.delete_courier(courier_id)


@pytest.fixture
def duplicate_courier_setup(courier_payload):
    create_response = CourierMethods.create_courier(courier_payload)
    courier_id = None
    if create_response.status_code == 201:
        courier_id = login_courier_and_get_id(courier_payload)

    yield courier_payload, create_response, courier_id

    if courier_id is not None:
        CourierMethods.delete_courier(courier_id)


@pytest.fixture
def created_order(request):
    color = getattr(request, "param", ["GREY"])
    create_response = OrderMethods.create_order(build_order_payload(color))

    if create_response.status_code != 201:
        pytest.fail(f"Не удалось создать заказ, status_code={create_response.status_code}")
    track = create_response.json().get("track")
    if track is None:
        pytest.fail("В ответе на создание заказа отсутствует track")

    order_response = OrderMethods.get_order_by_track(track)
    if order_response.status_code != 200:
        pytest.fail(
            "Не удалось получить заказ по track, "
            f"status_code={order_response.status_code}, track={track}"
        )
    order_id = order_response.json()["order"]["id"]

    yield track, order_id

    if track is not None:
        OrderMethods.cancel_order(track)


@pytest.fixture
def created_order_response(request):
    color = getattr(request, "param", None)
    response = OrderMethods.create_order(build_order_payload(color))
    track = response.json().get("track")

    yield response, track

    if track is not None:
        OrderMethods.cancel_order(track)
