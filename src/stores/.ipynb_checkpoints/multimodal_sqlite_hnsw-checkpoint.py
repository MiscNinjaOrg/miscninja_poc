from .base import Store
from databases.sqlite_image import SQLiteImagestore
from databases.sqlite_text import SQLiteTextstore
from indexes.hnsw import HNSW

class MultimodalSQLiteHNSW(Store):
    def __init__(self, name, dim = None, path=None, persistent=False, max_elements=100000):
        self.image_store = SQLiteImagestore(name, path, persistent)
        self.text_store = SQLiteTextstore(name, path, persistent)
        if dim == None:
            self.idx = None
            self.max_elements = max_elements
        else:
            self.idx = HNSW(dim, max_elements)
            
    def insert(self, ids, embeddings, items, datatype):
        assert datatype in ["image", "text"]
        
        # if first insertion, set dim and construct index
        if self.idx == None:
            self.dim = embeddings.squeeze().shape[-1]
            self.idx = HNSW(dim, self.max_elements)

        self.idx.insert(embeddings, ids)
        if datatype == "text":
            self.text_store.insert(ids, items)
        if datatype == "image":
            self.image_store.insert(ids, items)
            
    def delete(self, ids):
        for id_ in ids:
            self.idx.delete(id_)
        self.image_store.delete(ids)
        self.text_store.delete(ids)
        
    def query(self, queries, n_results_per_query):
        ids = self.idx.query(queries, n_results_per_query)
        image_out = self.image_store.query(ids)
        text_out = self.text_store.query(ids)
        return (image_out, text_out)