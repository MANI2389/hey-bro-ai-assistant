import streamlit as st
from status import get_status
from agent import run_agent

st.set_page_config(page_title="Jarvis AI")

st.title("🤖 Jarvis AI Dashboard")

st.write(run_agent())

if st.button("Check System Status"):

    status = get_status()

    st.write(f"CPU Usage: {status['cpu']} %")
    st.write(f"RAM Usage: {status['ram']} %")