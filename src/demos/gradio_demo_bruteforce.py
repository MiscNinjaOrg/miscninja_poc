# brute force approx nearest neighbor

import gradio as gr
import sqlite3
import time
import string
import random
import json
import math
import torch
from PIL import Image
from transformers import AutoTokenizer, AutoProcessor, CLIPVisionModelWithProjection, CLIPTextModelWithProjection

def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

tablename = randomword(16)

def build_vector_db(image_dir, progress=gr.Progress()):

    global tablename
    tablename = randomword(16)
    con = sqlite3.connect("temp.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE {}(emb text primary key, image text)".format(tablename))

    model = CLIPVisionModelWithProjection.from_pretrained("openai/clip-vit-base-patch32")
    processor = AutoProcessor.from_pretrained("openai/clip-vit-base-patch32")

    for d in progress.tqdm(image_dir, desc="Building"):

        if ("jpg" not in d.name) and ("png" not in d.name):
            continue
        image = Image.open(d.name)
        inputs = processor(images=image, return_tensors="pt")
        outputs = model(**inputs)
        image_embed = outputs.image_embeds.squeeze().tolist()
        image_embed_json = json.dumps(image_embed)
        cur.execute("INSERT INTO {} VALUES(\"{}\", \"{}\")".format(tablename, image_embed_json, d.name))
        con.commit()

    con.close()
    return "Boring DB Ready"

def search_query(query):

    con = sqlite3.connect("temp.db")
    cur = con.cursor()
    
    model = CLIPTextModelWithProjection.from_pretrained("openai/clip-vit-base-patch32")
    tokenizer = AutoTokenizer.from_pretrained("openai/clip-vit-base-patch32")
    inputs = tokenizer([query], return_tensors="pt")
    outputs = model(**inputs)
    text_embed = outputs.text_embeds.squeeze()

    min_image_path = None
    min_dist = math.inf

    for row in cur.execute("SELECT * FROM {}".format(tablename)):
        embedding_json = row[0]
        image_embed = torch.Tensor(json.loads(embedding_json))
        dist = torch.dist(image_embed, text_embed)
        if dist < min_dist:
            min_dist = dist
            min_image_path = row[1]

    image = Image.open(min_image_path)
    con.close()
    return image

with gr.Blocks() as interface:
    image_dir = gr.File(file_count="directory",label="Input Files", height=200)
    upload = gr.Button(value="Build Boring DB")
    outtext = gr.Textbox()
    upload.click(fn=build_vector_db, inputs=image_dir, outputs=outtext)
    query = gr.Textbox(placeholder="Text Query Here")
    search = gr.Button(value="Search")
    image = gr.Image()
    search.click(fn=search_query, inputs=query, outputs=image)

interface.queue().launch()