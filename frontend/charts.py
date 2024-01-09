import plotly.express as px
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
from frontend.frontend_utils import get_one_salary_min_max
from frontend.charts_config import (
    SALARY_DISTRIBUTION_CHART,
    COMPANY_DISTRIBUTION_CHART,
    COMPANY_WISE_SALAY_CHART,
    HARD_SKILLS_WORD_CLOUD,
    SOFT_SKILLS_WORD_CLOUD,
    MIN_EXPERIENCE_CHART,
    TECH_WORD_CLOUD,
    JOB_TITLE_WORD_CLOUD,
    JOB_DISTRIBUTION_BY_TECH_CHART,
)


def salary_distribution_chart(df):
    df = df.copy()
    df["salary_min"], df["salary_max"] = zip(
        *df.loc[:, "salary"].apply(get_one_salary_min_max)
    )
    df.loc[:, "mean_salary"] = (df["salary_min"] + df["salary_max"]) / 2
    df = df.sort_values(by=SALARY_DISTRIBUTION_CHART["sort_by"], ascending=True)
    fig = px.bar(
        df,
        x=SALARY_DISTRIBUTION_CHART["x-axis"],
        y=SALARY_DISTRIBUTION_CHART["y-axis"],
        orientation="h",
        labels=SALARY_DISTRIBUTION_CHART["labels"],
    )
    fig.update_layout(
        width=SALARY_DISTRIBUTION_CHART["width"],
        height=SALARY_DISTRIBUTION_CHART["height"],
    )
    fig.update_traces(
        texttemplate=SALARY_DISTRIBUTION_CHART["text_template"],
        textposition=SALARY_DISTRIBUTION_CHART["text_position"],
    )
    return fig


def company_distribution_chart(df):
    company_counts = df["company_name"].value_counts()
    fig = px.bar(
        company_counts,
        x=company_counts.index,
        y=company_counts.values,
        color=company_counts.index,
        labels=COMPANY_DISTRIBUTION_CHART["labels"],
    )
    fig.update_layout(
        xaxis_tickangle=COMPANY_DISTRIBUTION_CHART["tick_angle"],
        width=COMPANY_DISTRIBUTION_CHART["width"],
        height=COMPANY_DISTRIBUTION_CHART["height"],
    )
    return fig


def hard_skills_word_cloud(df):
    hard_skills_text = " ".join(
        [skill for skills_list in df["hard_skills"] for skill in skills_list]
    )
    wordcloud = WordCloud(
        width=HARD_SKILLS_WORD_CLOUD["width"],
        height=HARD_SKILLS_WORD_CLOUD["height"],
        background_color=HARD_SKILLS_WORD_CLOUD["background_color"],
    ).generate(hard_skills_text)
    plt.figure(figsize=HARD_SKILLS_WORD_CLOUD["fig_size"])
    plt.imshow(wordcloud, interpolation=HARD_SKILLS_WORD_CLOUD["interpolation"])
    plt.axis(HARD_SKILLS_WORD_CLOUD["axis"])
    return plt


def soft_skills_word_cloud(df):
    soft_skills_text = " ".join(
        [skill for skills_list in df["soft_skills"] for skill in skills_list]
    )
    wordcloud = WordCloud(
        width=SOFT_SKILLS_WORD_CLOUD["width"],
        height=SOFT_SKILLS_WORD_CLOUD["height"],
        background_color=SOFT_SKILLS_WORD_CLOUD["background_color"],
    ).generate(soft_skills_text)
    plt.figure(figsize=SOFT_SKILLS_WORD_CLOUD["fig_size"])
    plt.imshow(wordcloud, interpolation=SOFT_SKILLS_WORD_CLOUD["interpolation"])
    plt.axis(SOFT_SKILLS_WORD_CLOUD["axis"])
    return plt


def min_experience_chart(df):
    experience_counts = df["minimum_experience_year"].value_counts().sort_index()
    fig = px.bar(
        experience_counts,
        x=experience_counts.index,
        y=experience_counts.values,
        labels=MIN_EXPERIENCE_CHART["labels"],
    )
    fig.update_layout(
        width=MIN_EXPERIENCE_CHART["width"], height=MIN_EXPERIENCE_CHART["height"]
    )
    return fig


def tech_word_cloud(df):
    technologies_text = " ".join(
        [tech for tech_list in df["technologies"] for tech in tech_list]
    )
    wordcloud = WordCloud(
        width=TECH_WORD_CLOUD["width"],
        height=TECH_WORD_CLOUD["height"],
        background_color=TECH_WORD_CLOUD["background_color"],
    ).generate(technologies_text)
    plt.figure(figsize=TECH_WORD_CLOUD["fig_size"])
    plt.imshow(wordcloud, interpolation=TECH_WORD_CLOUD["interpolation"])
    plt.axis(TECH_WORD_CLOUD["axis"])
    return plt


def company_wise_salary_chart(df):
    df = df.copy()
    df["salary_min"], df["salary_max"] = zip(
        *df["salary"].apply(get_one_salary_min_max)
    )
    company_salary_comparison = df.groupby("company_name")[
        ["salary_min", "salary_max"]
    ].mean()
    fig = px.bar(
        company_salary_comparison,
        x=company_salary_comparison.index,
        y=["salary_min", "salary_max"],
        labels=COMPANY_WISE_SALAY_CHART["labels"],
    )
    fig.update_layout(
        barmode=COMPANY_WISE_SALAY_CHART["barmode"],
        width=COMPANY_WISE_SALAY_CHART["width"],
        height=COMPANY_WISE_SALAY_CHART["height"],
    )
    return fig


def job_title_word_cloud(df):
    job_title_text = " ".join(df["title"])
    wordcloud = WordCloud(
        width=JOB_TITLE_WORD_CLOUD["width"],
        height=JOB_TITLE_WORD_CLOUD["height"],
        background_color=JOB_TITLE_WORD_CLOUD["background_color"],
    ).generate(job_title_text)
    plt.figure(figsize=JOB_TITLE_WORD_CLOUD["fig_size"])
    plt.imshow(wordcloud, interpolation=JOB_TITLE_WORD_CLOUD["interpolation"])
    plt.axis(JOB_TITLE_WORD_CLOUD["axis"])
    return plt


def job_distribution_by_tech_chart(df):
    tech_counts = Counter(
        [tech.strip() for sublist in df["technologies"] for tech in sublist]
    )
    tech_counts_filtered = {
        tech: count for tech, count in tech_counts.items() if count > 1
    }
    tech_counts_df = pd.DataFrame(
        list(tech_counts_filtered.items()), columns=["Technology", "Number of Jobs"]
    )
    tech_counts_df = tech_counts_df.sort_values(
        by=JOB_DISTRIBUTION_BY_TECH_CHART["sort_by"], ascending=False
    )
    fig = px.bar(
        tech_counts_df,
        x=JOB_DISTRIBUTION_BY_TECH_CHART["x-axis"],
        y=JOB_DISTRIBUTION_BY_TECH_CHART["y-axis"],
        labels=JOB_DISTRIBUTION_BY_TECH_CHART["labels"],
    )
    fig.update_layout(
        width=JOB_DISTRIBUTION_BY_TECH_CHART["width"],
        height=JOB_DISTRIBUTION_BY_TECH_CHART["height"],
    )
    return fig
