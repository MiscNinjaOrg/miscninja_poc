from .base import Embedder
from transformers import CLIPProcessor, CLIPModel, AutoTokenizer, CLIPTextModelWithProjection, AutoProcessor, CLIPVisionModelWithProjection
from PIL import Image

class CLIPEmbedder(Embedder):
    def __init__(self, model_name="openai/clip-vit-base-patch32", processor_name="openai/clip-vit-base-patch32"):
        self.model_name = model_name
        self.processor_name = processor_name
        
    def __call__(self, text=None, images=None):
        
        image_inputs = []
        text_inputs = [""]
        
        if images is None and text is None:
            return
        
        if images is not None:
            for i in range(len(images)):
                if type(images[i]) == str:
                    images[i] = Image.open(images[i])
            image_inputs = images
        
        if text is not None:
            text_inputs = text
        
        model = CLIPModel.from_pretrained(self.model_name)
        processor = CLIPProcessor.from_pretrained(self.processor_name)
        inputs = processor(text=text_inputs, images=image_inputs, return_tensors="pt", padding=True)
        outputs = model(**inputs)
        
        if images is not None and text is None:
            return outputs.image_embeds
        if images is None and text is not None:
            return outputs.text_embeds
        if images is not None and text is not None:
            return (outputs.text_embeds, outputs.image_embeds)
    
    def embed(self, text=None, images=None):
        return self.__call__(text, images)