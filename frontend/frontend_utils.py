from datetime import datetime, timedelta
from jobcraft import get_data, data_row_update, get_logs_path


def get_salaries_min_max():
    data = get_data()
    salaries_lst = []
    for job in data:
        salaries_lst += get_salary_as_int_lst(job["salary"])
    if salaries_lst:
        return int(min(salaries_lst)), int(max(salaries_lst))
    else:
        return 0, 10000


def get_salary_as_int_lst(salary_str):
    salary_lst = salary_str.replace(".", "").split(" - ")
    return ["".join(filter(str.isnumeric, s)) for s in salary_lst]


def get_filtered_dict(filter_data, data):
    return [
        job
        for job in data
        if job in salary_filter(data, filter_data)
        and job in experience_filter(data, filter_data)
        and job in expired_filter(data, filter_data)
        and job in tech_filter(data, filter_data)
        and job in only_dev_jobs_filter(data, filter_data)
    ]


def only_dev_jobs_filter(data, filter_data):
    data_filtered = []
    if filter_data["is_only_dev_jobs_checked"]:
        for job in data:
            if job["job_for_programmer"]:
                data_filtered.append(job)
        return data_filtered
    else:
        return data


def tech_filter(data, filter_data):
    user_stack = filter_data["tech_stack"]
    data_filtered = []
    if user_stack:
        for job in data:
            tech_stack = job["technologies"]
            for tech in user_stack:
                if tech in tech_stack:
                    data_filtered.append(job)
        return data_filtered
    else:
        return data


def experience_filter(data, filter_data):
    data_filtered = []
    for job in data:
        experience = job["minimum_experience_year"]
        if experience:
            if int(experience) >= int(filter_data["min_experience"]):
                data_filtered.append(job)
        else:
            data_filtered.append(job)
    return data_filtered


def expired_filter(data, filter_data):
    now = datetime.today()
    data_filtered = []
    if filter_data["is_expired_checked"]:
        for job in data:
            valid_till = datetime.strptime(job["valid_till"], "%Y-%m-%d") + timedelta(
                days=1
            )
            if now < valid_till:
                data_filtered.append(job)
        return data_filtered
    else:
        return data


def salary_filter(data, filter_data):
    data_filtered = []
    for job in data:
        salary = get_salary_as_int_lst(job["salary"])
        if len(salary) == 2:
            if int(filter_data["salary_range"][0]) <= int(salary[0]) <= int(
                int(filter_data["salary_range"][1])
            ) or int(filter_data["salary_range"][0]) <= int(salary[1]) <= int(
                int(filter_data["salary_range"][1])
            ):
                data_filtered.append(job)
        if len(salary) == 1:
            if int(salary[0]) <= int(filter_data["salary_range"][1]):
                data_filtered.append(job)
    return data_filtered


def get_one_salary_min_max(salary):
    salaries_lst = []
    salaries_lst += get_salary_as_int_lst(salary)
    return int(min(salaries_lst)), int(max(salaries_lst))


def change_job_for_dev_value(job):
    if job["job_for_programmer"]:
        job["job_for_programmer"] = 0
    else:
        job["job_for_programmer"] = 1
    data_row_update(job)


def get_update_date():
    with open(get_logs_path(), "r") as file:
        updates = file.read()
    last_update = updates.strip().split("\n")[-1]
    return last_update.split(" ")[0]
