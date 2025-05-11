import streamlit as st
import pandas as pd

# Sample timeline data
timeline_data = [
    {"time": "1:10 hrs", "headline": "J&K CM Omar Abdullah holds interaction with civil society members in Jammu after drone attacks"},
    {"time": "0:38 hrs", "headline": "China condemns Pahalgam terror attack, says 'Peace & stability in Asia is hard-won'"},
    {"date": "10th May 2025"},
    {"time": "23:55 hrs", "headline": "Indian Army sentry injured in firing exchange with unidentified person in J&K’s Nagrota"},
    {"time": "23:23 hrs", "headline": "Pak violated ceasefire in last few hours, India giving reply: Govt", "highlight": True},
    {"time": "23:05 hrs", "headline": "Union Home Secretary holds meeting with Chief Secretaries of states bordering Pakistan after ceasefire violations"},
    {"time": "23:01 hrs", "headline": "Army giving appropriate response to ceasefire violations by Pakistan: India"},
]

st.set_page_config(layout="wide")
st.markdown("### 🪖 Operation Sindoor")
st.markdown("#### India avenges Pahalgam attack")
st.markdown("*How did events unfold today*")

# Timeline display
for event in timeline_data:
    if "date" in event:
        st.markdown(f"<div style='padding:6px 0;font-weight:bold;font-size:16px;background:#fff;color:#000;border-radius:4px;width:fit-content;'>{event['date']}</div>", unsafe_allow_html=True)
    else:
        time_html = f"<span style='color:gray;font-weight:bold;width:80px;display:inline-block;'>{event['time']}</span>"
        headline_color = "white"
        bg_color = "#b30000" if event.get("highlight") else "transparent"
        headline_html = f"<div style='background:{bg_color};padding:10px 15px;border-radius:6px;margin:6px 0;'>{time_html} {event['headline']}</div>"
        st.markdown(headline_html, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("🔗 More at [News18](https://www.news18.com)")
