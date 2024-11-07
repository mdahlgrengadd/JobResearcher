import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from collections import Counter
import os
from pathlib import Path

# Set page config
st.set_page_config(page_title="AI/ML Jobs Market Analysis", layout="wide")

# Function to load company reports from business_info folder


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

# Function to display company analysis


def display_company_analysis(company_data):
    if not company_data:
        st.write("No company data available.")
        return

    # Company Information
    if 'company_info' in company_data:
        info = company_data['company_info']
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Company Details")
            st.write(f"**Name:** {info.get('name', 'N/A')}")
            st.write("**Description:**")
            for desc in info.get('descriptions', []):
                st.write(f"- {desc}")

        with col2:
            st.subheader("Industries")
            for ind in info.get('industries', []):
                st.write(f"- {ind}")

        with col3:
            st.subheader("Locations")
            for loc in info.get('locations', []):
                st.write(f"- {loc}")

        # Skills word cloud or list
        if 'skills' in info:
            st.subheader("Key Skills")
            skills_df = pd.DataFrame(info['skills'], columns=['Skill'])
            fig = px.bar(skills_df['Skill'].value_counts(),
                         title="Required Skills",
                         labels={'value': 'Count', 'index': 'Skill'})
            st.plotly_chart(fig, use_container_width=True)

    # Analysis text
    if 'analysis' in company_data:
        st.subheader("Detailed Analysis")
        st.write(company_data['analysis'])

    # Search Results
    if 'search_results' in company_data:
        st.subheader("Recent Company Updates")
        for result in company_data['search_results']:
            with st.expander(result.get('title', 'No Title')):
                st.write(f"**Source:** {result.get('url', 'N/A')}")
                st.write(
                    f"**Description:** {result.get('description', 'No description available')}")


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

    # Header
    st.title("AI and Machine Learning Jobs Market Analysis - Sweden")
    st.write("Based on data from job listings and company reports")

    # Tabs for different sections
    tab1, tab2 = st.tabs(["Job Market Analysis", "Company Reports"])

    with tab1:
        # Key Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Jobs Found", jobs_data['Total Jobs Found'])
        with col2:
            avg_exp = jobs_df['Years of Experience'].mean()
            st.metric("Average Years of Experience Required",
                      f"{avg_exp:.1f} years")
        with col3:
            locations = jobs_df['Location'].value_counts()
            if not locations.empty:
                st.metric("Most Popular Location",
                          f"{locations.index[0]} ({locations.values[0]} jobs)")

        # Job Roles Distribution
        st.header("Job Roles Distribution")
        role_counts = jobs_df['Jobtitle'].value_counts().head(10)
        fig_roles = px.bar(
            x=role_counts.values,
            y=role_counts.index,
            orientation='h',
            title='Top 10 Job Titles',
            labels={'x': 'Number of Positions', 'y': 'Job Title'}
        )
        st.plotly_chart(fig_roles, use_container_width=True)

        # Skills Analysis
        st.header("Skills in Demand")
        all_skills = [skill for skills in jobs_df['Skills']
                      for skill in skills if isinstance(skills, list)]
        skill_counts = pd.Series(Counter(all_skills)).sort_values(
            ascending=True).tail(15)

        fig_skills = px.bar(
            x=skill_counts.values,
            y=skill_counts.index,
            orientation='h',
            title='Most In-Demand Skills',
            labels={'x': 'Number of Mentions', 'y': 'Skill'}
        )
        st.plotly_chart(fig_skills, use_container_width=True)

        # Experience Requirements
        st.header("Experience Requirements Analysis")
        col1, col2 = st.columns(2)

        with col1:
            exp_bins = [0, 2, 5, 8, 100]
            exp_labels = [
                'Entry Level (0-2)', 'Mid Level (3-5)', 'Senior (6-8)', 'Expert (8+)']
            jobs_df['Experience_Level'] = pd.cut(jobs_df['Years of Experience'],
                                                 bins=exp_bins,
                                                 labels=exp_labels,
                                                 right=False)
            exp_dist = jobs_df['Experience_Level'].value_counts()

            fig_exp = px.pie(
                values=exp_dist.values,
                names=exp_dist.index,
                title='Distribution of Experience Requirements'
            )
            st.plotly_chart(fig_exp)

        with col2:
            size_dist = jobs_df['Company Size'].value_counts()
            fig_size = px.pie(
                values=size_dist.values,
                names=size_dist.index,
                title='Distribution of Company Sizes'
            )
            st.plotly_chart(fig_size)

    with tab2:
        # Company Reports Section
        st.header("Company Analysis Reports")

        if not company_reports:
            st.warning(
                "No company reports available. Please add JSON files to the business_info directory.")
        else:
            # Company selector
            selected_company = st.selectbox(
                "Select a company to analyze:",
                options=list(company_reports.keys()),
                format_func=lambda x: x.replace('_', ' ').title()
            )

            # Display selected company analysis
            if selected_company:
                display_company_analysis(company_reports[selected_company])


if __name__ == "__main__":
    main()
