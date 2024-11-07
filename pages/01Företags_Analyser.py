import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from collections import Counter
import os
from pathlib import Path


def display_company_analysis(company_data):
    if not company_data:
        st.write("No company data available.")
        return

    # Company Information
    if 'company_info' in company_data:
        info = company_data['company_info']
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Företagsinfo")
            st.write(f"**Namn:** {info.get('name', 'N/A')}")
            st.write("**Beskrivning:**")
            for desc in info.get('descriptions', []):
                st.write(f"- {desc}")

        with col2:
            st.subheader("Brancher")
            for ind in info.get('industries', []):
                st.write(f"- {ind}")

        with col3:
            st.subheader("Platser")
            for loc in info.get('locations', []):
                st.write(f"- {loc}")

    # Analysis text
    if 'analysis' in company_data:
        st.subheader("Sammanfattning av företaget")
        st.write(company_data['analysis'])

    # Search Results
    if 'search_results' in company_data:
        st.subheader("Länkar")
        for result in company_data['search_results']:
            with st.expander(result.get('title', 'No Title')):
                st.write(f"**Source:** {result.get('url', 'N/A')}")
                st.write(
                    f"**Description:** {result.get('description', 'No description available')}")


def load_company_reports():
    try:
        business_info_path = Path("business_info")
        if not business_info_path.exists():
            st.warning(
                "business_info directory not found. Please create it and add company report files.")
            return {}

        company_reports = {}
        for file_path in business_info_path.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    company_reports[file_path.stem] = data
            except Exception as e:
                st.warning(f"Error loading {file_path.name}: {str(e)}")
                continue

        return company_reports
    except Exception as e:
        st.error(f"Error accessing business_info directory: {str(e)}")
        return {}

# Load the jobs data


def load_jobs_data():
    try:
        with open('job_results.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Error: Could not find job_results.json file.")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error: Invalid JSON format in job_results.json. {str(e)}")
        return None
    except Exception as e:
        st.error(
            f"An unexpected error occurred while loading job data: {str(e)}")
        return None

# Create DataFrame from jobs data


def create_jobs_df(jobs_data):
    if jobs_data is None:
        return pd.DataFrame()

    try:
        jobs = pd.DataFrame(jobs_data['Jobs'])
        jobs['Skills_str'] = jobs['Skills'].apply(
            lambda x: ', '.join(x) if isinstance(x, list) else '')
        return jobs
    except Exception as e:
        st.error(f"Error creating DataFrame: {str(e)}")
        return pd.DataFrame()


def main():
    # Load data
    jobs_data = load_jobs_data()
    company_reports = load_company_reports()

    if jobs_data is None:
        st.error("Unable to proceed due to job data loading errors.")
        return

    jobs_df = create_jobs_df(jobs_data)

    if jobs_df.empty:
        st.error("No job data available to display.")
        return

    # Company Reports Section
    st.header("Företagsanalyser")

    if not company_reports:
        st.warning(
            "No company reports available. Please add JSON files to the business_info directory.")
    else:
        # Company selector
        selected_company = st.selectbox(
            "Välj ett företag ur listan:",
            options=list(company_reports.keys()),
            format_func=lambda x: x.replace('_', ' ').title()
        )

        # Display selected company analysis
        if selected_company:
            display_company_analysis(company_reports[selected_company])


main()
