import pytest
from src.api_classes import Saver


# Saver
def test_sorted_list(saver_test):
    assert saver_test.sorted_list() == [{'id_vacancy': '123458', 'зарплата до': 150000},
                                        {'id_vacancy': '123457', 'зарплата до': 100000},
                                        {'id_vacancy': '123456', 'зарплата до': 50000}]


def test_top_n(saver_test):
    assert saver_test.top_n(2) == [{"id_vacancy": "123458", "зарплата до": 150000},
                                   {"id_vacancy": "123457", "зарплата до": 100000}, ]


def test_delete_item(saver_test):
    saver_test.delete_item("123458")
    assert saver_test.list_of_vacancy == [{"id_vacancy": "123456",
                                           "зарплата до": 50000},
                                          {"id_vacancy": "123457",
                                           "зарплата до": 100000},
                                          ]
