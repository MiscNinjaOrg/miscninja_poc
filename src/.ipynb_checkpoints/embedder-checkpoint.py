# Embedder Providers

from transformers import CLIPProcessor, CLIPModel, AutoTokenizer, CLIPTextModelWithProjection, AutoProcessor, CLIPVisionModelWithProjection
from PIL import Image

class CLIPEmbedder:
    def __init__(self, model_name="openai/clip-vit-base-patch32", processor_name="openai/clip-vit-base-patch32"):
        self.model_name = model_name
        self.processor_name = processor_name
        
    def __call__(self, text=None, images=None):
        
        if images is not None:
            for i in range(len(images)):
                if type(images[i]) == str:
                    images[i] = Image.open(images[i])
        
        if images is None and text is None:
            return
        
        if images is not None and text is None:
            model = CLIPVisionModelWithProjection.from_pretrained(self.model_name)
            processor = AutoProcessor.from_pretrained(self.processor_name)
            inputs = processor(images=images, return_tensors="pt", padding=True)
            outputs = model(**inputs)
            return outputs.image_embeds
        
        if images is None and text is not None:
            model = CLIPTextModelWithProjection.from_pretrained(self.model_name)
            tokenizer = AutoTokenizer.from_pretrained(self.processor_name)
            inputs = tokenizer(text=text, return_tensors="pt", padding=True)
            outputs = model(**inputs)
            return outputs.text_embeds
        
        if images is not None and text is not None:
            model = CLIPModel.from_pretrained(self.model_name)
            processor = CLIPProcessor.from_pretrained(self.processor_name)
            inputs = processor(text=text, images=images, return_tensors="pt", padding=True)
            outputs = model(**inputs)
            return (outputs.text_embeds, outputs.image_embeds)
    
    def embed(self, text=None, images=None):
        return self.__call__(text, images)