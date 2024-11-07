import streamlit as st
import os
import glob
from pathlib import Path


def load_markdown_content(file_path):
    """Load and return the content of a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error loading documentation: {str(e)}"


def create_documentation_pages():
    """Create the documentation navigation and display in Streamlit."""
    st.title("Dashboard Documentation")

    # Create sidebar navigation
    st.sidebar.title("Documentation")

    # Path to documentation files
    docs_path = Path('docs')

    # Dictionary mapping filenames to friendly names
    page_names = {
        # 'main.md': 'Introduction',
        'sections.md': 'About',
        'data_explorer.md': 'Guide',
        # 'trends.md': 'Understanding Trends',
        # 'user_guides.md': 'User Guides',
        # 'help.md': 'Help & Support'
    }

    # Get all markdown files
    markdown_files = sorted(glob.glob(str(docs_path / '*.md')))

    if not markdown_files:
        st.error(
            "No documentation files found. Please ensure the 'docs' directory exists and contains markdown files.")
        return

    # Create tabs for different sections
    tabs = st.tabs([page_names.get(Path(file).name, Path(file).stem)
                   for file in markdown_files])

    # Load and display content in tabs
    for tab, file_path in zip(tabs, markdown_files):
        with tab:
            content = load_markdown_content(file_path)
            st.markdown(content)

            # Add feedback section at bottom of each page
            st.divider()
            with st.expander("📝 Page Feedback"):
                st.write("Was this page helpful?")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("👍 Yes", key=f"yes_{Path(file_path).stem}"):
                        st.success("Thank you for your feedback!")
                with col2:
                    if st.button("👎 No", key=f"no_{Path(file_path).stem}"):
                        st.text_area("How can we improve this page?",
                                     key=f"feedback_{Path(file_path).stem}")
                        if st.button("Submit Feedback", key=f"submit_{Path(file_path).stem}"):
                            st.success("Thank you for your feedback!")


def render_documentation_home():
    """Render the documentation home page with navigation cards."""
    st.title("Dashboard Documentation")

    # Introduction
    st.markdown("""
    Welcome to the AI & Python Job Market Analysis Dashboard documentation. 
    Choose a section below to learn more about different aspects of the dashboard.
    """)

    # Create columns for card layout
    col1, col2 = st.columns(2)

    with col1:
        # Dashboard Sections Card
        with st.container(border=True):
            st.subheader("📊 Dashboard Sections")
            st.write("Learn about each visualization and metric in the dashboard.")
            if st.button("Explore Dashboard Sections", key="sections_btn"):
                st.switch_page("pages/sections.py")

        # Trends Card
        with st.container(border=True):
            st.subheader("📈 Understanding Trends")
            st.write("Interpret market trends and insights from the data.")
            if st.button("View Trends Guide", key="trends_btn"):
                st.switch_page("pages/trends.py")

        # Help Card
        with st.container(border=True):
            st.subheader("🤝 Help & Support")
            st.write("Get assistance and find answers to common questions.")
            if st.button("Get Help", key="help_btn"):
                st.switch_page("pages/help.py")

    with col2:
        # Data Explorer Card
        with st.container(border=True):
            st.subheader("🔍 Data Explorer")
            st.write("Learn how to use filters and explore job listings.")
            if st.button("Open Data Explorer Guide", key="explorer_btn"):
                st.switch_page("pages/data_explorer.py")

        # User Guides Card
        with st.container(border=True):
            st.subheader("💡 User Guides")
            st.write("Specific guides for job seekers, employers, and researchers.")
            if st.button("Read User Guides", key="guides_btn"):
                st.switch_page("pages/user_guides.py")


def setup_streamlit_pages():
    """Set up the Streamlit pages structure."""
    # Create pages directory if it doesn't exist
    pages_dir = Path('pages')
    if not pages_dir.exists():
        pages_dir.mkdir()

    # Create individual page files
    page_templates = {
        'sections.py': """
import streamlit as st
from documentation import load_markdown_content
st.markdown(load_markdown_content('docs/sections.md'))
""",
        'data_explorer.py': """
import streamlit as st
from documentation import load_markdown_content
st.markdown(load_markdown_content('docs/data_explorer.md'))
""",
        'trends.py': """
import streamlit as st
from documentation import load_markdown_content
st.markdown(load_markdown_content('docs/trends.md'))
""",
        'user_guides.py': """
import streamlit as st
from documentation import load_markdown_content
st.markdown(load_markdown_content('docs/user_guides.md'))
""",
        'help.py': """
import streamlit as st
from documentation import load_markdown_content
st.markdown(load_markdown_content('docs/help.md'))
"""
    }

    # Create the pages
    for filename, content in page_templates.items():
        page_path = pages_dir / filename
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f"Created {page_path}")


if __name__ == "__main__":
    setup_streamlit_pages()
