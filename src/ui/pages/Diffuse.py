import streamlit as st
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from utils.models_dict import diffusion_models_dict

st.markdown(
    """
    # Diffuse
    ##### 👈 Pick a Model and start Generating Images
    -------------
""")

models = list(diffusion_models_dict.keys())

with st.sidebar:
    pick_model = st.selectbox("Model", options=models)

pipeline = DiffusionPipeline.from_pretrained(diffusion_models_dict[pick_model], use_safetensors=True)
pipeline.scheduler = DPMSolverMultistepScheduler.from_config(pipeline.scheduler.config)

def on_click(prompt):
    with st.spinner("diffusing..."):
        st.session_state.image = pipeline(prompt, num_inference_steps=25).images[0]

with st.form("diffuse"):
    prompt = st.text_input("What do you want to see?")
    submit = st.form_submit_button("Diffuse", on_click=on_click, args=[prompt], type="primary")

if "image" in st.session_state:
    st.image(st.session_state.image, caption=prompt)