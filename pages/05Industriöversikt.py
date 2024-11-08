import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict
import json
import re
from pathlib import Path
from utils.industry_map import INDUSTRY_MAPPING  # Updated import

# # Industry mapping dictionary
# INDUSTRY_MAPPING = {
#     # Technology & Software
#     'SaaS': 'Technology & Software',
#     'Software Development': 'Technology & Software',
#     'Technology/Digital Media': 'Technology & Software',
#     'Cloud Services': 'Technology & Software',
#     'Cloud Technology': 'Technology & Software',
#     'Cloud Computing': 'Technology & Software',
#     'Software Engineering': 'Technology & Software',
#     'Information Technology': 'Technology & Software',
#     'IT Services': 'Technology & Software',
#     'IT Infrastructure': 'Technology & Software',
#     'Technology Solutions': 'Technology & Software',
#     'Data Technology': 'Technology & Software',
#     'Database Technology': 'Technology & Software',

#     # AI & Machine Learning
#     'AI Research and Innovation': 'AI & Machine Learning',
#     'Machine Learning': 'AI & Machine Learning',
#     'Digital Marketing/AI': 'AI & Machine Learning',

#     # Consulting & Professional Services
#     'IT Consulting': 'Consulting & Professional Services',
#     'Engineering Consulting': 'Consulting & Professional Services',
#     'Technology Consulting': 'Consulting & Professional Services',
#     'Consulting': 'Consulting & Professional Services',
#     'Pharmaceutical Consulting': 'Consulting & Professional Services',

#     # E-commerce & Retail
#     'E-commerce': 'E-commerce & Retail',
#     'Retail Technology': 'E-commerce & Retail',
#     'Fashion Retail': 'E-commerce & Retail',
#     'E-commerce Technology': 'E-commerce & Retail',

#     # Healthcare & Life Sciences
#     'Healthcare Technology': 'Healthcare & Life Sciences',
#     'Medical Technology': 'Healthcare & Life Sciences',
#     'Life Sciences': 'Healthcare & Life Sciences',
#     'Healthcare': 'Healthcare & Life Sciences',
#     'Pharmaceuticals': 'Healthcare & Life Sciences',

#     # Financial Services & FinTech
#     'FinTech': 'Financial Services & FinTech',
#     'Financial Technology': 'Financial Services & FinTech',
#     'Financial Services': 'Financial Services & FinTech',
#     'Banking': 'Financial Services & FinTech',
#     'InsurTech': 'Financial Services & FinTech',

#     # Automotive & Transportation
#     'Automotive Technology': 'Automotive & Transportation',
#     'Automotive Engineering': 'Automotive & Transportation',
#     'Transport': 'Automotive & Transportation',
#     'Public Transportation': 'Automotive & Transportation',
#     'Automotive Software': 'Automotive & Transportation',

#     # Gaming & Entertainment
#     'Gaming Technology': 'Gaming & Entertainment',
#     'Gaming': 'Gaming & Entertainment',
#     'Video Game Development': 'Gaming & Entertainment',
#     'Media and Entertainment': 'Gaming & Entertainment',

#     # Energy & Sustainability
#     'Energy Technology': 'Energy & Sustainability',
#     'Renewable Energy': 'Energy & Sustainability',
#     'Green Technology': 'Energy & Sustainability',
#     'Sustainability Technology': 'Energy & Sustainability',
#     'Energy': 'Energy & Sustainability',

#     # Manufacturing & Industrial
#     'Manufacturing Technology': 'Manufacturing & Industrial',
#     'Industrial Technology': 'Manufacturing & Industrial',
#     'Industrial Automation': 'Manufacturing & Industrial',
#     'Manufacturing': 'Manufacturing & Industrial',
#     '3D-printing teknologi': 'Manufacturing & Industrial',

#     # Security & Defense
#     'Cybersecurity': 'Security & Defense',
#     'Defense and Security Technology': 'Security & Defense',

#     # HR & Recruitment
#     'HR Technology': 'HR & Recruitment',
#     'HR Services': 'HR & Recruitment',
#     'Recruitment': 'HR & Recruitment',
#     'Tech Recruitment': 'HR & Recruitment',
# }


# # Industry mapping dictionary remains the same as before
# INDUSTRY_MAPPING = {
#     # [Previous mapping dictionary content remains the same]
#     # Technology & Software
#     'SaaS': 'Technology & Software',
#     'Software Development': 'Technology & Software',
#     'Technology/Digital Media': 'Technology & Software',
#     'Cloud Services': 'Technology & Software',
#     'Cloud Technology': 'Technology & Software',
#     'Cloud Computing': 'Technology & Software',
#     'Software Engineering': 'Technology & Software',
#     'Information Technology': 'Technology & Software',
#     'IT Services': 'Technology & Software',
#     'IT Infrastructure': 'Technology & Software',
#     'Technology Solutions': 'Technology & Software',
#     'Data Technology': 'Technology & Software',
#     'Database Technology': 'Technology & Software',

#     # AI & Machine Learning
#     'AI Research and Innovation': 'AI & Machine Learning',
#     'Machine Learning': 'AI & Machine Learning',
#     'Digital Marketing/AI': 'AI & Machine Learning',

#     # Consulting & Professional Services
#     'IT Consulting': 'Consulting & Professional Services',
#     'Engineering Consulting': 'Consulting & Professional Services',
#     'Technology Consulting': 'Consulting & Professional Services',
#     'Consulting': 'Consulting & Professional Services',
#     'Pharmaceutical Consulting': 'Consulting & Professional Services',

#     # E-commerce & Retail
#     'E-commerce': 'E-commerce & Retail',
#     'Retail Technology': 'E-commerce & Retail',
#     'Fashion Retail': 'E-commerce & Retail',
#     'E-commerce Technology': 'E-commerce & Retail',

#     # Healthcare & Life Sciences
#     'Healthcare Technology': 'Healthcare & Life Sciences',
#     'Medical Technology': 'Healthcare & Life Sciences',
#     'Life Sciences': 'Healthcare & Life Sciences',
#     'Healthcare': 'Healthcare & Life Sciences',
#     'Pharmaceuticals': 'Healthcare & Life Sciences',

#     # Financial Services & FinTech
#     'FinTech': 'Financial Services & FinTech',
#     'Financial Technology': 'Financial Services & FinTech',
#     'Financial Services': 'Financial Services & FinTech',
#     'Banking': 'Financial Services & FinTech',
#     'InsurTech': 'Financial Services & FinTech',

#     # Automotive & Transportation
#     'Automotive Technology': 'Automotive & Transportation',
#     'Automotive Engineering': 'Automotive & Transportation',
#     'Transport': 'Automotive & Transportation',
#     'Public Transportation': 'Automotive & Transportation',
#     'Automotive Software': 'Automotive & Transportation',

#     # Gaming & Entertainment
#     'Gaming Technology': 'Gaming & Entertainment',
#     'Gaming': 'Gaming & Entertainment',
#     'Video Game Development': 'Gaming & Entertainment',
#     'Media and Entertainment': 'Gaming & Entertainment',

#     # Energy & Sustainability
#     'Energy Technology': 'Energy & Sustainability',
#     'Renewable Energy': 'Energy & Sustainability',
#     'Green Technology': 'Energy & Sustainability',
#     'Sustainability Technology': 'Energy & Sustainability',
#     'Energy': 'Energy & Sustainability',

#     # Manufacturing & Industrial
#     'Manufacturing Technology': 'Manufacturing & Industrial',
#     'Industrial Technology': 'Manufacturing & Industrial',
#     'Industrial Automation': 'Manufacturing & Industrial',
#     'Manufacturing': 'Manufacturing & Industrial',
#     '3D-printing teknologi': 'Manufacturing & Industrial',

#     # Security & Defense
#     'Cybersecurity': 'Security & Defense',
#     'Defense and Security Technology': 'Security & Defense',

#     # HR & Recruitment
#     'HR Technology': 'HR & Recruitment',
#     'HR Services': 'HR & Recruitment',
#     'Recruitment': 'HR & Recruitment',
#     'Tech Recruitment': 'HR & Recruitment',
# }


def load_json_files(directory="business_info/business_info_AI_Engineer"):
    """
    Load and combine all JSON files from the specified directory
    """
    all_data = []
    directory_path = Path(directory)

    if not directory_path.exists():
        st.error(f"Directory {directory} not found!")
        return []

    for json_file in directory_path.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_data.append(data)
                # st.sidebar.success(f"Successfully loaded: {json_file.name}")
        except Exception as e:
            st.sidebar.error(f"Error loading {json_file.name}: {str(e)}")

    return all_data


def process_company_data(data):
    """
    Process the JSON data and extract relevant information.
    """
    companies = []

    # Handle both single company and multiple company documents
    if isinstance(data, list):
        documents = data
    else:
        documents = [data]

    for doc in documents:
        if 'document_content' in doc:  # Handle nested structure
            try:
                content = json.loads(doc['document_content'])
                if 'company_info' in content:
                    doc = content
            except:
                pass

        if 'company_info' in doc:
            company = doc['company_info']
            # Map industries to broader categories
            mapped_industries = []
            if 'industries' in company:
                for industry in company['industries']:
                    mapped_industry = INDUSTRY_MAPPING.get(industry, 'Other')
                    if mapped_industry not in mapped_industries:
                        mapped_industries.append(mapped_industry)

            companies.append({
                'name': company.get('name', ''),
                'industries': mapped_industries,
                'locations': company.get('locations', []),
                'skills': company.get('skills', []),
                'job_titles': company.get('job_titles', [])
            })

    return pd.DataFrame(companies)


def create_industry_trends(df):
    """
    Create industry trends visualization
    """
    industry_counts = defaultdict(int)
    for industries in df['industries']:
        for industry in industries:
            industry_counts[industry] += 1

    industry_df = pd.DataFrame({
        'Industry': list(industry_counts.keys()),
        'Count': list(industry_counts.values())
    }).sort_values('Count', ascending=False)

    fig = px.bar(industry_df,
                 x='Industry',
                 y='Count',
                 title='Industry Distribution',
                 color='Count',
                 color_continuous_scale='Viridis')

    fig.update_layout(
        xaxis_tickangle=45,
        height=600,
        showlegend=False
    )
    return fig


def create_skill_network(df):
    """
    Create a visualization showing relationships between skills
    """
    skill_pairs = defaultdict(int)
    for skills in df['skills']:
        for i, skill1 in enumerate(skills):
            for skill2 in skills[i+1:]:
                if skill1 < skill2:
                    skill_pairs[(skill1, skill2)] += 1
                else:
                    skill_pairs[(skill2, skill1)] += 1

    # Convert to DataFrame for visualization
    pairs_df = pd.DataFrame([
        {'skill1': pair[0], 'skill2': pair[1], 'count': count}
        for pair, count in skill_pairs.items()
    ]).sort_values('count', ascending=False).head(20)  # Top 20 pairs

    return pairs_df


def create_dashboard(df):
    st.title("Swedish Tech Companies Analysis Dashboard")
    st.write(f"Analyzing {len(df)} companies")

    # Add filters in sidebar
    st.sidebar.header("Filters")
    selected_industries = st.sidebar.multiselect(
        "Select Industries",
        sorted(list(set([ind for inds in df['industries'] for ind in inds])))
    )

    selected_locations = st.sidebar.multiselect(
        "Select Locations",
        sorted(list(set([loc for locs in df['locations'] for loc in locs])))
    )

    # Filter data based on selections
    filtered_df = df.copy()
    if selected_industries:
        filtered_df = filtered_df[filtered_df['industries'].apply(
            lambda x: any(ind in selected_industries for ind in x))]
    if selected_locations:
        filtered_df = filtered_df[filtered_df['locations'].apply(
            lambda x: any(loc in selected_locations for loc in x))]

    # Create main dashboard layout
    col1, col2 = st.columns(2)

    with col1:
        st.header("Industry Distribution")
        fig = create_industry_trends(filtered_df)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.header("Geographic Distribution")
        location_counts = defaultdict(int)
        for locations in filtered_df['locations']:
            for location in locations:
                location_counts[location] += 1

        location_df = pd.DataFrame({
            'Location': list(location_counts.keys()),
            'Count': list(location_counts.values())
        }).sort_values('Count', ascending=False)

        fig = px.pie(location_df, values='Count', names='Location',
                     title='Company Distribution by Location')
        st.plotly_chart(fig, use_container_width=True)

    # Skills Analysis
    st.header("Skills Analysis")
    col3, col4 = st.columns(2)

    with col3:
        skill_counts = defaultdict(int)
        for skills in filtered_df['skills']:
            for skill in skills:
                skill_counts[skill] += 1

        skill_df = pd.DataFrame({
            'Skill': list(skill_counts.keys()),
            'Count': list(skill_counts.values())
        }).sort_values('Count', ascending=False).head(20)

        fig = px.bar(skill_df, x='Count', y='Skill',
                     title='Top 20 Most Required Skills',
                     orientation='h')
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        # Show skill relationships
        skill_pairs = create_skill_network(filtered_df)
        fig = px.scatter(skill_pairs, x='skill1', y='skill2', size='count',
                         title='Skill Co-occurrence Network',
                         color='count',
                         hover_data=['count'])
        fig.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    # Job Titles Analysis
    st.header("Job Title Analysis")
    job_counts = defaultdict(int)
    for titles in filtered_df['job_titles']:
        for title in titles:
            job_counts[title] += 1

    job_df = pd.DataFrame({
        'Job Title': list(job_counts.keys()),
        'Count': list(job_counts.values())
    }).sort_values('Count', ascending=False).head(15)

    fig = px.bar(job_df, x='Job Title', y='Count',
                 title='Most Common Job Titles',
                 color='Count',
                 color_continuous_scale='Viridis')
    fig.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

    # Add detailed data table
    st.header("Detailed Company Data")
    st.dataframe(
        filtered_df[['name', 'industries', 'locations', 'job_titles']])


def main():
    st.set_page_config(page_title="Tech Companies Analysis", layout="wide")

    # Load data from directory
    json_data = load_json_files()

    if json_data:
        # Process all companies from all files
        all_companies = []
        for data in json_data:
            df = process_company_data(data)
            all_companies.append(df)

        # Combine all dataframes
        combined_df = pd.concat(all_companies, ignore_index=True)

        # Remove duplicates based on company name
        combined_df = combined_df.drop_duplicates(subset=['name'])

        create_dashboard(combined_df)
    else:
        st.error("No data found in the business_info directory.")


if __name__ == "__main__":
    main()
