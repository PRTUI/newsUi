import streamlit as st
import sqlite3
import pandas as pd

# Set default layout and title
st.set_page_config(page_title="12OAD Live")

# Styling: Dark mode + professional fonts
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

# Heading
st.markdown("**12OAD Status**")

# DB file path
db_path = "status_feed.db"

# Function to render entries for a tab
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

# Tabs
tabs = st.tabs(["Live Updates", "Leaves", "Upgrade", "➕ Add Entry"])

# --- Tab 1: Live Updates ---
with tabs[0]:
    st.subheader("Live Updates")
    render_timeline("live")

# --- Tab 2: Leaves ---
with tabs[1]:
    st.subheader("Leaves")
    render_timeline("leaves")

# --- Tab 3: Upgrade ---
with tabs[2]:
    st.subheader("Upgrade")
    render_timeline("upgrade")

# --- Tab 4: Add Entry ---
with tabs[3]:
    st.subheader("Add New Entry to Timeline")

    with st.form("add_entry_form"):
        tab_choice = st.selectbox("Select Tab", ["live", "leaves", "upgrade"])
        log_date = st.date_input("Date")
        log_time = st.text_input("Time (e.g., 14:30 hrs)")
        red_text = st.text_area("Red Text (leave blank if not applicable)")
        normal_text = st.text_area("Normal Text (leave blank if not applicable)")
        submitted = st.form_submit_button("Submit")

        if submitted:
            if not log_time or (not red_text and not normal_text):
                st.warning("Please provide at least time and one message (red or normal).")
            else:
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO status_log (tab, log_date, log_time, red_text, normal_text)
                        VALUES (?, ?, ?, ?, ?)
                    """, (tab_choice, log_date.isoformat(), log_time, red_text.strip(), normal_text.strip()))
                    conn.commit()
                    conn.close()
                    st.success("✅ Entry added successfully!")
                except Exception as e:
                    st.error(f"❌ Failed to add entry: {e}")
