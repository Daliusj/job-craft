SALARY_DISTRIBUTION_CHART = {
    "labels": {"mean_salary": "Mean Offer Salary (EUR)", "title": "Job Title"},
    "x-axis": "mean_salary",
    "y-axis": "title",
    "sort_by": "mean_salary",
    "text_position": "outside",
    "text_template": "%{x:.0f}",
    "width": 1400,
    "height": 1600,
}
COMPANY_DISTRIBUTION_CHART = {
    "labels": {"company_name": "Company", "y": "Number of Jobs"},
    "width": 1400,
    "height": 800,
    "tick_angle": -45,
}
HARD_SKILLS_WORD_CLOUD = {
    "width": 800,
    "height": 400,
    "background_color": "black",
    "interpolation": "bilinear",
    "fig_size": (10, 5),
    "axis": "off",
}
SOFT_SKILLS_WORD_CLOUD = {
    "width": 800,
    "height": 400,
    "background_color": "black",
    "interpolation": "bilinear",
    "fig_size": (10, 5),
    "axis": "off",
}
MIN_EXPERIENCE_CHART = {
    "labels": {"minimum_experience_year": "Experience (year)", "y": "Number of Jobs"},
    "width": 1400,
    "height": 800,
}
TECH_WORD_CLOUD = {
    "width": 800,
    "height": 400,
    "background_color": "black",
    "interpolation": "bilinear",
    "fig_size": (10, 5),
    "axis": "off",
}

COMPANY_WISE_SALAY_CHART = {
    "labels": {"company_name": "Company", "value": "Salary (€)"},
    "width": 1400,
    "height": 800,
    "barmode": "group",
}
JOB_TITLE_WORD_CLOUD = {
    "width": 800,
    "height": 400,
    "background_color": "black",
    "interpolation": "bilinear",
    "fig_size": (10, 5),
    "axis": "off",
}

JOB_DISTRIBUTION_BY_TECH_CHART = {
    "labels": {"x": "Technology", "y": "Number of Jobs"},
    "x-axis": "Technology",
    "y-axis": "Number of Jobs",
    "sort_by": "Number of Jobs",
    "width": 1400,
    "height": 800,
}
