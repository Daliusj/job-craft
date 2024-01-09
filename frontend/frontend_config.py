# Home.py configs
DATA_LABELS = {
    "jobs_data": "Jobs data",
    "data_exploration": "Data Exploration",
    "data_visualization": "Data Visualization",
}
PAGE_TITLE = "JobCraft Insights"
PAGE_ICON_PATH = "frontend/images/job-offer.png"
LAYOUT = "wide"

# components.py configs
JOB_DATA_COMPONENT_MESSAGES = {"empty_data": "Nothing found"}
JOBS_LISTING_COMPONENT_MESSAGES = {
    "not_dev_job": "Marked as not a Developer Job",
    "title": "Title",
    "company": "Company",
    "salary": "Salary",
    "min_experience": "Minimum Experience (year)",
    "no_experience_data": "\-",
    "location": "Location",
    "valid_till": "Valid till",
    "button_source_page": "Source page",
    "button_details": "More details",
    "button_not_dev_job": "Not Dev Job",
    "button_dev_job": "Dev Job",
}
MORE_DETAILS_COMPONENT_MESSAGES = {
    "hard_skills": "Hard skills",
    "soft_skills": "Soft skills",
    "technologies": "Technologies",
}
NOT_DEV_JOB_COMPONENT_MESSAGE = "The job has been marked as Not a Developer Job and will not be shown in Data Visualization"
NOT_DEV_JOB_COMPONENT_TIMING = 3
DEV_JOB_COMPONENT_MESSAGE = (
    "The job has been marked as a Developer Job and will be shown in Data Visualization"
)
DEV_JOB_COMPONENT_TIMING = 3
SIDEBAR_FILTER_COMPONENT_MESSAGES = {
    "dont_show_expired": "Do not show expired",
    "show_only_dev_jobs": "Show only developer jobs",
    "salary": "Salary",
    "experience": "Experience years",
    "tech": "Technologies",
}
DATA_VISUALIZATION_COMPONENT_MESSAGES = {"choose_chart": "Choose Chart"}
DATA_VISUALIZATION_COMPONENT_CHARTS_NAMES = {
    "salary_distribution": "Salary Distribution",
    "company_distribution": "Company Distribution",
    "hard_skills_cloud": "Hard Skills Word Cloud",
    "soft_skills_cloud": "Soft Skills Word Cloud",
    "min_experience": "Minimum Experience Required",
    "tech_cloud": "Technologies Word Cloud",
    "company_salary": "Company-wise Salary Comparison",
    "job_title_cloud": "Job Title Word Cloud",
    "tech_distribution": "Job Distribution by Technology",
}

UPDATE_DATE_COMPONENT_MESSAGE = "Last data update"

# 1_About.py configs
ABOUT_PAGE_TEXT_TITLE = "About JobCraft Insights"
ABOUT_PAGE_TEXT_WELCOME_MARKDOWN = """
Welcome to **JobCraft Insights**, a platform designed for developers and software engineers to explore the dynamic job market. Dive into detailed insights and trends in the tech employment landscape using our user-friendly tools.
"""
ABOUT_PAGE_TEXT_WHAT_IS_HEADER = "What is JobCraft Insights?"
ABOUT_PAGE_TEXT_WHAT_IS_MARKDOWN = """
**JobCraft Insights** is exclusively designed for developers and software engineers. It helps you discover career opportunities and stay updated on the latest trends in tech jobs through its streamlined features.
"""
ABOUT_PAGE_TEXT_FEATURES_HEADER = "Key Features"
ABOUT_PAGE_TEXT_FEATURES_MARKDOWN = """
- **Tech-Focused Exploration:** Explore developer job listings with details like titles, salaries, and required technologies.
- **Developer-Centric Filtering:** Customize your search with filters like technology preferences, minimum experience, and relevant job types.
- **Real-Time Data:** Our data is collected using web scraping, ensuring accurate and up-to-date information.
- **Visualize Tech Trends:** Gain insights through interactive visualizations, including salary distribution and company trends.
"""
ABOUT_PAGE_TEXT_USAGE_HEADER = "How to Use"
ABOUT_PAGE_TEXT_USAGE_MARKDOWN = """
1. **Select Data Type:** Choose "Jobs Data" to explore developer job listings, "Data Exploration" for details, or "Data Visualization" for insightful charts.
2. **Tailored Developer Filters:** Apply filters relevant to developers, such as technology preferences and minimum experience.
3. **Explore Listings:** Browse through detailed job listings, view additional details, and mark jobs based on your expertise.
4. **Visualize Developer Data:** Explore charts for insights into salary distribution, company trends, and the technology landscape.
"""
ABOUT_PAGE_TEXT_FEEDBACK_HEADER = "Feedback"
ABOUT_PAGE_TEXT_FEEDBACK_MARKDOWN = """
We value your feedback! If you have suggestions or encounter issues, please reach out. Your input helps us enhance JobCraft Insights to better serve developers and software engineers.
"""
ABOUT_PAGE_TEXT_THANKS_MARKDOWN = "Thank you for choosing JobCraft Insights!"
