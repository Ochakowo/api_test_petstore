import requests
import allure


class ApiReqres:
    def __init__(self, base_url):
        self.base_url = base_url

    @allure.step("GET request to {path}")
    def get(self, path, params=None):
        params = {} if params is None else params
        return requests.get(self.base_url + path, params)

    @allure.step("POST request to {path}")
    def post(self, path, data=None):
        data = {} if data is None else data
        return requests.post(self.base_url + path, json=data)

    @allure.step("PUT request to {path}")
    def put(self, path, data=None):
        data = {} if data is None else data
        return requests.put(self.base_url + path, json=data)

    @allure.step("DELETE request to {path}")
    def delete(self, path):
        return requests.delete(self.base_url + path)

    @allure.step("Validate request result data")
    def validate(self, result, model):
        return model.model_validate(result)
