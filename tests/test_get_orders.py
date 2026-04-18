import allure
from methods.order_methods import OrderMethods


class TestGetOrders:

    @allure.title("Получение списка заказов")
    def test_get_orders(self):
        response = OrderMethods.get_orders()
        response_json = response.json()

        assert response.status_code == 200
        assert "orders" in response_json
        assert isinstance(response_json["orders"], list)
