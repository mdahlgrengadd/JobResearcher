import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from collections import Counter
import numpy as np
import re

# Set page configuration
st.set_page_config(page_title="AI & Python Jobbanalys", layout="wide")


def normalize_language(lang):
    lang = lang.lower().strip()
    # Mapping of variations to standard names
    language_map = {
        'english': 'Engelska',
        'swedish': 'Svenska',
        'svenska': 'Svenska',
        'mandarin': 'Mandarin',
        'chinese': 'Mandarin',
        'german': 'Tyska',
        'deutsch': 'Tyska',
        'french': 'Franska',
        'français': 'Franska',
        'spanish': 'Spanska',
        'español': 'Spanska',
        'dutch': 'Nederländska',
        'nederlands': 'Nederländska'
    }

    # Remove qualifiers and find base language
    base_lang = lang.split('(')[0].strip()
    return language_map.get(base_lang, base_lang.capitalize())

# Function to load and process the data


def load_and_process_data():
    with open('job_results.json', 'r') as file:
        data = json.load(file)

    df = pd.DataFrame(data['Jobs'])

    def is_ai_ml_python_related(row):
        title_keywords = ['AI', 'Machine Learning', 'ML', 'Data Scientist', 'Data Engineer',
                          'Python', 'Artificial Intelligence', 'NLP', 'Deep Learning']

        skills = set(row['Skills']) if isinstance(
            row['Skills'], list) else set()
        skill_keywords = {'Python', 'Machine Learning', 'AI', 'Deep Learning', 'TensorFlow',
                          'PyTorch', 'NLP', 'Neural Networks', 'Data Science', 'Artificial Intelligence'}

        title_match = any(
            keyword.lower() in row['Jobtitle'].lower() for keyword in title_keywords)
        skills_match = bool(skills & skill_keywords)

        return title_match or skills_match

    df_filtered = df[df.apply(is_ai_ml_python_related, axis=1)]
    df_filtered['Years of Experience'] = pd.to_numeric(
        df_filtered['Years of Experience'], errors='coerce')

    return df_filtered


# Load the data
df = load_and_process_data()

# Dashboard title
st.title("AI & Python Jobbmarknadsanalys")
st.markdown(
    "Analys av AI-, maskininlärnings- och Pythonrelaterade jobb i Sverige")

# Create columns for all visualizations
col1, col2 = st.columns(2)

with col1:
    # Company Industry Distribution
    st.subheader("Fördelning av jobb per bransch")
    industry_counts = df['Company Industry'].value_counts().head(10)
    fig_industry = px.pie(values=industry_counts.values,
                          names=industry_counts.index,
                          title="Topp 10 branscher")
    st.plotly_chart(fig_industry, use_container_width=True)

    # Years of Experience Requirements
    st.subheader("Krav på arbetslivserfarenhet")
    fig_exp = px.histogram(df[df['Years of Experience'].notna()],
                           x='Years of Experience',
                           nbins=10,
                           title="Fördelning av erfarenhetskrav")
    fig_exp.update_layout(xaxis_title="År av erfarenhet",
                          yaxis_title="Antal jobb")
    fig_exp.update_layout(
        bargap=0.1
    )
    st.plotly_chart(fig_exp, use_container_width=True)

    # Education Analysis
    st.subheader("Utbildningskrav")
    edu_df = df[df['Education'].notna()]

    def categorize_education(edu_str):
        if pd.isna(edu_str):
            return "Ej specificerat"
        edu_str = str(edu_str).lower()
        if any(term in edu_str for term in ['phd', 'doktor']):
            return "Doktorsexamen"
        elif any(term in edu_str for term in ['master', 'msc', 'civilingenjör']):
            return "Master/Civilingenjör"
        elif any(term in edu_str for term in ['bachelor', 'kandidat', 'bsc']):
            return "Kandidatexamen"
        else:
            return "Övrig utbildning"

    edu_df['Education_Category'] = edu_df['Education'].apply(
        categorize_education)
    edu_counts = edu_df['Education_Category'].value_counts()

    fig_edu = px.pie(values=edu_counts.values,
                     names=edu_counts.index,
                     title="Fördelning av utbildningskrav")
    st.plotly_chart(fig_edu, use_container_width=True)

    # Language Requirements
    st.subheader("Språkkrav")
    # Normalize and count languages
    all_languages = []
    for langs in df['Languages']:
        if isinstance(langs, list):
            all_languages.extend([normalize_language(lang) for lang in langs])

    lang_counts = pd.Series(Counter(all_languages)).sort_values(ascending=True)
    fig_lang = px.bar(x=lang_counts.values,
                      y=lang_counts.index,
                      orientation='h',
                      title="Efterfrågade språkkunskaper")
    fig_lang.update_layout(xaxis_title="Antal jobbannonser",
                           yaxis_title="Språk")
    st.plotly_chart(fig_lang, use_container_width=True)

with col2:
    # Location Distribution
    st.subheader("Jobbfördelning per ort")
    location_counts = df['Location'].value_counts().head(10)
    fig_location = px.bar(x=location_counts.index,
                          y=location_counts.values,
                          title="Topp 10 orter")
    fig_location.update_layout(xaxis_title="Ort",
                               yaxis_title="Antal jobb")
    st.plotly_chart(fig_location, use_container_width=True)

    # Most Common Skills
    st.subheader("Mest efterfrågade kompetenser")
    all_skills = [skill for skills in df['Skills']
                  if isinstance(skills, list) for skill in skills]
    skill_counts = pd.Series(Counter(all_skills)).sort_values(
        ascending=True).tail(15)

    fig_skills = px.bar(x=skill_counts.values,
                        y=skill_counts.index,
                        orientation='h',
                        title="Topp 15 efterfrågade kompetenser")
    fig_skills.update_layout(xaxis_title="Antal jobbannonser",
                             yaxis_title="Kompetens")
    st.plotly_chart(fig_skills, use_container_width=True)

    # Common fields of study
    st.subheader("Vanligaste studieinriktningar")
    common_fields = ['Computer Science', 'Engineering', 'Data Science',
                     'Mathematics', 'Statistics', 'Physics']
    field_counts = []
    for field in common_fields:
        count = edu_df['Education'].str.contains(field, case=False).sum()
        field_counts.append({'Field': field, 'Count': count})

    field_df = pd.DataFrame(field_counts)
    fig_fields = px.bar(field_df, x='Field', y='Count',
                        title="Efterfrågade studieinriktningar")
    fig_fields.update_layout(xaxis_title="Studieinriktning",
                             bargap=0.1,
                             yaxis_title="Antal jobbannonser")
    st.plotly_chart(fig_fields, use_container_width=True)

    # Job Titles Analysis
    st.subheader("Analys av jobbtitlar")

    def clean_and_count_title_terms(titles):
        stop_words = {'and', 'or', 'the', 'in', 'at', 'for', 'och', 'med',
                      'på', 'i', 'en', 'ett', '-', '&', 'av'}

        all_words = []
        for title in titles:
            words = title.lower().split()
            words = [word for word in words
                     if len(word) > 1
                     and word not in stop_words
                     and not word.isnumeric()
                     and not all(c in ',%.-/' for c in word)]
            all_words.extend(words)

        return Counter(all_words)

    title_word_counts = clean_and_count_title_terms(df['Jobtitle'])
    title_counts = pd.Series(title_word_counts).sort_values(
        ascending=True).tail(15)

    fig_titles = px.bar(x=title_counts.values,
                        y=title_counts.index,
                        orientation='h',
                        title="Topp 15 vanligaste termer i jobbtitlar")
    fig_titles.update_layout(xaxis_title="Frekvens",
                             yaxis_title="Term")

    st.plotly_chart(fig_titles, use_container_width=True)

# Show raw data option
if st.checkbox('Visa rådata'):
    st.subheader('Rådata')
    st.write(df)
