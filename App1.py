import streamlit as st
import sqlite3
import pandas as pd

# Default layout with dark mode
st.set_page_config(page_title="12OAD Status")

# Page heading
st.markdown("### Related Products by Industry → **12OAD Status**")

# Tabs
tabs = st.tabs(["Live Updates", "Leaves", "Upgrade"])

# Styling for clean, professional font and layout
st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }
        .log-entry {
            padding: 10px;
            margin-bottom: 6px;
            border-radius: 4px;
            font-size: 15px;
        }
        .log-red {
            background-color: #D32F2F;
            color: white;
        }
        .log-normal {
            background-color: #1e1e1e;
            color: white;
        }
        .log-date {
            background: white;
            color: black;
            padding: 4px 10px;
            font-weight: bold;
            margin-top: 20px;
            width: fit-content;
            border-radius: 3px;
        }
    </style>
""", unsafe_allow_html=True)

# DB path
db_path = "status_feed.db"

def render_timeline(tab_key):
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(
            f"SELECT * FROM status_log WHERE tab = '{tab_key}' ORDER BY log_date DESC, log_time DESC", conn
        )
        conn.close()

        current_date = None
        for _, row in df.iterrows():
            if row['log_date'] != current_date:
                current_date = row['log_date']
                st.markdown(f"<div class='log-date'>{current_date}</div>", unsafe_allow_html=True)

            if row['red_text']:
                st.markdown(
                    f"<div class='log-entry log-red'><b>{row['log_time']}:</b> {row['red_text']}</div>",
                    unsafe_allow_html=True
                )
            elif row['normal_text']:
                st.markdown(
                    f"<div class='log-entry log-normal'><b>{row['log_time']}:</b> {row['normal_text']}</div>",
                    unsafe_allow_html=True
                )

    except Exception as e:
        st.error("⚠️ Could not load or query `status_feed.db`.")


# Render each tab
with tabs[0]: st.subheader("Live Updates"); render_timeline("live")
with tabs[1]: st.subheader("Leaves"); render_timeline("leaves")
with tabs[2]: st.subheader("Upgrade"); render_timeline("upgrade")
