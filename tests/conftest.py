import pytest

from app.main import reset_user_store


@pytest.fixture(autouse=True)
def clean_user_store():
    reset_user_store()
    yield
    reset_user_store()

