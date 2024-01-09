from dataclasses import dataclass
import os
import pandas as pd


# config
DATA_PATH = "backend/data/"
DATA_FILE_EXTENSION = ".csv"
JOBSDATA_MESSAGES = {
    "data_load_error": "JobsData.load_data: ",
    "data_load_warning": "JobsData.load_data: Can not load data. Profle is not set",
    "profile_set_error": "JobsData.profile.setter: Invalid profile name ",
    "profile_created": "JobsData.create_new_profile: New profile created ",
    "profile_create_error": "JobsData.create_new_profile: Profile not created. Invalid profile name.",
}
HEADER = "title,salary,url_endpoint,company_name,city,valid_till,hard_skills,soft_skills,minimum_experience_year,job_for_programmer,technologies\n"
TECH_STACK_DATA_PATH = "backend/data/technologies.txt"


@dataclass
class Data:
    """
    This module is for managing job-related data stored in CSV format. It supports functionalities such as loading, appending, overwriting, and updating data.
    The script also provides methods to retrieve the loaded data as either a list of dictionaries or a Pandas DataFrame.
    Additionally, it includes logging capabilities and checks for the availability of profile names.
    """

    profile = ""
    data = pd.DataFrame([])
    logger = None

    def set_logger(self, logger):
        self.logger = logger

    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self, profile):
        if self.is_profile_available(profile):
            self._profile = profile
        else:
            self.log(JOBSDATA_MESSAGES["profile_set_error"], "ERROR")

    def load(self):
        if not self.profile:
            self.log(JOBSDATA_MESSAGES["data_load_warning"], "WARNING")
        else:
            try:
                df = pd.read_csv(DATA_PATH + self.profile + DATA_FILE_EXTENSION)
                try:
                    self.data = df.drop(columns="Unnamed: 0")
                except:
                    self.data = df
            except FileNotFoundError as e:
                self.log(f"{JOBSDATA_MESSAGES['data_load_error']}{e}", "INFO")

    def append(self, data, keep="first"):
        df = pd.DataFrame(data)
        df.drop_duplicates(subset=["title"], keep=keep, inplace=True)
        df.to_csv(
            DATA_PATH + self.profile + DATA_FILE_EXTENSION,
            index=False,
            encoding="utf-8",
            mode="a",
            header=False,
        )
        self.load()

    def overwrite(self, data):
        with open(DATA_PATH + self.profile + DATA_FILE_EXTENSION, "w") as file:
            file.write(HEADER)
        data.to_csv(
            DATA_PATH + self.profile + DATA_FILE_EXTENSION,
            index=False,
            encoding="utf-8",
            mode="a",
            header=False,
        )
        self.load()

    def update(self, data, keep="first"):
        with open(DATA_PATH + self.profile + DATA_FILE_EXTENSION, "w") as file:
            file.write(HEADER)
        self.append(data, keep=keep)

    def row_update(self, row):
        data_dict = self.get()
        data_dict.append(row)
        self.update(data_dict, keep="last")

    def get(self):
        self.load()
        return (
            self.data.sort_values(by=["title"], ascending=True)
            .fillna("")
            .to_dict("records")
        )

    def get_df(self):
        self.load()
        return self.data

    def log(self, message, level):
        if self.logger:
            self.logger.log(message, level)
        else:
            print(level, message)

    def is_profile_available(self, profile):
        profiles_names = []
        for file_name in os.listdir(DATA_PATH):
            if file_name.endswith(".csv"):
                profiles_names.append(file_name.replace(".csv", ""))
        return profile in profiles_names

    def get_tech_list(self):
        with open(TECH_STACK_DATA_PATH, "r") as file:
            return list(set(file.read().split("\n")))
