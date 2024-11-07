import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import json

st.set_page_config(page_title="Tech Job Market Analysis", layout="wide")


def load_data():
    # Load job data
    with open('job_results.json', 'r', encoding='utf-8') as f:
        jobs_data = json.load(f)
    jobs_df = pd.DataFrame(jobs_data['Jobs'])

    # Clean and prepare the data
    jobs_df['Years_Experience'] = pd.to_numeric(
        jobs_df['Years of Experience'], errors='coerce')
    jobs_df['Skills_str'] = jobs_df['Skills'].apply(
        lambda x: ', '.join(x) if isinstance(x, list) else '')
    jobs_df['Has_Python'] = jobs_df['Skills'].apply(
        lambda x: 'Python' in x if isinstance(x, list) else False)
    jobs_df['Has_AI'] = jobs_df['Skills'].apply(lambda x: any(skill in x for skill in [
                                                'AI', 'Machine Learning', 'Deep Learning', 'Neural Networks', 'NLP']) if isinstance(x, list) else False)

    return jobs_df


def create_skill_distribution(df):
    # Flatten skills list and count occurrences
    all_skills = [skill for skills in df['Skills']
                  if isinstance(skills, list) for skill in skills]
    skill_counts = Counter(all_skills)

    # Create DataFrame for plotting
    skills_df = pd.DataFrame.from_dict(
        skill_counts, orient='index', columns=['Count']).reset_index()
    skills_df.columns = ['Skill', 'Count']
    skills_df = skills_df.sort_values('Count', ascending=True)

    # Create horizontal bar chart
    fig = px.bar(skills_df.tail(20), y='Skill', x='Count',
                 orientation='h', title='Most In-Demand Skills',
                 color='Count', color_continuous_scale='viridis')
    fig.update_layout(height=600)
    return fig


def create_location_distribution(df):
    # Handle null locations
    df_loc = df[df['Location'].notna()]
    location_counts = df_loc['Location'].value_counts().reset_index()
    location_counts.columns = ['Location', 'Count']

    fig = px.pie(location_counts, values='Count', names='Location',
                 title='Job Distribution by Location',
                 hole=0.4)
    return fig


def create_experience_distribution(df):
    # Create histogram of years of experience
    fig = px.histogram(df[df['Years_Experience'] > 0],
                       x='Years_Experience',
                       title='Distribution of Required Years of Experience',
                       nbins=20)
    fig.update_layout(
        xaxis_title="Years of Experience Required",
        yaxis_title="Number of Jobs"
    )
    return fig


def create_company_industry_analysis(df):
    industry_counts = df['Company Industry'].value_counts().reset_index()
    industry_counts.columns = ['Industry', 'Count']

    fig = px.bar(industry_counts.head(10), x='Industry', y='Count',
                 title='Top 10 Industries with Job Openings',
                 color='Count', color_continuous_scale='viridis')
    return fig


def main():
    st.title("Python and AI Job Market Analysis")

    # Load data
    df = load_data()

    # Summary statistics
    st.header("Market Overview")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Jobs", len(df))
    with col2:
        st.metric("Python Jobs", int(df['Has_Python'].sum()))
    with col3:
        st.metric("AI/ML Jobs", int(df['Has_AI'].sum()))

    # Skills Distribution
    st.header("Skills Analysis")
    st.plotly_chart(create_skill_distribution(df), use_container_width=True)

    # Location and Experience Analysis
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(create_location_distribution(df),
                        use_container_width=True)

    with col2:
        st.plotly_chart(create_experience_distribution(df),
                        use_container_width=True)

    # Industry Analysis
    st.header("Industry Analysis")
    st.plotly_chart(create_company_industry_analysis(df),
                    use_container_width=True)

    # Detailed Job Listings
    st.header("Job Listings")
    if st.checkbox("Show Python & AI Jobs Only"):
        filtered_df = df[df['Has_Python'] & df['Has_AI']]
    else:
        filtered_df = df

    for _, row in filtered_df.iterrows():
        with st.expander(f"{row['Jobtitle']} at {row['Company']}"):
            st.write(f"**Location:** {row['Location']}")
            st.write(
                f"**Required Experience:** {row['Years_Experience']} years")
            st.write(f"**Skills Required:** {row['Skills_str']}")
            st.write(f"**Job Description:** {row['Job Description']}")


if __name__ == "__main__":
    main()
