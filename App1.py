import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from pytz import timezone

# ---------- CONFIG ----------
st.set_page_config(page_title="Status")
st.markdown("### Related Products by Industry → **Status**")

# ---------- STYLE ----------
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

# ---------- DB PATH ----------
db_path = "status_feed_v2.db"

# ---------- RENDER TIMELINE ----------
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

# ---------- DELETE ENTRY ----------
def delete_entry(entry_id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM status_log WHERE id = ?", (entry_id,))
        conn.commit()
        conn.close()
        st.success("🗑️ Entry deleted successfully.")
        st.experimental_rerun()
    except Exception as e:
        st.error(f"❌ Failed to delete entry: {e}")

# ---------- TABS ----------
tabs = st.tabs(["Live Updates", "Leaves", "Upgrade", "➕ Add Entry"])

with tabs[0]: st.subheader("Live Updates"); render_timeline("live")
with tabs[1]: st.subheader("Leaves"); render_timeline("leaves")
with tabs[2]: st.subheader("Upgrade"); render_timeline("upgrade")

# ---------- ADD ENTRY FORM ----------
with tabs[3]:
    st.subheader("Add New Entry")

    with st.form("add_entry_form"):
        tab_choice = st.selectbox("Select Tab", ["live", "leaves", "upgrade"])
        red_text = st.text_area("Red Text (optional)")
        normal_text = st.text_area("Normal Text (optional)")
        emoji = st.selectbox("Pick an Emoji", ["😄", "🔥", "🚀", "👍", "🤘", "💡", "🎉", "❗", "📢", "✅", ""])
        name = st.text_input("Name (author)", max_chars=100)
        submitted = st.form_submit_button("Submit")

        if submitted:
            if not name.strip() or (not red_text.strip() and not normal_text.strip()):
                st.warning("Please fill name and at least one message field.")
            else:
                try:
                    india_time = datetime.now(timezone("Asia/Kolkata"))
                    log_date = india_time.strftime('%Y-%m-%d')
                    log_time = india_time.strftime('%H:%M hrs')

                    # Attach emoji
                    if red_text:
                        red_text = f"{emoji} {red_text.strip()}"
                    if normal_text:
                        normal_text = f"{emoji} {normal_text.strip()}"

                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO status_log (tab, log_date, log_time, red_text, normal_text, name)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (tab_choice, log_date, log_time, red_text, normal_text, name.strip()))
                    conn.commit()
                    conn.close()
                    st.success("✅ Entry added successfully!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"❌ Failed to add entry: {e}")
