import streamlit as st
import pandas as pd

st.set_page_config(page_title="12oad", layout="centered")
st.markdown("<h2 style='text-align:center;'>📁 12oad</h2>", unsafe_allow_html=True)

folder_names = st.session_state.get("folders", ["Projects", "Leaves"])
with st.sidebar:
    st.markdown("### Folders")
    for folder in folder_names:
        if st.button(folder):
            st.session_state['selected_folder'] = folder
    new_folder = st.text_input("➕ Add Folder")
    if st.button("Create") and new_folder:
        folder_names.append(new_folder)
        st.session_state["folders"] = folder_names

selected_folder = st.session_state.get("selected_folder", "Leaves")
st.markdown(f"<h4 style='color:gray;'>Opened Folder: {selected_folder}</h4>", unsafe_allow_html=True)

if selected_folder == "Leaves":
    uploaded_file = st.file_uploader("Upload 'entry.xlsx'", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)

        if {'Timestamp', 'RedText', 'NormalText'}.issubset(df.columns):
            df['Date'] = pd.to_datetime(df['Timestamp']).dt.strftime('%d %B %Y')
            df['Time'] = pd.to_datetime(df['Timestamp']).dt.strftime('%H:%M')
            grouped = df.groupby('Date')

            for date, group in grouped:
                st.markdown(f"<div style='padding:6px 0;font-weight:bold;font-size:16px;background:#fff;color:#000;border-radius:4px;width:fit-content;margin-top:20px;'>{date}</div>", unsafe_allow_html=True)

                for _, row in group.iterrows():
                    time = row['Time']
                    red_text = str(row['RedText'])
                    normal_text = str(row['NormalText'])

                    st.markdown(f"""
                    <div style='background:#111;padding:12px;border-radius:6px;margin:6px 0;'>
                        <div style='color:red;font-weight:bold'>{time}</div>
                        <div style='color:red;'>{red_text}</div>
                        <div style='color:white;'>{normal_text}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.error("Excel must contain columns: 'Timestamp', 'RedText', and 'NormalText'")
