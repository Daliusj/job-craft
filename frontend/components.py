import streamlit as st
import time
import pandas as pd
from jobcraft import get_data_df, get_data, get_base_url, get_tech_list
from frontend.frontend_utils import (
    get_salaries_min_max,
    get_filtered_dict,
    change_job_for_dev_value,
    get_update_date,
)
from frontend.charts import (
    salary_distribution_chart,
    company_distribution_chart,
    hard_skills_word_cloud,
    soft_skills_word_cloud,
    min_experience_chart,
    tech_word_cloud,
    company_wise_salary_chart,
    job_title_word_cloud,
    job_distribution_by_tech_chart,
)
from frontend.frontend_config import (
    JOB_DATA_COMPONENT_MESSAGES,
    JOBS_LISTING_COMPONENT_MESSAGES,
    MORE_DETAILS_COMPONENT_MESSAGES,
    NOT_DEV_JOB_COMPONENT_MESSAGE,
    NOT_DEV_JOB_COMPONENT_TIMING,
    DEV_JOB_COMPONENT_MESSAGE,
    DEV_JOB_COMPONENT_TIMING,
    SIDEBAR_FILTER_COMPONENT_MESSAGES,
    DATA_VISUALIZATION_COMPONENT_MESSAGES,
    DATA_VISUALIZATION_COMPONENT_CHARTS_NAMES,
    UPDATE_DATE_COMPONENT_MESSAGE,
)


def jobs_data_component(filter_data):
    data = get_data()
    data_filtered = get_filtered_dict(filter_data, data)
    if data_filtered:
        for index, job in enumerate(data_filtered):
            more_details, is_not_dev_job, is_dev_job = jobs_listing_component(
                index, job, filter_data["is_only_dev_jobs_checked"]
            )
            if more_details:
                more_details_component(job)
            if is_not_dev_job:
                change_job_for_dev_value(job)
                not_dev_job_component()
            if is_dev_job:
                change_job_for_dev_value(job)
                dev_job_component()
            st.divider()
    else:
        st.warning(JOB_DATA_COMPONENT_MESSAGES["empty_data"])


def data_exploration_component():
    data = get_data_df()
    st.sidebar.divider()
    st.dataframe(data)


def jobs_listing_component(index, job, is_only_dev_jobs_checked):
    if not job["job_for_programmer"]:
        st.info(JOBS_LISTING_COMPONENT_MESSAGES["not_dev_job"])
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        st.caption(JOBS_LISTING_COMPONENT_MESSAGES["title"])
        st.write(job["title"])

    with col2:
        st.caption(JOBS_LISTING_COMPONENT_MESSAGES["company"])
        st.write(job["company_name"])
    with col3:
        st.caption(JOBS_LISTING_COMPONENT_MESSAGES["salary"])
        st.write(job["salary"])
    with col4:
        st.caption(JOBS_LISTING_COMPONENT_MESSAGES["min_experience"])
        if job["minimum_experience_year"]:
            st.write(str(job["minimum_experience_year"]).split(".")[0])
        else:
            st.write(JOBS_LISTING_COMPONENT_MESSAGES["no_experience_data"])
    with col5:
        st.caption(JOBS_LISTING_COMPONENT_MESSAGES["location"])
        st.write(job["city"])
    with col6:
        st.caption(JOBS_LISTING_COMPONENT_MESSAGES["valid_till"])
        st.write(job["valid_till"])
    with col7:
        url = get_base_url() + job["url_endpoint"]
        st.link_button(JOBS_LISTING_COMPONENT_MESSAGES["button_source_page"], url=url)
        more_details = st.button(
            JOBS_LISTING_COMPONENT_MESSAGES["button_details"], key=f"{index}-link"
        )
        is_not_dev_job = st.button(
            JOBS_LISTING_COMPONENT_MESSAGES["button_not_dev_job"],
            key=f"{index}-not-dev",
        )
        if not is_only_dev_jobs_checked:
            is_dev_job = st.button(
                JOBS_LISTING_COMPONENT_MESSAGES["button_dev_job"], key=f"{index}-dev"
            )
            return more_details, is_not_dev_job, is_dev_job
        else:
            return more_details, is_not_dev_job, False


def more_details_component(job):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(MORE_DETAILS_COMPONENT_MESSAGES["hard_skills"])
        for skill in job["hard_skills"].split(","):
            st.write(f"- {skill}")
    with col2:
        st.caption(MORE_DETAILS_COMPONENT_MESSAGES["soft_skills"])
        for skill in job["soft_skills"].split(","):
            st.write(f"- {skill}")
    with col3:
        st.caption(MORE_DETAILS_COMPONENT_MESSAGES["technologies"])
        for skill in job["technologies"].split(","):
            st.write(f"- {skill}")


def not_dev_job_component():
    st.warning(NOT_DEV_JOB_COMPONENT_MESSAGE)
    time.sleep(NOT_DEV_JOB_COMPONENT_TIMING)
    st.rerun()


def dev_job_component():
    st.warning(DEV_JOB_COMPONENT_MESSAGE)
    time.sleep(DEV_JOB_COMPONENT_TIMING)
    st.rerun()


def sidebar_filter_component():
    st.sidebar.divider()
    is_expired_checked = st.sidebar.checkbox(
        SIDEBAR_FILTER_COMPONENT_MESSAGES["dont_show_expired"], value=True
    )
    is_only_dev_jobs_checked = st.sidebar.checkbox(
        SIDEBAR_FILTER_COMPONENT_MESSAGES["show_only_dev_jobs"], value=True
    )
    salary_min, salary_max = get_salaries_min_max()
    salary_range = st.sidebar.slider(
        SIDEBAR_FILTER_COMPONENT_MESSAGES["salary"], value=[salary_min, salary_max]
    )
    min_experience = st.sidebar.slider(
        SIDEBAR_FILTER_COMPONENT_MESSAGES["experience"], 0, 10
    )
    tech_stack = st.sidebar.multiselect(
        SIDEBAR_FILTER_COMPONENT_MESSAGES["tech"], get_tech_list()
    )
    return {
        "is_expired_checked": is_expired_checked,
        "salary_range": salary_range,
        "min_experience": min_experience,
        "tech_stack": tech_stack,
        "is_only_dev_jobs_checked": is_only_dev_jobs_checked,
    }


def data_visualization_component():
    raw_df = get_data_df()
    df = raw_df[raw_df["job_for_programmer"] == 1]
    df.loc[:, "hard_skills"] = df["hard_skills"].apply(
        lambda x: x.split(",") if pd.notna(x) else []
    )
    df.loc[:, "soft_skills"] = df["soft_skills"].apply(
        lambda x: x.split(",") if pd.notna(x) else []
    )
    df.loc[:, "technologies"] = df["technologies"].apply(
        lambda x: x.split(",") if pd.notna(x) else []
    )
    st.sidebar.divider()
    st.sidebar.header(DATA_VISUALIZATION_COMPONENT_MESSAGES["choose_chart"])
    chart_option = st.sidebar.radio(
        "Select Chart",
        list(DATA_VISUALIZATION_COMPONENT_CHARTS_NAMES.values()),
        label_visibility="hidden",
    )
    if chart_option == DATA_VISUALIZATION_COMPONENT_CHARTS_NAMES["salary_distribution"]:
        st.header(DATA_VISUALIZATION_COMPONENT_CHARTS_NAMES["salary_distribution"])
        st.plotly_chart(salary_distribution_chart(df))
    elif (
        chart_option
        == DATA_VISUALIZATION_COMPONENT_CHARTS_NAMES["company_distribution"]
    ):
        st.header(DATA_VISUALIZATION_COMPONENT_CHARTS_NAMES["company_distribution"])
        st.plotly_chart(company_distribution_chart(df))
    elif chart_option == DATA_VISUALIZATION_COMPONENT_CHARTS_NAMES["hard_skills_cloud"]:
        st.header(DATA_VISUALIZATION_COMPONENT_CHARTS_NAMES["hard_skills_cloud"])
        st.pyplot(hard_skills_word_cloud(df))
    elif chart_option == DATA_VISUALIZATION_COMPONENT_CHARTS_NAMES["soft_skills_cloud"]:
        st.header(DATA_VISUALIZATION_COMPONENT_CHARTS_NAMES["soft_skills_cloud"])
        st.pyplot(soft_skills_word_cloud(df))
    elif chart_option == DATA_VISUALIZATION_COMPONENT_CHARTS_NAMES["min_experience"]:
        st.header(DATA_VISUALIZATION_COMPONENT_CHARTS_NAMES["min_experience"])
        st.plotly_chart(min_experience_chart(df))
    elif chart_option == DATA_VISUALIZATION_COMPONENT_CHARTS_NAMES["tech_cloud"]:
        st.header(DATA_VISUALIZATION_COMPONENT_CHARTS_NAMES["tech_cloud"])
        st.pyplot(tech_word_cloud(df))
    elif chart_option == DATA_VISUALIZATION_COMPONENT_CHARTS_NAMES["company_salary"]:
        st.header(DATA_VISUALIZATION_COMPONENT_CHARTS_NAMES["company_salary"])
        st.plotly_chart(company_wise_salary_chart(df))
    elif chart_option == DATA_VISUALIZATION_COMPONENT_CHARTS_NAMES["job_title_cloud"]:
        st.header(DATA_VISUALIZATION_COMPONENT_CHARTS_NAMES["job_title_cloud"])
        st.pyplot(job_title_word_cloud(df))
    elif chart_option == DATA_VISUALIZATION_COMPONENT_CHARTS_NAMES["tech_distribution"]:
        st.header(DATA_VISUALIZATION_COMPONENT_CHARTS_NAMES["tech_distribution"])
        st.plotly_chart(job_distribution_by_tech_chart(df))


def update_date_info_component():
    update_date = get_update_date()
    if update_date:
        st.sidebar.info(f"{UPDATE_DATE_COMPONENT_MESSAGE} {get_update_date()}")
