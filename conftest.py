import pytest
from init_db import main as init_db


@pytest.fixture(scope="session", autouse=True)
def reset_test_db(request):
    init_db("test")
