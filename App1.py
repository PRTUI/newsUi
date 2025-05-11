import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Live")

st.markdown("### Related Products by Industry → **Live**")

# Styling
st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }
        .log-entry {
            padding: 10px;
            margin-bottom: 8px;
            border-radius: 4px;
            font-size: 15px;
            position: relative;
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
        .author {
            font-size: 12px;
            color: #cccccc;
            padding-top: 4px;
        }
    </style>
""", unsafe_allow_html=True)

# DB path
db_path = "status_feed_v2.db"

def render_timeline(tab_key):
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(
            f"SELECT * FROM status_log WHERE tab = '{tab_key}' ORDER BY log_date DESC, log_time DESC, id DESC", conn
        )
        conn.close()

        current_date = None
        for _, row in df.iterrows():
            if row['log_date'] != current_date:
                current_date = row['log_date']
                st.markdown(f"<div class='log-date'>{current_date}</div>", unsafe_allow_html=True)

            message = row['red_text'] or row['normal_text']
            style_class = "log-red" if row['red_text'] else "log-normal"

            col1, col2 = st.columns([0.95, 0.05])
            with col1:
                st.markdown(
                    f"""
                    <div class='log-entry {style_class}'>
                        <b>{row['log_time']}:</b> {message}
                        <div class='author'>{row['name']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with col2:
                if st.button("🗑️", key=f"del_{row['id']}"):
                    delete_entry(row['id'])

    except Exception as e:
        st.error("⚠️ Could not load or query the database.")

def delete_entry(entry_id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM status_log WHERE id = ?", (entry_id,))
        conn.commit()
        conn.close()
        st.experimental_rerun()
    except Exception as e:
        st.error(f"❌ Failed to delete entry: {e}")

# Tabs
tabs = st.tabs(["Live Updates", "Leaves", "Upgrade", "➕ Add Entry"])

with tabs[0]: render_timeline("live")
with tabs[1]: render_timeline("leaves")
with tabs[2]: render_timeline("upgrade")

# Add Entry Form
with tabs[3]:
    st.subheader("Add New Entry")

    with st.form("add_entry_form"):
        tab_choice = st.selectbox("Select Tab", ["live", "leaves", "upgrade"])
        red_text = st.text_area("Red Text (optional)")
        normal_text = st.text_area("Normal Text (optional)")
        name = st.text_input("Name (author)", max_chars=100)
        submitted = st.form_submit_button("Submit")

        if submitted:
            if not name.strip() or (not red_text.strip() and not normal_text.strip()):
                st.warning("Please fill name and at least one message field.")
            else:
                try:
                    now = datetime.now()
                    log_date = now.strftime('%Y-%m-%d')
                    log_time = now.strftime('%H:%M hrs')
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO status_log (tab, log_date, log_time, red_text, normal_text, name)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (tab_choice, log_date, log_time, red_text.strip(), normal_text.strip(), name.strip()))
                    conn.commit()
                    conn.close()
                    st.success("✅ Entry added successfully!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"❌ Failed to add entry: {e}")
