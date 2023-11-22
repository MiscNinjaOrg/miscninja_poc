import streamlit as st
from llms.openai import GPT_3_5

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
    if pick_model in ["GPT-3.5", "GPT-4.0"]:
        openai_api_key = st.text_input("OpenAI API Key", key="api_key", type="password")

if pick_model == "GPT-3.5":
    model = GPT_3_5(openai_api_key)

prompt = [{"role": "system", "content": "You are a intelligent assistant."}]

if prompt_input := st.chat_input("Just Chat"):
    prompt.append({"role": "user", "content": prompt_input})

    with st.chat_message("user"):
        st.markdown(prompt_input)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for reply in model.stream(prompt):
            full_response += reply
            message_placeholder.markdown(full_response + " |")
        message_placeholder.markdown(full_response)