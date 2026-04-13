import streamlit as st
from streamlit_gsheets import GSheetsConnection

def fetch_data(sheet_url, ttl):
    conn = st.connection("gsheets", type=GSheetsConnection)
    raw_df = conn.read(spreadsheet=sheet_url, ttl=ttl)
    raw_df = raw_df.dropna(how="all")
    return raw_df