import pytest
import allure
from utils.enums import Status
from models.models import Pet


class Test_API:
    base_url = "https://petstore.swagger.io/v2/"
    api_pet = "pet/"
    valid_test_data = {
        "id": 50,
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "doggie",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": "available"
    }

    @allure.epic("Test Petstore")
    @allure.feature("Everything about your Pets")
    @allure.story("Создание питомца")
    @allure.title("Add a new pet to the store")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag('post', 'pet')
    @allure.description_html("- полноценный объект, статус available 200<br>"
                             "- пустой словарь 405<br>"
                             "- пустое тело запроса 415")
    @pytest.mark.parametrize("data", [valid_test_data, {}, None],
                             ids=["200", "405", "415"])
    def test_create_new_pet(self, methods, data):
        result = methods.post(self.api_pet, data)
        if data == self.valid_test_data:
            with allure.step(f"Test with full request body, status {result.status_code}"):
                assert result.status_code == 200, "Incorrect HTTP status code"
                assert methods.validate(result.json(), Pet)
        elif data is {}:
            with allure.step(f"Empty dictionary test, status {result.status_code}"):
                assert result.status_code == 405, "Incorrect HTTP status code"
        else:
            with allure.step(f"Test with empty request body, status {result.status_code}"):
                assert result.status_code == 415, "Incorrect HTTP status code"

    @allure.epic("Test Petstore")
    @allure.feature("Everything about your Pets")
    @allure.story("Изменение информации о питомце")
    @allure.title("Updates a pet in the store with form data")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag('pet', 'post')
    @allure.description_html("- поменять статус на sold 200<br>"
                             "- поменять статус на lost 405<br>"
                             "- попробовать изменить несуществующий объект 404<br>"
                             "- попробовать изменить объект с некорректным id 400")
    @pytest.mark.parametrize("id, name, status, http_status", [("50", "doggie", "sold", 200),
                                                               ("50", "doggie", "lost", 405),
                                                               ("50", "bulka", "sold", 404),
                                                               ("abc", "doggie", "sold", 400)],
                             ids=["sold200", "lost405", "bulka404", "id=abc"])
    def test_update_pet(self, methods, id, name, status, http_status):
        result = methods.put(self.api_pet, {"id": id, "name": name, "status": status})
        if status not in Status:
            with allure.step(f"Test with status {status}, different from our statuses. HTTP status {result.status_code}"):
                assert result.status_code == 405, "Incorrect HTTP status code"
        else:

            with allure.step(f"Check status {result.status_code}"):
                assert result.status_code == http_status, "Incorrect HTTP status code"
            obj = result.json()
            with allure.step("Validation of response data"):
                assert methods.validate(obj, Pet)

    @allure.epic("Test Petstore")
    @allure.feature("Everything about your Pets")
    @allure.story("Поиск питомца по статусу")
    @allure.title("Finds Pets by status {data}")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag('get', 'pet')
    @allure.description_html("- найти свое животное в статусе sold 200<br>"
                             "- поискать животное в статусе lost 400")
    @pytest.mark.parametrize("data", ["sold", "lost"])
    def test_find_pet_by_status(self, methods, data):
        result = methods.get(self.api_pet + "findByStatus", {"status": {data}})
        if data in Status:
            with allure.step(f"Test in {data} status, HTTP status {result.status_code}"):
                assert result.status_code == 200, "Incorrect HTTP status code"
                assert methods.validate(result.json()[0], Pet)
        else:
            with allure.step(f"Test with status {data}, different from our statuses. HTTP status {result.status_code}"):
                assert result.status_code == 400, "Incorrect HTTP status code"

    @allure.epic("Test Petstore")
    @allure.feature("Everything about your Pets")
    @allure.story("Удаление питомца")
    @allure.title("Deletes a pet with id {data}")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag('delete', 'pet')
    @allure.description_html("- удалить своё животное 200<br>"
                             "- удалить ещё раз 404<br>"
                             "- удалить с некорректным id 400")
    @pytest.mark.parametrize("data, http_status", [("50", 200),
                                                   ("50", 404),
                                                   ("abc", 400)],
                             ids=["del200", "del_again404", "del_incorrect_id400"])
    def test_delete_pet_by_id(self, methods, data, http_status):
        result = methods.delete(self.api_pet + data)
        with allure.step(f"Test with id {data}, status {result.status_code}"):
            assert result.status_code == http_status, "Incorrect HTTP status code"
