from faker import Faker


faker = Faker("ru_RU")


COURIER_CREDENTIAL_LENGTH = 10

ORDER_BASE_PAYLOAD = {
    "firstName": "Иван",
    "lastName": "Петров",
    "address": "Тверская, 12, кв. 34",
    "metroStation": 4,
    "phone": "+79991234567",
    "rentTime": 5,
    "comment": "Позвоните за 10 минут до доставки",
}

ORDER_COLOR_VARIANTS = [
    ["BLACK"],
    ["GREY"],
    ["BLACK", "GREY"],
    [],
]
