import streamlit as st
import pandas as pd
from backend.security import has_role
from backend.i18n import t

st.set_page_config(page_title="Admin Dashboard", page_icon="🛠️", layout="wide")

lang = st.session_state.get("lang", "en")
st.title("🛠️ " + t(lang, "role_admin"))

if "session" not in st.session_state or not has_role(st.session_state.get("session"), "admin"):
    st.error("Admin access only (demo).")
else:
    st.success("Welcome, Admin (demo).")
    try:
        df = pd.read_csv("logs/interactions.csv")
        st.dataframe(df)
    except FileNotFoundError:
        st.info("No interactions logged yet.")