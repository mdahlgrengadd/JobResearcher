import streamlit as st
from documentation import load_markdown_content
st.markdown(load_markdown_content('docs/sections.md'))
