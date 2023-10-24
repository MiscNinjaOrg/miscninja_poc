from .base import Index
import hnswlib

class HNSW(Index):
    def __init__(self, dim, max_elements=100000):
        self.idx = hnswlib.Index(space='l2', dim=dim)
        self.idx.init_index(max_elements=max_elements, ef_construction=20, M=100)
        self.idx.set_ef(60)
        
    def insert(self, embeddings, ids):
        self.idx.add_items(embeddings, ids)
    
    def query(self, queries, n_results_per_query=2):
        ids, distances = self.idx.knn_query(queries, k=n_results_per_query)
        ids = ids.tolist()
        return ids
    
    def delete(self, id_):
        self.idx.mark_deleted(id)