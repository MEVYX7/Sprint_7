def assert_json_error_response(response, expected_status_code, expected_code, expected_message):
    assert response.status_code == expected_status_code
    assert response.headers.get("Content-Type", "").startswith("application/json")
    response_json = response.json()
    assert set(response_json.keys()) == {"code", "message"}
    assert response_json["code"] == expected_code
    assert response_json["message"] == expected_message


def assert_text_error_response(response, expected_status_code, expected_text):
    assert response.status_code == expected_status_code
    assert response.text is not None
    if expected_text:
        assert expected_text in response.text


def assert_ok_response(response):
    assert response.status_code == 200
    assert response.headers.get("Content-Type", "").startswith("application/json")
    assert response.json() == {"ok": True}


def assert_login_success_response(response):
    assert response.status_code == 200
    assert response.headers.get("Content-Type", "").startswith("application/json")
    response_json = response.json()
    assert set(response_json.keys()) == {"id"}
    assert isinstance(response_json["id"], int)


def assert_create_order_success_response(response):
    assert response.status_code == 201
    assert response.headers.get("Content-Type", "").startswith("application/json")
    response_json = response.json()
    assert set(response_json.keys()) == {"track"}
    assert isinstance(response_json["track"], int)
