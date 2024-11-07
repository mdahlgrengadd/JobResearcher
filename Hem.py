import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import json
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os
import glob

# Add these functions after the existing load_data function


def create_wordcloud(df):
    """
    Create a word cloud from skills in job listings
    """
    # Flatten the skills list
    all_skills = []
    for skills in df['Skills']:
        if isinstance(skills, list):
            all_skills.extend(skills)

    # Create text for word cloud
    text = ' '.join(all_skills)

    # Create and generate a word cloud image
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='black',
        colormap='viridis',
        max_words=100,
        min_font_size=10,
        max_font_size=150,
        random_state=42
    ).generate(text)

    # Create matplotlib figure
    fig, ax = plt.subplots(figsize=(20, 10), facecolor='k')
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')

    return fig


# Set page config
st.set_page_config(
    page_title="Affärsmannaskap Branchanalys",
    page_icon="📊",
    layout="wide"
)

# Load and process data


def load_data(job_data):
    # Convert job data to DataFrame
    df = pd.DataFrame(job_data['Jobs'])

    # Extract all skills into a flat list
    all_skills = [skill for skills in df['Skills'].tolist()
                  for skill in skills]
    # Count skill frequencies
    skill_freq = Counter(all_skills)

    return df, skill_freq


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


json_files = glob.glob('job_listings/*.json')
file_names = [os.path.basename(f) for f in json_files]
selected_file = st.sidebar.selectbox('Välj JSON-fil', file_names)

with open(os.path.join('job_listings', selected_file), 'r') as file:
    job_data = json.load(file)


def load_and_process_data():
    # Replace hardcoded filename with selected_file
    with open(os.path.join('job_listings', selected_file), 'r') as file:
        data = json.load(file)

    # Extract and store metadata
    search_query = data.get('Search query', 'N/A')
    search_engine = data.get('Search Engine', 'N/A')
    total_jobs_found = data.get('Total Jobs Found', 0)
    pages_processed = data.get('Pages Processed', 0)

    st.sidebar.info(f"**Sökuppgifter:** {search_query}")
    st.sidebar.info(f"**Sökmotor:** {search_engine}")
    st.sidebar.info(f"**Totala Jobb Hittade:** {total_jobs_found}")
    st.sidebar.info(f"**Sidor Bearbetade:** {pages_processed}")

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

    df['Has_Python'] = df['Skills'].apply(
        lambda x: 'Python' in x if isinstance(x, list) else False)
    df['Has_AI'] = df['Skills'].apply(lambda x: any(skill in x for skill in [
        'AI', 'Machine Learning', 'Deep Learning', 'Neural Networks', 'NLP']) if isinstance(x, list) else False)

    df_filtered = df[df.apply(is_ai_ml_python_related, axis=1)]
    df_filtered['Years of Experience'] = pd.to_numeric(
        df_filtered['Years of Experience'], errors='coerce')

    return df, df_filtered


def create_skill_distribution(df):
    # Flatten skills list and count occurrences
    all_skills = [skill for skills in df['Skills']
                  if isinstance(skills, list) for skill in skills]
    skill_counts = Counter(all_skills)

    # Create DataFrame for plotting
    skills_df = pd.DataFrame.from_dict(
        skill_counts, orient='index', columns=['Antal']).reset_index()
    skills_df.columns = ['Kompetens', 'Antal']
    skills_df = skills_df.sort_values('Antal', ascending=True)

    # Create horizontal bar chart
    fig = px.bar(skills_df.tail(15), y='Kompetens', x='Antal',
                 orientation='h', title='Mest Efterfrågade Kompetenser',
                 color='Antal', color_continuous_scale='viridis')
    # fig.update_layout(height=600)
    return fig


def show_dashboard(df, skill_freq):

    # Load the data
    df, df_filtered = load_and_process_data()

    # Dashboard title
    st.title("Affärsmannaskap Branchanalys")
    st.header(
        "Analys av AI-, maskininlärnings- och Pythonrelaterade jobb i Sverige")

    # Display basic statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Totalt Antal Jobbannonser", len(df))
    with col2:
        st.metric("Python Jobb", df['Has_Python'].sum())
    with col3:
        st.metric("AI/ML Jobb", df['Has_AI'].sum())
    with col4:
        avg_exp = df_filtered['Years of Experience'].mean()
        st.metric("Genomsnittlig erfarenhet som krävs", f"{avg_exp:.1f} år")

    # Role Distribution
    st.header("1. Analys av Yrkesroller")

    # Fill missing 'Company Industry' values
    df['Company Industry'] = df['Company Industry'].fillna('Unknown')

    fig_roles = px.treemap(
        df,
        path=['Company Industry', 'Jobtitle'],
        title="Fördelning av Yrkesroller per Bransch",
        height=640
    )
    st.plotly_chart(fig_roles)

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
                all_languages.extend([normalize_language(lang)
                                     for lang in langs])

        lang_counts = pd.Series(Counter(all_languages)
                                ).sort_values(ascending=True)
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
        # all_skills = [skill for skills in df['Skills']
        #               if isinstance(skills, list) for skill in skills]
        # skill_counts = pd.Series(Counter(all_skills)).sort_values(
        #     ascending=True).tail(15)

        # fig_skills = px.bar(x=skill_counts.values,
        #                     y=skill_counts.index,
        #                     orientation='h',
        #                     title="Topp 15 efterfrågade kompetenser")
        # fig_skills.update_layout(xaxis_title="Antal jobbannonser",
        #                          yaxis_title="Kompetens")
        # st.plotly_chart(fig_skills, use_container_width=True)
        st.plotly_chart(create_skill_distribution(df),
                        use_container_width=True)

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

    st.subheader("")
    wordcloud_fig = create_wordcloud(df)
    st.sidebar.pyplot(wordcloud_fig)
    plt.close(wordcloud_fig)  # Clean up matplotlib figure


def show_dashboard2(df, skill_freq):
    st.title("AI & Python Arbetsmarknadsanalys")
    st.subheader("Analys av Tech-branschens Jobb i Sverige")

    # Display basic statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Totalt Antal Jobbannonser", len(df))
    with col2:
        avg_exp = df['Years of Experience'].mean()
        st.metric("Genomsnittlig erfarenhet som krävs",
                  f"{avg_exp:.1f} år")
    with col3:
        st.metric("Städer med Öppna Tjänster", df['Location'].nunique())

    # Role Distribution
    st.header("1. Analys av Yrkesroller")

    fig_roles = px.treemap(
        df,
        path=['Company Industry', 'Jobtitle'],
        title="Fördelning av Yrkesroller per Bransch",
        width=800,
        height=500
    )
    st.plotly_chart(fig_roles)

    # Skills Analysis
    st.header("2. Nyckelkompetenser")

    skills_df = pd.DataFrame.from_dict(
        skill_freq, orient='index', columns=['count'])
    skills_df = skills_df.reset_index().rename(columns={'index': 'skill'})
    skills_df = skills_df.sort_values('count', ascending=True)

    fig_skills = px.bar(
        skills_df.tail(15),
        x='count',
        y='skill',
        orientation='h',
        title="Mest Efterfrågade Kompetenser",
        labels={'count': 'Antal Jobbannonser', 'skill': 'Kompetens'}
    )
    st.plotly_chart(fig_skills)

    # Company Analysis
    st.header("3. Företagslandskap")

    company_sizes = df['Company Size'].value_counts()
    fig_sizes = px.pie(
        values=company_sizes.values,
        names=company_sizes.index,
        title="Fördelning av Företagsstorlekar",
        hole=0.4
    )

    industries = df['Company Industry'].value_counts()
    fig_industries = px.bar(
        x=industries.index,
        y=industries.values,
        title="Jobbannonser per Bransch",
        labels={'x': 'Bransch', 'y': 'Antal Jobbannonser'}
    )

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_sizes)
    with col2:
        st.plotly_chart(fig_industries)

    # Experience Requirements
    st.header("4. Erfarenhetskrav")

    def categorize_experience(years):
        if years == 0:
            return "Instegsnivå"
        elif years <= 2:
            return "Junior (1-2 år)"
        elif years <= 5:
            return "Mellannivå (3-5 år)"
        else:
            return "Senior (6+ år)"

    df['experience_category'] = df['Years of Experience'].apply(
        categorize_experience)
    exp_dist = df['experience_category'].value_counts()

    fig_exp = px.pie(
        values=exp_dist.values,
        names=exp_dist.index,
        title="Fördelning av Erfarenhetskrav",
        hole=0.4
    )
    st.plotly_chart(fig_exp)

    # Location Analysis
    st.header("5. Geografisk Fördelning")

    location_counts = df['Location'].value_counts()
    fig_locations = px.bar(
        x=location_counts.index,
        y=location_counts.values,
        title="Jobbmöjligheter per Stad",
        labels={'x': 'Stad', 'y': 'Antal Jobbannonser'}
    )
    st.plotly_chart(fig_locations)

    # Language Requirements
    st.header("6. Språkkrav")

    all_languages = [lang for langs in df['Languages'].tolist()
                     for lang in langs]
    lang_freq = Counter(all_languages)

    fig_lang = px.pie(
        values=lang_freq.values(),
        names=lang_freq.keys(),
        title="Fördelning av Språkkrav",
        hole=0.4
    )
    st.plotly_chart(fig_lang)


def show_data_explorer(df):
    st.title("Utforska Jobbannonser")
    st.write("Utforska och filtrera rådata från jobbannonser")

    # Sidebar filters
    st.sidebar.header("Filter")

    unique_locations = df['Location'].unique()
    valid_locations = sorted(
        [loc for loc in unique_locations if loc is not None])
    locations = ['Alla'] + valid_locations
    selected_location = st.sidebar.selectbox('Välj Ort', locations)

    unique_industries = df['Company Industry'].unique()
    valid_industries = sorted(
        [ind for ind in unique_industries if ind is not None])
    industries = ['Alla'] + valid_industries
    selected_industry = st.sidebar.selectbox('Välj Bransch', industries)

    min_exp = int(df['Years of Experience'].fillna(0).min())
    max_exp = int(df['Years of Experience'].fillna(0).max())
    exp_range = st.sidebar.slider(
        'Års Erfarenhet',
        min_exp, max_exp,
        (min_exp, max_exp)
    )

    all_skills = set([skill for skills in df['Skills'].dropna()
                     for skill in (skills if skills else [])])
    selected_skills = st.sidebar.multiselect(
        'Välj Önskade Kompetenser', sorted(all_skills))

    # Apply filters
    filtered_df = df.copy()

    if selected_location != 'Alla':
        filtered_df = filtered_df[filtered_df['Location'] == selected_location]

    if selected_industry != 'Alla':
        filtered_df = filtered_df[filtered_df['Company Industry']
                                  == selected_industry]

    filtered_df = filtered_df[
        (filtered_df['Years of Experience'].fillna(0) >= exp_range[0]) &
        (filtered_df['Years of Experience'].fillna(0) <= exp_range[1])
    ]

    if selected_skills:
        filtered_df = filtered_df[
            filtered_df['Skills'].apply(lambda x: all(
                skill in (x or []) for skill in selected_skills))
        ]

    st.write(f"Visar {len(filtered_df)} jobbannonser")

    columns_to_display = ['Company', 'Jobtitle', 'Location', 'Company Industry',
                          'Years of Experience', 'Skills', 'Languages']

    display_df = filtered_df[columns_to_display].copy()
    display_df['Skills'] = display_df['Skills'].apply(
        lambda x: ', '.join(x) if isinstance(x, list) else '')
    display_df['Languages'] = display_df['Languages'].apply(
        lambda x: ', '.join(x) if isinstance(x, list) else '')

    st.dataframe(display_df, use_container_width=True)

    if st.checkbox('Visa detaljerade jobbeskrivningar'):
        selected_job = st.selectbox(
            'Välj ett jobb för att se detaljer',
            filtered_df['Jobtitle'].tolist()
        )

        job_details = filtered_df[filtered_df['Jobtitle']
                                  == selected_job].iloc[0]

        st.subheader(f"{job_details['Jobtitle']} hos {job_details['Company']}")
        st.write(
            f"**Företagsbeskrivning:** {job_details['Company Description']}")
        st.write(f"**Ort:** {job_details['Location'] or 'Ej specificerat'}")
        st.write(
            f"**Erfarenhetskrav:** {job_details['Years of Experience'] or 'Ej specificerat'} år")
        st.write(
            f"**Utbildning:** {job_details['Education'] or 'Ej specificerat'}")
        st.write("**Önskade Kompetenser:**")
        st.write(", ".join(job_details['Skills']) if isinstance(
            job_details['Skills'], list) else 'Ej specificerat')
        st.write("**Jobbeskrivning:**")
        st.write(job_details['Job Description'] or 'Ej specificerat')


def main():
    with open('job_results3.json') as f:
        job_data = json.load(f)

    df, skill_freq = load_data(job_data)

    # st.sidebar.title("Välj")
    page = st.sidebar.radio("Gå till", ["Diagram", "Annonser"])

    if page == "Diagram":
        show_dashboard(df, skill_freq)
    else:
        show_data_explorer(df)


if __name__ == "__main__":
    main()
