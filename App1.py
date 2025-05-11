import streamlit as st
import sqlite3
from datetime import datetime
from pytz import timezone

st.set_page_config(page_title="12OAD Status")
st.markdown("### Related Products by Industry → **12OAD Status**")

# DB path
db_path = "status_feed_v2.db"

# --- CSS Styling ---
st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }
        .log-entry {
            background-color: #1e1e1e;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 10px;
            font-size: 15px;
        }
        .log-red {
            background-color: #D32F2F !important;
        }
        .log-normal {
            background-color: #1e1e1e !important;
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
        .author-row {
            font-size: 12px;
            color: #ccc;
            margin-top: 6px;
            display: flex;
            justify-content: space-between;
        }
        .reaction-row {
            font-size: 18px;
            margin-top: 6px;
        }
    </style>
""", unsafe_allow_html=True)

# --- DB functions ---
def get_reactions(message_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT emoji, COUNT(*) FROM reactions WHERE message_id = ? GROUP BY emoji", (message_id,))
    data = cursor.fetchall()
    conn.close()
    return data

def add_reaction(message_id, emoji):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reactions (message_id, emoji) VALUES (?, ?)", (message_id, emoji))
    conn.commit()
    conn.close()
    st.experimental_rerun()

def delete_entry(message_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reactions WHERE message_id = ?", (message_id,))
    cursor.execute("DELETE FROM status_log WHERE id = ?", (message_id,))
    conn.commit()
    conn.close()
    st.success("✅ Deleted successfully.")
    st.experimental_rerun()

def render_timeline(tab_key):
    conn = sqlite3.connect(db_path)
    df = conn.execute(
        f"SELECT * FROM status_log WHERE tab = ? ORDER BY log_date DESC, log_time DESC, id DESC", (tab_key,)
    ).fetchall()
    conn.close()

    current_date = None
    for row in df:
        message_id, tab, log_date, log_time, red_text, normal_text, name = row
        message = red_text if red_text else normal_text
        style_class = "log-red" if red_text else "log-normal"

        if log_date != current_date:
            current_date = log_date
            st.markdown(f"<div class='log-date'>{log_date}</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='log-entry {style_class}'>", unsafe_allow_html=True)
        st.markdown(f"<b>{log_time}:</b> {message}", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([0.75, 0.10, 0.15])
        with col1:
            st.markdown(f"<div class='author-row'><span>{name}</span></div>", unsafe_allow_html=True)
        with col2:
            with st.expander("➕", expanded=False):
                emoji = st.selectbox(
                    "", ["👍", "❤️", "😂", "🎉", "🔥", "🚀", "👏", "✅", "❗", "🧠", "🙏", "🤘"], key=f"emoji_{message_id}"
                )
                state_key = f"reacted_{message_id}_{emoji}"
                if not st.session_state.get(state_key):
                    if st.button("React", key=f"react_btn_{message_id}_{emoji}"):
                        add_reaction(message_id, emoji)
                        st.session_state[state_key] = True
                else:
                    st.caption("✅ Already reacted.")
        with col3:
            if st.button("✖", key=f"del_{message_id}"):
                delete_entry(message_id)

        reactions = get_reactions(message_id)
        if reactions:
            row = " ".join([f"{emoji} × {count}" for emoji, count in reactions])
            st.markdown(f"<div class='reaction-row'>{row}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# --- Tabs ---
tabs = st.tabs(["Live Updates", "Leaves", "Upgrade", "➕ Add Entry"])

with tabs[0]:
    st.subheader("Live Updates")
    render_timeline("live")

with tabs[1]:
    st.subheader("Leaves")
    render_timeline("leaves")

with tabs[2]:
    st.subheader("Upgrade")
    render_timeline("upgrade")

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
                india_time = datetime.now(timezone("Asia/Kolkata"))
                log_date = india_time.strftime('%Y-%m-%d')
                log_time = india_time.strftime('%H:%M hrs')
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
