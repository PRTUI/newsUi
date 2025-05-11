import streamlit as st
import sqlite3
import pandas as pd

# Default (narrow) layout, dark mode styling manually applied
st.set_page_config(page_title="12OAD Status")
st.markdown("**12OAD Status**")

# Optional: Force dark theme styling via custom CSS
st.markdown(
    """
    <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        .stMarkdown, .stText {
            color: white;
        }
    </style>
    """, unsafe_allow_html=True
)

# Tabs
tabs = st.tabs(["Live Updates", "Leaves", "Upgrade"])

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
            elif row['normal_text']:
                st.markdown(
                    f"""
                    <div style="background-color:#111; color:white; padding:10px; margin-bottom:5px;">
                        <b>{row['log_time']}</b><br>{row['normal_text']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    except Exception as e:
        st.error("⚠️ Could not load or query `status_feed.db`.")


# Render content for each tab
with tabs[0]: st.subheader("Live Updates"); render_timeline("live")
with tabs[1]: st.subheader("Leaves"); render_timeline("leaves")
with tabs[2]: st.subheader("Upgrade"); render_timeline("upgrade")


