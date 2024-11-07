import streamlit as st


def generate_career_analysis():
    st.title("Yrkesroller och Kompetensbehov inom AI och Python-utveckling")

    st.header("1. Kartläggning av Yrkesroller")
    st.markdown("""
    ### A. Huvudsakliga Yrkeskategorier
    
    1. **AI/ML Engineer**
    - *Beskrivning*: Utvecklar och implementerar AI- och ML-lösningar
    - *Huvuduppgifter*:
        - Bygga och optimera ML-modeller
        - Implementera AI-pipelines
        - Integrera AI-lösningar i produktionsmiljö
    - *Vanliga titlar*: 
        - Machine Learning Engineer
        - AI Developer
        - AI Systems Engineer
    
    2. **Data Scientist med AI-fokus**
    - *Beskrivning*: Analyserar data och utvecklar AI-modeller
    - *Huvuduppgifter*:
        - Statistisk analys och modellering
        - Experimentdesign och utvärdering
        - Datavisualisering och rapportering
    - *Vanliga titlar*:
        - AI Research Scientist
        - Applied Machine Learning Scientist
        - Quantitative Researcher
    
    3. **MLOps Engineer**
    - *Beskrivning*: Ansvarar för AI-systems infrastruktur och drift
    - *Huvuduppgifter*:
        - Bygga och underhålla ML-pipelines
        - Automatisera AI-processer
        - Säkerställa skalbarhet och prestanda
    - *Vanliga titlar*:
        - ML Platform Engineer
        - AI Infrastructure Engineer
        - ML Operations Specialist
    
    4. **AI Solutions Architect**
    - *Beskrivning*: Designar övergripande AI-lösningar och system
    - *Huvuduppgifter*:
        - Systemarkitektur för AI-lösningar
        - Teknisk projektledning
        - Strategisk planering
    - *Vanliga titlar*:
        - AI Technical Lead
        - ML Solutions Architect
        - AI Systems Architect
    """)

    st.header("2. Efterfrågade Kompetenser")
    st.markdown("""
    ### A. Tekniska Kompetenser
    
    1. **Grundläggande Kompetenser**
    - Python (avancerad nivå)
    - Software engineering principer
    - Versionshantering (Git)
    - Databaskunskaper (SQL/NoSQL)
    
    2. **AI/ML-specifika Kompetenser**
    - Deep Learning frameworks (PyTorch, TensorFlow)
    - ML-algoritmer och modeller
    - Natural Language Processing
    - Computer Vision
    
    3. **Infrastruktur & Verktyg**
    - Cloud platforms (AWS, Azure, GCP)
    - MLOps-verktyg (MLflow, Kubeflow)
    - Containerisering (Docker, Kubernetes)
    - CI/CD för ML-system
    
    ### B. Mjuka Kompetenser
    
    1. **Samarbete & Kommunikation**
    - Tvärfunktionellt samarbete
    - Teknisk dokumentation
    - Presentationsförmåga
    - Pedagogisk förmåga
    
    2. **Problemlösning & Innovation**
    - Analytiskt tänkande
    - Kreativ problemlösning
    - Forskningsmetodik
    - Experimentdesign
    """)

    st.header("3. Företagstyper och Skillnader")
    st.markdown("""
    ### A. Företagskategorier och Fokus
    
    1. **Tech-företag**
    - *Exempel*: Google, Spotify, Klarna
    - *Fokus*:
        - Cutting-edge AI-utveckling
        - Storskaliga AI-system
        - Produktdriven utveckling
    - *Särskilda krav*:
        - Djup teknisk expertis
        - Erfarenhet av storskaliga system
        - Innovationsförmåga
    
    2. **Traditionella Företag i Digital Transformation**
    - *Exempel*: Volvo, AstraZeneca, banker
    - *Fokus*:
        - AI för processoptimering
        - Prediktivt underhåll
        - Kundinsikter
    - *Särskilda krav*:
        - Förståelse för legacy-system
        - Branschkunskap
        - Förändringshantering
    
    3. **Konsultbolag**
    - *Exempel*: Techster Solutions, VIPAS AB
    - *Fokus*:
        - Kundanpassade AI-lösningar
        - Varierande projekt
        - Teknisk rådgivning
    - *Särskilda krav*:
        - Bred teknisk kompetens
        - Anpassningsförmåga
        - Kundkommunikation
    
    4. **AI-fokuserade Startups**
    - *Exempel*: BrightBid, H2O.ai
    - *Fokus*:
        - Innovativa AI-produkter
        - Snabb utveckling
        - Specialiserade lösningar
    - *Särskilda krav*:
        - Full-stack kapabilitet
        - Entreprenöriellt tänkande
        - Snabb inlärning
    """)

    st.header("4. Trender och Framtidsutsikter")
    st.markdown("""
    ### A. Kortsiktiga Trender (1-2 år)
    
    1. **Tekniska Trender**
    - Ökad efterfrågan på MLOps
    - Fokus på AI-säkerhet och robusthet
    - Generativ AI-kompetens
    - Edge AI och embedded ML
    
    2. **Kompetenskrav**
    - Specialisering inom specifika AI-domäner
    - Ökad efterfrågan på end-to-end AI-kunskap
    - Etik och ansvarsfull AI
    
    ### B. Långsiktiga Trender (3-5 år)
    
    1. **Branschens Utveckling**
    - AI-integration i alla affärsprocesser
    - Automatisering av ML-processer
    - Ökad reglering och standardisering
    - Demokratisering av AI-verktyg
    
    2. **Framtida Kompetensbehov**
    - Hybrid AI-kompetens (klassisk ML + deep learning)
    - Quantum computing för AI
    - AutoML och AI-automatisering
    - Domänspecifik AI-expertis
    
    ### C. Emerging Technologies
    
    1. **Nya Teknologiska Områden**
    - Federated Learning
    - AI för hållbarhet
    - Neuromorphic computing
    - AI-drivna utvecklingsverktyg
    
    2. **Kompetensimplikationer**
    - Kontinuerlig vidareutbildning krävs
    - Ökad specialisering
    - Tvärvetenskaplig kompetens
    - Etisk AI-utveckling
    """)

    st.header("5. Sammanfattande Insikter")
    st.markdown("""
    1. **Yrkesrollens Utveckling**
    - Från generalist till specialist
    - Ökad teknisk komplexitet
    - Större fokus på produktion och skalbarhet
    
    2. **Marknadens Behov**
    - Stark och ökande efterfrågan
    - Brist på erfarna utvecklare
    - Behov av både specialister och generalister
    
    3. **Framgångsfaktorer**
    - Kontinuerlig kompetensutveckling
    - Balans mellan teknisk och domänkunskap
    - Anpassningsförmåga till ny teknologi
    
    4. **Utmaningar och Möjligheter**
    - Snabb teknologisk utveckling
    - Ökande komplexitet
    - Många karriärvägar
    - Stort utrymme för specialisering
    """)

    return None


generate_career_analysis()
