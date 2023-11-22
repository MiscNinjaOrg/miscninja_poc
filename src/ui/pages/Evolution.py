import streamlit as st
from evolutionary.evoprompting import EvoPrompting
import os

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="api_key", type="password")
    "[View the source code](https://github.com/MiscNinjaOrg/miscninja)"
    "[Read the paper](https://arxiv.org/abs/2302.14838)"

st.markdown(
    """
    # EvoPrompting
    ##### Upload some seed code files and watch an LLM evolve new models for you!
    ---------------
""")

input_page = True
evolving = False
output_page = False

if input_page:
    uploaded_files = st.file_uploader("Upload seed files", type=("txt", "py"), accept_multiple_files=True)
    uploaded_prepend = False
    need_prepend = st.toggle("Prepend Static Code")
    if need_prepend:
        uploaded_prepend = st.file_uploader("Upload prepend (static) code (optional)", type=("txt", "py"), accept_multiple_files=False)
    if need_prepend:
        evolve = st.button("Evolve", type="primary", disabled=not (uploaded_files and uploaded_prepend and openai_api_key))
        input_page = not (uploaded_files and evolve and uploaded_prepend and openai_api_key)
        evolving = uploaded_files and evolve and uploaded_prepend and openai_api_key 
    else:
        evolve = st.button("Evolve", type="primary", disabled=not (uploaded_files and openai_api_key))
        input_page = not (uploaded_files and evolve and openai_api_key)
        evolving = uploaded_files and evolve and openai_api_key

population = None

if evolving:
    seed_files = [f.read().decode() for f in uploaded_files]
    prepend_file = ""
    if uploaded_prepend:
        prepend_file = uploaded_prepend.read().decode()
    data_dir = os.path.join(os.getcwd(), "evolutionary/data")
    with st.spinner('Evolving New Models...'):

        evo = EvoPrompting(openai_api_key, 3, 3, 3, seed_files, prepend_file, data_dir, 20000000)
        population = evo.evolve()
    output_page = True
    input_page = False
    evolving = False

if output_page:
    tabs = st.tabs(["Model " + str(i+1) for i in range(len(population))])
    for i, tab in enumerate(tabs):
        with tab:
            st.subheader("Model Score: " + str(population[i][-1]))
            st.subheader("Code:")
            st.code(population[i][0], "python", line_numbers=True)
