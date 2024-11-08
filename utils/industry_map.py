# Added imports
import os
import json
import pandas as pd
from collections import Counter
from typing import Dict, List

# Industry mapping dictionary
INDUSTRY_MAPPING = {
    # Technology & Software
    'SaaS': 'Technology & Software',
    'Software Development': 'Technology & Software',
    'Technology/Digital Media': 'Technology & Software',
    'Cloud Services': 'Technology & Software',
    'Cloud Technology': 'Technology & Software',
    'Cloud Computing': 'Technology & Software',
    'Software Engineering': 'Technology & Software',
    'Information Technology': 'Technology & Software',
    'IT Services': 'Technology & Software',
    'IT Infrastructure': 'Technology & Software',
    'Technology Solutions': 'Technology & Software',
    'Data Technology': 'Technology & Software',
    'Database Technology': 'Technology & Software',

    # AI & Machine Learning
    'AI Research and Innovation': 'AI & Machine Learning',
    'Machine Learning': 'AI & Machine Learning',
    'Digital Marketing/AI': 'AI & Machine Learning',

    # Consulting & Professional Services
    'IT Consulting': 'Consulting & Professional Services',
    'Engineering Consulting': 'Consulting & Professional Services',
    'Technology Consulting': 'Consulting & Professional Services',
    'Consulting': 'Consulting & Professional Services',
    'Pharmaceutical Consulting': 'Consulting & Professional Services',

    # E-commerce & Retail
    'E-commerce': 'E-commerce & Retail',
    'Retail Technology': 'E-commerce & Retail',
    'Fashion Retail': 'E-commerce & Retail',
    'E-commerce Technology': 'E-commerce & Retail',

    # Healthcare & Life Sciences
    'Healthcare Technology': 'Healthcare & Life Sciences',
    'Medical Technology': 'Healthcare & Life Sciences',
    'Life Sciences': 'Healthcare & Life Sciences',
    'Healthcare': 'Healthcare & Life Sciences',
    'Pharmaceuticals': 'Healthcare & Life Sciences',

    # Financial Services & FinTech
    'FinTech': 'Financial Services & FinTech',
    'Financial Technology': 'Financial Services & FinTech',
    'Financial Services': 'Financial Services & FinTech',
    'Banking': 'Financial Services & FinTech',
    'InsurTech': 'Financial Services & FinTech',

    # Automotive & Transportation
    'Automotive Technology': 'Automotive & Transportation',
    'Automotive Engineering': 'Automotive & Transportation',
    'Transport': 'Automotive & Transportation',
    'Public Transportation': 'Automotive & Transportation',
    'Automotive Software': 'Automotive & Transportation',

    # Gaming & Entertainment
    'Gaming Technology': 'Gaming & Entertainment',
    'Gaming': 'Gaming & Entertainment',
    'Video Game Development': 'Gaming & Entertainment',
    'Media and Entertainment': 'Gaming & Entertainment',

    # Energy & Sustainability
    'Energy Technology': 'Energy & Sustainability',
    'Renewable Energy': 'Energy & Sustainability',
    'Green Technology': 'Energy & Sustainability',
    'Sustainability Technology': 'Energy & Sustainability',
    'Energy': 'Energy & Sustainability',

    # Manufacturing & Industrial
    'Manufacturing Technology': 'Manufacturing & Industrial',
    'Industrial Technology': 'Manufacturing & Industrial',
    'Industrial Automation': 'Manufacturing & Industrial',
    'Manufacturing': 'Manufacturing & Industrial',
    '3D-printing teknologi': 'Manufacturing & Industrial',

    # Security & Defense
    'Cybersecurity': 'Security & Defense',
    'Defense and Security Technology': 'Security & Defense',

    # HR & Recruitment
    'HR Technology': 'HR & Recruitment',
    'HR Services': 'HR & Recruitment',
    'Recruitment': 'HR & Recruitment',
    'Tech Recruitment': 'HR & Recruitment',
}


def load_company_data(directory: str = "business_info/business_info_AI_Engineer") -> List[Dict]:
    """Load all company JSON files from the specified directory."""
    companies = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                companies.append(json.load(f))
    return companies


def get_industry_trends(companies: List[Dict], excluded_industries: List[str] = None) -> pd.DataFrame:
    """Analyze industry trends from companies, excluding specified industry groups."""
    industries = []
    for company in companies:
        if 'company_info' in company and 'industries' in company['company_info']:
            company_industries = [INDUSTRY_MAPPING.get(
                ind, "Other") for ind in company['company_info']['industries']]
            if excluded_industries:
                company_industries = [
                    ind for ind in company_industries if ind not in excluded_industries]
            industries.extend(company_industries)

    industry_counts = Counter(industries)
    df = pd.DataFrame.from_dict(
        industry_counts, orient='index', columns=['count'])
    df.sort_values('count', ascending=True, inplace=True)
    return df


def extract_all_skills(companies: List[Dict], excluded_industries: List[str] = None) -> Counter:
    """Extract and count all skills from companies, excluding specified industries."""
    all_skills = []
    for company in companies:
        if 'company_info' not in company:
            continue

        # Skip companies in excluded industries
        if excluded_industries and any(ind in company['company_info'].get('industries', [])
                                       for ind in excluded_industries):
            continue

        if 'skills' in company['company_info']:
            all_skills.extend(company['company_info']['skills'])
    return Counter(all_skills)
