import os
import pytest
from region_service import create_app

@pytest.fixture
def app():
    app = create_app(True)
    return app
