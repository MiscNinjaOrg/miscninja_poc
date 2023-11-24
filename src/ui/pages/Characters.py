import streamlit as st
import json

st.markdown(
    """
    # Characters
    ##### Customize Characters and have fun
    -------------
""")

characters_dict = json.load(open("utils/characters.json"))
characters = list(characters_dict.keys())

with st.sidebar:
    st.markdown("Update a Character:")
    pick_character = st.selectbox("Character", options=characters)

    st.markdown(
        """
        -----------
        Create a New Character:
    """)

    name = st.text_input("New Character Name")
    def on_click(characters_dict, name):
        if name == "":
            return
        f = open("utils/characters.json", "w")
        characters_dict[name] = ""
        f.write(json.dumps(characters_dict))
        f.close()
    button = st.button("Create Character", type="primary", on_click=on_click, args=[characters_dict, name])

    st.markdown(
        """
        -----------
        Delete a Character:
    """)
    
    delete_character = st.selectbox("Delete Character", options=characters)
    def on_click(characters_dict, name):
        if name == "":
            return
        f = open("utils/characters.json", "w")
        del characters_dict[name]
        f.write(json.dumps(characters_dict))
        f.close()
    button = st.button("Delete Character", type="primary", on_click=on_click, args=[characters_dict, delete_character])
 

st.markdown("## System Prompt for {}".format(pick_character))

with st.form("Character Update"):
    text = st.text_area("Describe your Character here", value=characters_dict[pick_character])
    submit = st.form_submit_button("Update Character", type="primary")
    if submit:
        f = open("utils/characters.json", "w")
        characters_dict[pick_character] = text
        f.write(json.dumps(characters_dict))
        f.close()
