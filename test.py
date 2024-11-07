import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import json

# Set page config
st.set_page_config(layout="wide", page_title="Tech Job Market Analysis")

# Load and prepare data


@st.cache_data
def load_data():
    # Load job results
    with open('job_results.json') as f:
        job_data = json.load(f)

    # Convert jobs to DataFrame
    df = pd.DataFrame(job_data['Jobs'])

    # Clean up and prepare data
    df['Skills'] = df['Skills'].fillna('').apply(
        lambda x: x if isinstance(x, list) else [])
    df['Years of Experience'] = pd.to_numeric(
        df['Years of Experience'], errors='coerce')

    return df


# Load data
df = load_data()

# Title and introduction
st.title("Tech Job Market Analysis - Python & AI Focus")
st.markdown("""
This dashboard analyzes the tech job market in Sweden, with a special focus on Python and AI-related positions.
It provides insights into company distributions, required skills, and market trends.
""")

# Create two columns for the first row
col1, col2 = st.columns(2)

with col1:
    st.subheader("Company Distribution by Industry")
    industry_counts = df['Company Industry'].value_counts().head(10)
    fig = px.bar(x=industry_counts.index, y=industry_counts.values,
                 labels={'x': 'Industry', 'y': 'Number of Jobs'},
                 title='Top 10 Industries')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Job Locations")
    location_counts = df['Location'].value_counts().head(10)
    fig = px.pie(values=location_counts.values, names=location_counts.index,
                 title='Job Distribution by Location')
    st.plotly_chart(fig, use_container_width=True)

# Skills Analysis
st.subheader("Most In-Demand Skills")
# Flatten skills list and count occurrences
all_skills = [skill for skills in df['Skills'] for skill in skills]
skill_counts = pd.Series(Counter(all_skills)).sort_values(ascending=False)

# Filter for Python and AI related skills
relevant_skills = ['Python', 'Machine Learning', 'AI', 'Deep Learning', 'TensorFlow',
                   'PyTorch', 'Data Science', 'NLP', 'Computer Vision', 'Neural Networks']
relevant_skill_counts = skill_counts[skill_counts.index.isin(relevant_skills)]

fig = px.bar(x=relevant_skill_counts.index, y=relevant_skill_counts.values,
             labels={'x': 'Skill', 'y': 'Frequency'},
             title='Python and AI Related Skills Demand')
st.plotly_chart(fig, use_container_width=True)

# Experience Requirements
st.subheader("Years of Experience Requirements")
experience_data = df['Years of Experience'].dropna()
fig = px.histogram(experience_data, nbins=10,
                   labels={'value': 'Years of Experience Required',
                           'count': 'Number of Jobs'},
                   title='Distribution of Required Years of Experience')
st.plotly_chart(fig, use_container_width=True)

# Company Analysis
st.subheader("Top Companies Hiring")
company_counts = df['Company'].value_counts().head(10)
fig = px.bar(x=company_counts.index, y=company_counts.values,
             labels={'x': 'Company', 'y': 'Number of Job Postings'},
             title='Top 10 Companies by Job Postings')
st.plotly_chart(fig, use_container_width=True)

# Language Requirements
st.subheader("Language Requirements")
all_languages = [lang for langs in df['Languages']
                 for lang in langs if isinstance(langs, list)]
language_counts = pd.Series(
    Counter(all_languages)).sort_values(ascending=False)
fig = px.pie(values=language_counts.values, names=language_counts.index,
             title='Required Languages Distribution')
st.plotly_chart(fig, use_container_width=True)

# Key Insights Section
st.subheader("Key Insights")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Job Listings", len(df))

with col2:
    avg_exp = df['Years of Experience'].mean()
    st.metric("Average Years of Experience Required", f"{avg_exp:.1f} years")

with col3:
    python_jobs = sum(df['Skills'].apply(lambda x: 'Python' in x))
    st.metric("Jobs Requiring Python", python_jobs)

# Add filters in the sidebar
st.sidebar.title("Filters")
selected_industry = st.sidebar.multiselect(
    "Select Industry",
    options=sorted(df['Company Industry'].unique())
)

selected_location = st.sidebar.multiselect(
    "Select Location",
    options=sorted(df['Location'].unique())
)

# Company Insights
st.subheader("Company Analysis")
st.markdown("""
#### Key Observations:
1. **Industry Leaders**: The market is dominated by IT Consulting firms and large tech companies
2. **Geographic Distribution**: Major tech hubs are Stockholm, Gothenburg, and Malmö
3. **Company Types**:
   - Large enterprises (Volvo, Ericsson, AstraZeneca)
   - IT Consulting firms (Techster Solutions, VIPAS AB)
   - Startups and Scale-ups (BrightBid, Klarna)
""")

# Download functionality
if st.button('Download Analysis as CSV'):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Click here to download",
        csv,
        "job_market_analysis.csv",
        "text/csv",
        key='download-csv'
    )
