import streamlit as st
from llms.openai import GPT_3_5
from llms.llama import LLAMA
from huggingface_hub import try_to_load_from_cache
from wonderwords import RandomWord

st.markdown(
    """
    # Just Chat
    ##### 👈 Pick a Model and a Character to talk to.
    -------------
""")

if "conversations" not in st.session_state:
    st.session_state.conversations = {}

models = ["GPT-3.5", "GPT-4.0", "Mistral-7B", "Mistral-7B Instruct"]
characters = ["Base", "Accelerationist"]
conversations = list(st.session_state.conversations.keys())[::-1]

with st.sidebar:
    pick_model = st.selectbox("Model", options=models)
    pick_character = st.selectbox("Character", options=characters)
    pick_conversation = st.selectbox("Conversation", options=conversations)
    new_conversation = st.button("New Conversation", type="primary")
    if pick_model in ["GPT-3.5", "GPT-4.0"]:
        openai_api_key = st.text_input("OpenAI API Key", key="api_key", type="password")

if pick_model == "GPT-3.5":
    model = GPT_3_5(openai_api_key)
if pick_model == "Mistral-7B":
    model = LLAMA(try_to_load_from_cache("TheBloke/Mistral-7B-v0.1-GGUF", "mistral-7b-v0.1.Q4_K_M.gguf"), chat_format="mistrallite")
if pick_model == "Mistral-7B Instruct":
    model = LLAMA(try_to_load_from_cache("TheBloke/Mistral-7B-v0.1-GGUF", "mistral-7b-v0.1.Q4_K_M.gguf"), chat_format="llama-2")

conversation_name = pick_conversation
if new_conversation:
    r = RandomWord()
    conversation_name = r.word(include_parts_of_speech=["adjectives"]) + " " + r.word(include_parts_of_speech=["noun"])
    prompt = [{"role": "system", "content": "You are a intelligent assistant."}]
    st.session_state.conversations[conversation_name] = prompt
    st.rerun()

if conversation_name:
    for message in st.session_state.conversations[conversation_name]:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

if prompt_input := st.chat_input("Just Chat"):
    st.session_state.conversations[conversation_name].append({"role": "user", "content": prompt_input})

    with st.chat_message("user"):
        st.markdown(prompt_input)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for reply in model.stream(st.session_state.conversations[conversation_name]):
            full_response += reply
            message_placeholder.markdown(full_response + " |")
        message_placeholder.markdown(full_response)
    st.session_state.conversations[conversation_name].append({"role": "assistant", "content": full_response})