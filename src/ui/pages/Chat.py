import streamlit as st

st.markdown(
    """
    # Just Chat
    ##### 👈 Pick a Model and a Character to talk to.
    -------------
""")

models = ["GPT-3.5", "GPT-4.0"]
characters = ["Base", "Accelerationist"]

with st.sidebar:
    pick_model = st.selectbox("Model", options=models)
    pick_character = st.selectbox("Character", options=characters)