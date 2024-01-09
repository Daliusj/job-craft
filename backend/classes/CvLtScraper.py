from bs4 import BeautifulSoup
from datetime import datetime

# config
CVLT_BASE_URL = "https://www.cv.lt"
CVLT_SEARCH_ENDPOINT = "/nuolatinis-darbas"
CVLT_PAGE_ENDPOINT = "?page="
CVLT_KEYWORD_ENDPOINT = "&texts="
CVLT_SORT_ENDPOINT = "&sortField=ORDER_TIME"
SCRAPE_TIMING = 20
UPDATES_LOG_PATH = "logs/updates_log.log"
CVLTSCRAPER_MESSAGES = {
    "error": "CvLtScraper: ",
    "full_update_log": "Full Update",
    "update_log": "Update",
    "update_start": "CvLtScraper: STARTING NEW ENTRIES UPDATE SCRAPING",
    "update_finish": "CvLtScraper: FINISHED NEW ENTRIES UPDATE SCRAPING",
    "full_start": "CvLtScraper: STARTING FULL UPDATE SCRAPING",
    "full_finish": "CvLtScraper: FINISHED FULL UPDATE SCRAPING",
}


class CvLtScraper:
    """
    This module is designed for web scraping job listings from the CV.lt website.
    It provides functionality to update and retrieve job data based on specified search keywords.
    The extracted data includes essential details such as job titles, salaries, company names, and city locations.
    The script is configurable through parameters and includes logging capabilities to track updates and potential errors during execution.
    """

    def __init__(
        self,
        scraper,
        keywords,
        logger,
        data,
        parser,
    ) -> None:
        self.parser = parser
        self.logger = logger
        self.data = data
        self.scraper = scraper
        self.scraper.timing = SCRAPE_TIMING
        self.keywords = keywords
        self.soups_lst = []

    def get_soups_list(self, urls_list):
        self.scraper.urls_list = urls_list
        self.scraper.scrape()
        return self.scraper.soups_list

    def get_full_update(self):
        self.logger.log(CVLTSCRAPER_MESSAGES["full_start"], "INFO")
        self.soups_lst = self.get_soups_lst_by_keywords()
        jobs = self.get_jobs_from_soups_lst()
        self.data.update(jobs)
        jobs_data = self.get_jobs_details()
        self.data.update(jobs_data)
        self.update_log(CVLTSCRAPER_MESSAGES["full_update_log"])
        self.logger.log(CVLTSCRAPER_MESSAGES["full_finish"], "INFO")

    def get_update(self):
        self.logger.log(CVLTSCRAPER_MESSAGES["update_start"], "INFO")
        self.soups_lst = self.get_soups_lst_by_keywords()
        jobs = self.get_jobs_from_soups_lst()
        jobs_data = self.data.get()
        jobs_data += jobs
        self.data.update(jobs_data)
        jobs_data = self.get_jobs_details()
        self.data.update(jobs_data)
        self.update_log(CVLTSCRAPER_MESSAGES["update_log"])
        self.logger.log(CVLTSCRAPER_MESSAGES["update_finish"], "INFO")

    def get_jobs_details(self):
        jobs_data = self.data.get()
        for job in jobs_data:
            if not job["valid_till"]:
                try:
                    url = CVLT_BASE_URL + job["url_endpoint"]
                    soup = self.get_soups_list([url])[0]
                    raw_text = soup.find("div", {"class": "job"}).text.strip()
                    text = self.remove_empty_lines(raw_text)
                    parsed_data = self.parser.parse(text)
                    if parsed_data:
                        job["hard_skills"] = ",".join(
                            [
                                skill.replace(",", "")
                                for skill in parsed_data["hard_skills"]
                            ]
                        )
                        job["soft_skills"] = ",".join(
                            [
                                skill.replace(",", "")
                                for skill in parsed_data["soft_skills"]
                            ]
                        )
                        job["minimum_experience_year"] = parsed_data[
                            "minimum_experience_year"
                        ]
                        job["job_for_programmer"] = parsed_data["job_for_programmer"]
                        job["technologies"] = ", ".join(
                            [
                                skill.replace(",", "")
                                for skill in parsed_data["technologies"]
                            ]
                        )
                    details_div = soup.find("div", {"class": "company-details"})
                    valid_till_component = details_div.find_all(
                        "div", {"details-item"}
                    )[-1]
                    job["valid_till"] = valid_till_component.find("p").text.strip()
                except Exception as e:
                    self.logger.log(
                        f"{CVLTSCRAPER_MESSAGES['error']}.get_jobs_details: {e}",
                        "ERROR",
                    )
        return jobs_data

    def get_soups_lst_by_keywords(self):
        soups_lst = []
        for keyword in self.keywords:
            first_page_url = [self.get_url(keyword=keyword)]
            initial_soup = self.get_soups_list(first_page_url)[0]
            total_pages_number = self.get_total_pages_number(initial_soup)
            urls_list = self.get_urls_list(keyword, total_pages_number)
            soups_lst += self.get_soups_list(urls_list)
        return soups_lst

    def remove_empty_lines(self, text):
        lines = text.split("\n")
        lines_list = filter(lambda line: line.strip() != "", lines)
        return "\n".join(lines_list)

    def get_total_pages_number(self, soup):
        pages_number_div = soup.find("div", {"class": "col col-12 text-center mt-4"})
        pages_number = pages_number_div.find_all("span", {"class": "ng-binding"})
        return int(pages_number[-1].text.strip())

    def get_jobs_from_soups_lst(self):
        jobs = []
        for soup in self.soups_lst:
            try:
                for element in soup.find_all("a", {"class": "job-wr"}):
                    job_title = element.find("button", {"class": "title"})
                    salary = element.find("span", {"class": "salary"})
                    url_endpoint = element.get("href")
                    company_span = element.find("span", {"class": "company"})
                    company_name = company_span.find("button")
                    city = company_span.find("span")
                    job_data = {
                        "title": job_title.text,
                        "salary": salary.text.replace(" €", ""),
                        "url_endpoint": url_endpoint,
                        "company_name": company_name.text,
                        "city": city.text,
                    }
                    jobs.append(job_data)
            except Exception as e:
                self.logger.log(
                    f"{CVLTSCRAPER_MESSAGES['error']}.get_jobs_from_soups_lst: {e}",
                    "ERROR",
                )
        return jobs

    def get_urls_list(self, keyword, total_pages_number):
        return [
            self.get_url(keyword=keyword, page_number=str(i + 1))
            for i in range(total_pages_number)
        ]

    def get_url(self, keyword: str, page_number: str = "1") -> str:
        return (
            CVLT_BASE_URL
            + CVLT_SEARCH_ENDPOINT
            + CVLT_PAGE_ENDPOINT
            + page_number
            + CVLT_KEYWORD_ENDPOINT
            + keyword
            + CVLT_SORT_ENDPOINT
        )

    def update_log(self, message):
        now = datetime.today().strftime("%Y-%m-%d")
        with open(UPDATES_LOG_PATH, "a") as file:
            file.write(f"{now} {message}\n")
