from backend.classes.WebScraper import WebScrapper
from backend.classes.CvLtScraper import CvLtScraper, CVLT_BASE_URL, UPDATES_LOG_PATH
from backend.classes.Logger import Logger
from backend.classes.Data import Data
from backend.classes.GptParser import GptParser
import argparse

# config
SEARCH_KEYWORDS = ["developer", f"software%20engineer"]
DATA_PROFILE_NAME = "jobs"
ARGS_PARSER_MESSAGES = {
    "description": "JobCraft webscraping program",
    "update_help": "Start web scraping, updating only new positions.",
    "full_help": "Run full update, overwriting existing data.",
    "invalid_action": "Invalid action specified.",
}


def main():
    """
    To run the script, execute it from the command line. The only supported action is "update."
    Example: python script_name.py update
    Optional argument: --full or -f: Run a full update, overwriting existing data.
    The script logs updates and errors.
    """
    args = set_args_parser()
    cv = set_scraping_utils()
    if args.action == "update":
        if args.full:
            cv.get_full_update()
        else:
            cv.get_update()
    elif args.action is None:
        print(ARGS_PARSER_MESSAGES["invalid_action"])


def set_data_utils():
    logger = Logger()
    data = Data()
    data.set_logger(logger)
    data.profile = DATA_PROFILE_NAME
    return data


def set_scraping_utils():
    logger = Logger()
    data = Data()
    data.set_logger(logger)
    data.profile = DATA_PROFILE_NAME
    parser = GptParser(logger)
    scraper = WebScrapper(logger)
    cv = CvLtScraper(scraper, SEARCH_KEYWORDS, logger, data, parser)
    return cv


def set_args_parser():
    parser = argparse.ArgumentParser(description=ARGS_PARSER_MESSAGES["description"])
    parser.add_argument(
        "action",
        choices=["update"],
        help=ARGS_PARSER_MESSAGES["update_help"],
    )
    parser.add_argument(
        "--full",
        "-f",
        action="store_true",
        help=ARGS_PARSER_MESSAGES["full_help"],
    )
    return parser.parse_args()


def get_data_df():
    # for frontend
    data = set_data_utils()
    return data.get_df()


def get_data():
    # for frontend
    data = set_data_utils()
    return data.get()


def get_base_url():
    # for frontend
    return CVLT_BASE_URL


def get_logs_path():
    # for frontend
    return UPDATES_LOG_PATH


def get_tech_list():
    # for frontend
    data = set_data_utils()
    return data.get_tech_list()


def data_row_update(row):
    # for frontend
    data = set_data_utils()
    data.row_update(row)


if __name__ == "__main__":
    main()
