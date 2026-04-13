import streamlit as st

SHEET_URL = st.secrets["dashboard_config"]["sheet_url"]
REFRESH_INTERVAL = 60000 
CACHE_TTL = 50