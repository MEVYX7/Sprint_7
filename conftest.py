import pytest
from helpers import register_new_courier_and_get_id
from methods.courier_methods import CourierMethods


@pytest.fixture
def courier():
    payload, create_response, courier_id = register_new_courier_and_get_id()

    assert create_response.status_code == 201
    assert courier_id is not None

    yield payload, courier_id

    if courier_id is not None:
        CourierMethods.delete_courier(courier_id)
