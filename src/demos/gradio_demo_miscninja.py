# miscninja

import gradio as gr
import string
import random
from PIL import Image
from store import Store
from embedder import CLIPEmbedder

def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

tablename = randomword(16)
store = None

def build_vector_db(image_dir, progress=gr.Progress()):

    global tablename
    global store
    tablename = randomword(16)
    store = Store(name=tablename)
    c = CLIPEmbedder()

    i = 0
    for d in progress.tqdm(image_dir, desc="Building"):
        if ("jpg" not in d.name) and ("png" not in d.name):
            continue
        image = Image.open(d.name)
        emb = c.embed(images=[image]).detach().numpy()
        store.insert([i], emb, [d.name], datatype="image")
        i += 1
        
    return "Vector DB Ready"

def search_query(query):
    
    c = CLIPEmbedder()
    text_embed = c.embed(text=[query]).detach().squeeze()
    image = random.choice(store.get_pil_images(store.query([text_embed.numpy()], 3))[0])
    return image

with gr.Blocks() as interface:
    image_dir = gr.File(file_count="directory",label="Input Files", height=200)
    upload = gr.Button(value="Build Vector DB")
    outtext = gr.Textbox()
    upload.click(fn=build_vector_db, inputs=image_dir, outputs=outtext)
    query = gr.Textbox(placeholder="Text Query Here")
    search = gr.Button(value="Search")
    image = gr.Image()
    search.click(fn=search_query, inputs=query, outputs=image)

interface.queue().launch()