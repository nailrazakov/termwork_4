from src.api_classes import Saver
import pytest


@pytest.fixture
def saver_test():
    return Saver("python", [{"id_vacancy": "123456",
                             "зарплата до": 50000},
                            {"id_vacancy": "123457",
                             "зарплата до": 100000},
                            {"id_vacancy": "123458",
                             "зарплата до": 150000},
                            ])
