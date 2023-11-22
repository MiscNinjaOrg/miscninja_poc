import streamlit as st
from evolutionary.evoprompting import EvoPrompting
import os

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="api_key", type="password")
    "[View the source code](https://github.com/MiscNinjaOrg/miscninja)"
    "[Read the paper](https://arxiv.org/abs/2302.14838)"

st.title("EvoPrompting")

uploaded_files = st.file_uploader("Upload seed files", type=("txt", "py"), accept_multiple_files=True)
uploaded_prepend = st.file_uploader("Upload prepend (static) code (optional)", type=("txt", "py"), accept_multiple_files=False)
evolve = st.button("Evolve", type="primary", disabled=not (uploaded_files and openai_api_key))

if uploaded_files and evolve:
    seed_files = [f.read().decode() for f in uploaded_files]
    prepend_file = ""
    if uploaded_prepend:
        prepend_file = uploaded_prepend.read().decode()
    data_dir = os.path.join(os.getcwd(), "evolutionary/data")
    evo = EvoPrompting(openai_api_key, 3, 3, 3, seed_files, prepend_file, data_dir, 10000000)