import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Page Setup
st.set_page_config(page_title="Team Status Tracker", layout="wide")
st.title("🕒 Real-Time Resource Monitor")

# 2. Connect to your Google Sheet
# (You will provide the URL in the configuration later)
conn = st.connection("gsheets", type=GSheetsConnection)

# --- SIDEBAR: AGENT ACTIONS ---
with st.sidebar:
    st.header("Agent Portal")
    name = st.text_input("Enter Your Name", placeholder="e.g. John Doe")
    
    st.write("Update your status:")
    col1, col2 = st.columns(2)
    
    if name:
        if col1.button("🟢 Login"):
            new_row = pd.DataFrame([{"Timestamp": datetime.now(), "Name": name, "Status": "Logged In"}])
            conn.create(data=new_row)
            st.success("Logged In!")

        if col2.button("🟠 Break"):
            new_row = pd.DataFrame([{"Timestamp": datetime.now(), "Name": name, "Status": "On Break"}])
            conn.create(data=new_row)
            st.warning("On Break")

        if st.button("🔴 Logout", use_container_width=True):
            new_row = pd.DataFrame([{"Timestamp": datetime.now(), "Name": name, "Status": "Logged Out"}])
            conn.create(data=new_row)
            st.error("Logged Out")

# --- MAIN PAGE: SUPERVISOR DASHBOARD ---
st.subheader("Live Status Board")

# Load data from Google Sheets
df = conn.read()

if not df.empty:
    # Logic: Get the latest entry for each person
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    latest_updates = df.sort_values('Timestamp').groupby('Name').tail(1)
    
    # Visual Styling
    def color_status(val):
        color = 'green' if val == 'Logged In' else 'orange' if val == 'On Break' else 'red'
        return f'background-color: {color}; color: white; font-weight: bold'

    st.table(latest_updates.style.applymap(color_status, subset=['Status']))
else:
    st.info("No data yet. Agents need to check in!")

# Auto-refresh button (Streamlit can also auto-refresh every XX seconds)
if st.button('🔄 Refresh Dashboard'):
    st.rerun()