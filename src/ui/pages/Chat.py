import streamlit as st
from llms.openai import GPT_3_5
from llms.llama import LLAMA
from utils.models_dict import llm_models_dict
from huggingface_hub import try_to_load_from_cache, _CACHED_NO_EXIST
from wonderwords import RandomWord
import json

st.markdown(
    """
    # Just Chat
    ##### 👈 Pick a Model and a Character to talk to.
    -------------
""")

if "conversations" not in st.session_state:
    st.session_state.conversations = {}

models = ["GPT-3.5", "GPT-4.0"] + list(llm_models_dict.keys())
characters_dict = json.load(open("utils/characters.json"))
characters = list(characters_dict.keys())
conversations = list(st.session_state.conversations.keys())[::-1]

with st.sidebar:
    pick_model = st.selectbox("Model", options=models)
    pick_character = st.selectbox("Character", options=characters)
    pick_conversation = st.selectbox("Conversation", options=conversations)
    new_conversation = st.button("New Conversation", type="primary")
    if pick_model in ["GPT-3.5", "GPT-4.0"]:
        openai_api_key = st.text_input("OpenAI API Key", key="api_key", type="password")
    else:
        pick_variant = st.selectbox("Variant", options=llm_models_dict[pick_model]["variants"])
        pick_context_length = st.slider("Context Length", min_value=512, max_value=2048, value=512)

if pick_model == "GPT-3.5":
    model = GPT_3_5(openai_api_key)
elif pick_model == "GPT-4.0":
    pass
else:
    model_path = try_to_load_from_cache(llm_models_dict[pick_model]["repo_name"], pick_variant)
    if model_path is _CACHED_NO_EXIST or model_path is None:
        st.error("You don't have this model downloaded. Head over to the Model Shop and download it first.")
        st.stop()
    else:
        model = LLAMA(model_path=model_path, context_length=pick_context_length, chat_format=llm_models_dict[pick_model]["chat_format"])

conversation_name = pick_conversation
if new_conversation:
    r = RandomWord()
    conversation_name = r.word(include_parts_of_speech=["adjectives"]) + " " + r.word(include_parts_of_speech=["noun"])
    prompt = [{"role": "system", "content": characters_dict[pick_character]}]
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