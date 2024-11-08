import streamlit as st
import pandas as pd
import plotly.express as px
from utils.industry_map import load_company_data, get_industry_trends, extract_all_skills, INDUSTRY_MAPPING  # Added imports
from collections import Counter

# Trender och Insikter
st.header("Observationer och trender")
col1, col2 = st.columns(2)
with col1:
    st.write("""
    Baserat på analysen av jobbannonser.
    
    1. **Kompetensutveckling:**
       - Stark efterfrågan på Python och maskininlärningskompetenser
       - Ökat fokus på molnplattformar (AWS, Azure)
       - Växande betydelse av MLOps och distributionskompetenser
    
    2. **Branschfokus:**
       - IT-konsulttjänster och tjänster leder i jobbmöjligheter
       - Växande AI-användning i traditionella industrier
       - Fokus på praktisk implementeringserfarenhet
    
    3. **Erfarenhetskrav:**
       - De flesta positioner kräver 3-5 års erfarenhet
       - Seniorroller kräver ofta specifik branschkunskap
       - Juniorpositioner kräver ofta stark teoretisk grund
    
    4. **Geografiska Trender:**
       - Stora centralorter: Stockholm, Göteborg, Malmö
       - Fler alternativ för distansarbete
       - Regionala skillnader i kompetenskrav
    """)

with col2:
    # Add Industry Landscape Section
    # st.header("Industry Landscape")
    companies = load_company_data()
    excluded_industries = []  # Define as needed or add filters
    industry_df = get_industry_trends(companies, excluded_industries)
    fig = px.bar(industry_df,
                 y='count',
                 x=industry_df.index,
                 # orientation='v',
                 title="Industry Distribution")
    st.plotly_chart(fig)

    # Add Trend Analysis and Predictions Section
    # st.header("Trend Analysis and Predictions")

    # Calculate trending skills
    all_skills = extract_all_skills(companies, excluded_industries)
    top_skills = pd.DataFrame.from_dict(
        all_skills, orient='index', columns=['count'])
    top_skills = top_skills.sort_values('count', ascending=False).head(10)

    fig = px.bar(top_skills,
                 x=top_skills.index,
                 y='count',
                 title="Top 10 In-Demand Skills")
    st.plotly_chart(fig)

# # Add Key Insights Section
# st.header("Key Insights")

# if 'selected_company' in st.session_state:
#     selected_company = st.session_state.selected_company
#     company_skills = set(selected_company['company_info']['skills'])
#     top_skills_set = set(top_skills.index)

#     # Calculate skill alignment considering excluded industries
#     if len(top_skills_set) > 0:
#         alignment_score = len(company_skills.intersection(
#             top_skills_set)) / len(top_skills_set) * 100
#     else:
#         alignment_score = 0

#     # Count companies in same industry excluding filtered industries
#     companies_in_industry = len([c for c in companies
#                                 if any(ind in c['company_info']['industries']
#                                         for ind in selected_company['company_info']['industries'])
#                                 and not any(ind in c['company_info'].get('industries', [])
#                                             for ind in (excluded_industries or []))])

#     st.write(f"""
#     1. **Skill Alignment:** This company's skill set aligns {alignment_score:.1f}% with current market trends
#     {' (excluding filtered industries)' if excluded_industries else ''}.
#     2. **Market Position:** {selected_company['company_info']['name']} is positioned in
#     {', '.join(selected_company['company_info']['industries'])}, which represents
#     {companies_in_industry} companies in our filtered dataset.
#     3. **Geographic Presence:** Based in {', '.join(selected_company['company_info']['locations'])},
#     which is a {
#     'major' if any(loc in ['Stockholm', 'Gothenburg', 'Malmö']
#     for loc in selected_company['company_info']['locations']) else 'growing'} tech hub.
#     """)
# else:
#     st.warning("Please select a company from the dashboard to view insights.")

# # Add Future Recommendations Section
# st.header("Future Recommendations")
# if 'selected_company' in st.session_state:
#     selected_company = st.session_state.selected_company
#     missing_top_skills = set(top_skills.index) - \
#         set(selected_company['company_info']['skills'])
#     if missing_top_skills:
#         st.write("Consider developing capabilities in:")
#         for skill in missing_top_skills:
#             st.write(f"- {skill}")
# else:
#     st.warning(
#         "Please select a company from the dashboard to view future recommendations.")
