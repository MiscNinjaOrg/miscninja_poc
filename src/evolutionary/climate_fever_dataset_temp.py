import os
import torch
import pandas as pd
from skimage import io, transform
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import json
from transformers import AutoTokenizer, BertModel
import tqdm
import torch.nn as nn
import math

# custom dataset class to load our data

class OurDataset(Dataset):
    def __init__(self, data_file, labels_file):
        self.full_data = json.load(open(data_file))
        self.labels = torch.load(labels_file)

        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.model = BertModel.from_pretrained("bert-base-uncased")
        
    def __len__(self):
        return len(self.full_data) 
    
    def __getitem__(self, idx):
        inputs = self.tokenizer(self.full_data[idx], return_tensors="pt")
        outputs = self.model(**inputs)
        last_hidden_states = outputs.last_hidden_state
        return last_hidden_states, self.labels[idx]