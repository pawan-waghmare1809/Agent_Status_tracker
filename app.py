import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Team Tracker", layout="wide")

# Connect to Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()
except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()

st.title("🕒 Resource Status Monitor")

# Agent Input
with st.sidebar:
    name = st.text_input("Agent Name")
    status = st.selectbox("Action", ["Logged In", "On Break", "Logged Out"])
    if st.button("Update Status"):
        new_data = pd.DataFrame([{"Timestamp": datetime.now(), "Name": name, "Status": status}])
        updated_df = pd.concat([df, new_data], ignore_index=True)
        conn.update(data=updated_df)
        st.success("Status Updated!")
        st.rerun()

# Dashboard View
st.subheader("Live Dashboard")
if not df.empty:
    # Get latest status per person
    latest = df.sort_values("Timestamp").groupby("Name").tail(1)
    st.dataframe(latest, use_container_width=True)