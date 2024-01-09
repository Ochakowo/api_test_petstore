import pytest
from utils.methods import ApiReqres


@pytest.fixture(scope="class")
def methods(request):
    base_url = ApiReqres(request.cls.base_url)
    yield base_url

