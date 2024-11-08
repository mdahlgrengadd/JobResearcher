import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from typing import Dict, List
import networkx as nx
import random
from utils.industry_map import INDUSTRY_MAPPING, load_company_data, get_industry_trends, extract_all_skills  # Added imports


def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    """Custom color function for wordcloud."""
    if word in company_skills_global:
        return "rgb(255, 215, 0)"  # Yellow for company skills
    return "rgb(128, 128, 128)"    # Grey for other skills


def get_all_industries(companies: List[Dict]) -> List[str]:
    """Extract all unique industry groups from the companies."""
    industry_groups = set()
    for company in companies:
        if 'company_info' in company and 'industries' in company['company_info']:
            for industry in company['company_info']['industries']:
                group = INDUSTRY_MAPPING.get(industry, "Other")
                industry_groups.add(group)
    return sorted(list(industry_groups))


def create_wordcloud(company_data: Dict, all_companies: List[Dict], excluded_industries: List[str] = None):
    """Create a wordcloud with company-specific skills in yellow and others in grey.

    Args:
        company_data: Data for the selected company
        all_companies: List of all company data
        excluded_industries: List of industries to exclude from the analysis

    Returns:
        WordCloud object or None if no skills are found
    """
    # Get selected company skills
    company_skills = set(company_data['company_info'].get('skills', []))

    # Get all industry groups
    all_industries = get_all_industries(all_companies)

    # Always set the global variable
    global company_skills_global
    company_skills_global = company_skills

    # Initialize word weights dictionary
    word_weights = {}

    if excluded_industries and set(excluded_industries) == set(all_industries):
        # If all industries are excluded, show only selected company's skills
        word_weights = {skill: 5 for skill in company_skills}

        # Create custom color function for this case
        def color_func_company_only(word, *args, **kwargs):
            """When showing only company skills, all words should be yellow"""
            return "rgb(255, 215, 0)"  # Yellow for all words

        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='black',
            color_func=color_func_company_only,
            prefer_horizontal=0.7
        ).generate_from_frequencies(word_weights)

    else:
        # Get skills from companies not in excluded industries
        relevant_skills = []
        for company in all_companies:
            if 'company_info' not in company:
                continue

            # Check if company is in excluded industries
            company_industries = [INDUSTRY_MAPPING.get(ind, "Other")
                                  for ind in company['company_info'].get('industries', [])]

            if excluded_industries and any(ind in excluded_industries for ind in company_industries):
                continue

            # Add skills from non-excluded company
            relevant_skills.extend(company['company_info'].get('skills', []))

        # Count skills
        skill_counts = Counter(relevant_skills)

        # Create weighted dictionary
        for skill, count in skill_counts.items():
            # Give higher weight to company-specific skills
            weight = count * 5 if skill in company_skills else count
            word_weights[skill] = weight

        if not word_weights:
            st.warning("No skills found after applying industry filters.")
            return None

        # Create wordcloud with standard color function
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='black',
            color_func=color_func,
            prefer_horizontal=0.7
        ).generate_from_frequencies(word_weights)

    return wordcloud


def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    """Custom color function for wordcloud."""
    if word in company_skills_global:
        return "rgb(255, 215, 0)"  # Yellow for company skills
    return "rgb(128, 128, 128)"    # Grey for other skills


def create_dashboard():
    st.title("Company Skills Analysis")

    # Load all company data
    companies = load_company_data()

    if not companies:
        st.error("No company data available. Please check the data directory.")
        return

    # Industry filter
    st.sidebar.header("Filters")
    all_industries = get_all_industries(companies)
    excluded_industries = st.sidebar.multiselect(
        "Exclude Industries from Analysis",
        options=all_industries,
        default=["Other"],
        help="Select industries to exclude from the skills analysis"
    )

    # Company selector
    company_names = [company['company_info']['name'] for company in companies]
    selected_company_name = st.sidebar.selectbox(
        "Select a Company", company_names)

    try:
        # Get selected company data
        selected_company = next(company for company in companies
                                if company['company_info']['name'] == selected_company_name)

        # Display company information
        st.sidebar.header("Company Overview")

        with st.sidebar:
            st.subheader("Basic Information")
            # st.write(f"**Name:** {selected_company['company_info']['name']}")
            st.write(
                f"**Location:** {', '.join(selected_company['company_info']['locations'])}")
            st.write(
                f"**Industries:** {', '.join(selected_company['company_info']['industries'])}")

            st.subheader("Job Titles")
            for title in selected_company['company_info']['job_titles']:
                st.write(f"- {title}")

        # Skills WordCloud
        if excluded_industries:
            st.caption(
                f"Excluding skills from companies in: {', '.join(excluded_industries)}")
        st.write("🟡 Company-specific skills | ⚫ Industry-wide skills")

        # Create and display wordcloud
        wordcloud = create_wordcloud(
            selected_company, companies, excluded_industries)
        if wordcloud:
            plt.figure(figsize=(10, 5), facecolor='k')
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(plt)

    except Exception as e:
        st.error(f"Error processing company data: {str(e)}")
        st.error("Please check the data format and try again.")


if __name__ == "__main__":
    st.set_page_config(page_title="Company Analysis Dashboard", layout="wide")
    create_dashboard()
