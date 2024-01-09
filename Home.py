import streamlit as st
from frontend.components import (
    data_exploration_component,
    sidebar_filter_component,
    jobs_data_component,
    data_visualization_component,
    update_date_info_component,
)
from frontend.frontend_config import DATA_LABELS, PAGE_TITLE, PAGE_ICON_PATH, LAYOUT


def home_page():
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON_PATH,
        layout=LAYOUT,
    )
    update_date_info_component()
    component = st.sidebar.radio(
        "Select data type", list(DATA_LABELS.values()), label_visibility="hidden"
    )
    if component == DATA_LABELS["data_exploration"]:
        data_exploration_component()
    elif component == DATA_LABELS["jobs_data"]:
        filter_data = sidebar_filter_component()
        jobs_data_component(filter_data)
    elif component == DATA_LABELS["data_visualization"]:
        data_visualization_component()


if __name__ == "__main__":
    home_page()
