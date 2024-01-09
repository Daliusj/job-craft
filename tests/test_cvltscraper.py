import pytest
from bs4 import BeautifulSoup
from backend.utils.CvLtScraper import CvLtScraper


@pytest.fixture
def mock_scraper(mocker):
    return mocker.MagicMock()


@pytest.fixture
def mock_logger(mocker):
    return mocker.MagicMock()


@pytest.fixture
def mock_data(mocker):
    return mocker.MagicMock()


@pytest.fixture
def mock_parser(mocker):
    return mocker.MagicMock()


@pytest.fixture
def scraper_instance(mock_scraper, mock_logger, mock_data, mock_parser):
    return CvLtScraper(
        scraper=mock_scraper,
        keywords=["developer"],
        logger=mock_logger,
        data=mock_data,
        parser=mock_parser,
    )


def test_remove_empty_lines(scraper_instance):
    input_text = "Line 1\n\nLine 2\n \nLine 3"
    result = scraper_instance.remove_empty_lines(input_text)
    assert result == "Line 1\nLine 2\nLine 3"


def test_get_total_pages_number(scraper_instance, mocker):
    mock_soup = BeautifulSoup(
        "<div class='col col-12 text-center mt-4'><span class='ng-binding'>1</span><span class='ng-binding'>2</span></div>",
        "html.parser",
    )
    result = scraper_instance.get_total_pages_number(mock_soup)
    assert result == 2


def test_get_jobs_from_soups_lst(scraper_instance, mocker):
    mock_soup = BeautifulSoup(
        "<a class='job-wr'><button class='title'>Job Title</button><span class='salary'>1000 €</span><span class='company'><button>Company Name</button><span>City</span></span></a>",
        "html.parser",
    )
    scraper_instance.soups_lst = [mock_soup]

    result = scraper_instance.get_jobs_from_soups_lst()

    assert len(result) == 1
    assert result[0]["title"] == "Job Title"
    assert result[0]["salary"] == "1000"


def test_get_urls_list(scraper_instance):
    result = scraper_instance.get_urls_list("developer", 3)
    expected = [
        "https://www.cv.lt/nuolatinis-darbas?page=1&texts=developer&sortField=ORDER_TIME",
        "https://www.cv.lt/nuolatinis-darbas?page=2&texts=developer&sortField=ORDER_TIME",
        "https://www.cv.lt/nuolatinis-darbas?page=3&texts=developer&sortField=ORDER_TIME",
    ]
    assert result == expected


def test_get_url(scraper_instance):
    result = scraper_instance.get_url("python", "2")
    expected = (
        "https://www.cv.lt/nuolatinis-darbas?page=2&texts=python&sortField=ORDER_TIME"
    )
    assert result == expected
