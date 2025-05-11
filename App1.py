import streamlit as st
import sqlite3
import pandas as pd

# Page Setup
st.set_page_config(layout="wide")
st.markdown("**12OAD Status**")

# Tabs
tabs = st.tabs(["Live Updates", "Leaves", "Upgrade"])

# --- Live Updates Tab ---
with tabs[0]:
    #st.subheader("Live Updates")
    products = [
        {"desc": "10MHz, Quad, Precision Op Amp"},
        {"desc": "30V Input, 1A Output, Synchronous Buck Regulator"},
        {"desc": "ATA6560"},
        {"desc": "MIC4605 Half-Bridge Driver"},
    ]
    for product in products:
        with st.container():
            st.markdown(product["desc"])
            st.markdown("---")

# --- Leaves Tab ---
with tabs[1]:
    st.subheader("Leaves")

    try:
        # Connect to SQLite DB
        conn = sqlite3.connect("leaves.db")
        df = pd.read_sql_query("SELECT * FROM leaves_log ORDER BY log_date DESC, log_time DESC", conn)

        current_date = None
        for _, row in df.iterrows():
            if row['log_date'] != current_date:
                current_date = row['log_date']
                st.markdown(
                    f"<div style='margin-top:20px; font-weight:bold; background:white; color:black; padding:5px; width:fit-content;'>{current_date}</div>",
                    unsafe_allow_html=True
                )

            if row['red_text']:
                st.markdown(
                    f"""
                    <div style="background-color:#D32F2F; color:white; padding:10px; margin-bottom:5px;">
                        <b>{row['log_time']}</b><br>{row['red_text']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style="background-color:#111; color:white; padding:10px; margin-bottom:5px;">
                        <b>{row['log_time']}</b><br>{row['normal_text']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        conn.close()

    except Exception as e:
        st.error("⚠️ SQLite database `leaves.db` is missing or cannot be loaded.")

# --- Upgrade Tab ---
with tabs[2]:
    st.subheader("Upgrade")
    st.write("Access premium folders, features, and analytics.")

