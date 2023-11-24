import streamlit as st
from stqdm import stqdm
from utils.models_dict import llm_models_dict
from huggingface_hub import try_to_load_from_cache, _CACHED_NO_EXIST, snapshot_download

st.markdown(
    """
    # Model Shop
    ##### Welcome to the Model Shop! Download a Model you like and start Chatting.
    -------------

""")

models_list = list(llm_models_dict.keys())

for model_name in models_list:
    variants = llm_models_dict[model_name]['variants']
    model_cached = True
    for variant in variants:
        model_path = try_to_load_from_cache(llm_models_dict[model_name]["repo_name"], variant)
        model_cached = model_cached and (model_path is not None) and (model_path is not _CACHED_NO_EXIST)
    if model_cached:
        model_current_state = "Downloaded"
    else:
        model_current_state = "Not Downloaded"
    with st.expander(model_name + " ({})".format(model_current_state)):
        st.markdown("{}".format(model_name))
        if model_current_state == "Downloaded":
            left, right = st.columns([0.5, 0.5])
            with left:
                hf = st.link_button("View on HuggingFace", "https://huggingface.co/" + llm_models_dict[model_name]["repo_name"], use_container_width=True)
            with right:
                button = st.button("Delete", key=model_name, type="primary", use_container_width=True)
        elif model_current_state == "Not Downloaded":
            left, right = st.columns([0.5, 0.5])
            with left:
                hf = st.link_button("View on HuggingFace", "https://huggingface.co/" + llm_models_dict[model_name]["repo_name"], use_container_width=True)
            with right:
                button = st.button("Download", key=model_name, type="primary", use_container_width=True)
                if button:
                    snapshot_download(llm_models_dict[model_name]["repo_name"], tqdm_class=stqdm)