from datetime import datetime, timedelta
from frontend.frontend_utils import (
    get_one_salary_min_max,
    get_update_date,
    tech_filter,
    salary_filter,
    experience_filter,
    expired_filter,
)


def test_get_one_salary_min_max():
    result_1 = get_one_salary_min_max("1500 - 2500€")
    result_2 = get_one_salary_min_max("Nuo 5000€")
    assert result_1 == (1500, 2500)
    assert result_2 == (5000, 5000)


def test_get_update_date(mocker):
    mocker.patch(
        "builtins.open",
        mocker.mock_open(read_data="2024-01-01 Full Update\n2024-01-02 Update"),
    )
    result = get_update_date()
    assert result == "2024-01-02"


def test_tech_filter():
    mock_data = [
        {"technologies": ["Python", "Flask"]},
        {"technologies": ["Java", "Spring"]},
        {"technologies": ["JavaScript", "React"]},
    ]
    filter_data = {"tech_stack": ["Python", "React"]}
    result = tech_filter(mock_data, filter_data)
    assert result == [
        {"technologies": ["Python", "Flask"]},
        {"technologies": ["JavaScript", "React"]},
    ]


def test_experience_filter():
    mock_data = [
        {"minimum_experience_year": 2},
        {"minimum_experience_year": 3},
        {"minimum_experience_year": 1},
    ]
    filter_data = {"min_experience": 2}
    result = experience_filter(mock_data, filter_data)
    assert result == [
        {"minimum_experience_year": 2},
        {"minimum_experience_year": 3},
    ]


def test_expired_filter():
    mock_data = [
        {"valid_till": (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")},
        {"valid_till": (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")},
        {"valid_till": (datetime.today() + timedelta(days=2)).strftime("%Y-%m-%d")},
    ]
    filter_data = {"is_expired_checked": True}
    result = expired_filter(mock_data, filter_data)
    assert result == [
        {"valid_till": (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")},
        {"valid_till": (datetime.today() + timedelta(days=2)).strftime("%Y-%m-%d")},
    ]


def test_salary_filter():
    mock_data = [
        {"salary": "1000 - 1450€"},
        {"salary": "1500 - 2500€"},
        {"salary": "2600 - 3000€"},
    ]
    filter_data = {"salary_range": ["1500", "2500"]}
    result = salary_filter(mock_data, filter_data)
    assert result == [
        {"salary": "1500 - 2500€"},
    ]
