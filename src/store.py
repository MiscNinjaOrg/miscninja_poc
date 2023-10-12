# Core Vector Store, Embedded Instance

import sqlite3
import os
import hnswlib
import json
from PIL import Image

class Store:
    def __init__(self, name, path=None, persistent=False, max_elements=100000):
        self.name = name
        if persistent:
            assert path is not None
            self.con = sqlite3.connect(os.path.join(path, "temp.db"))
        else:
            self.con = sqlite3.connect(":memory:")
            
            
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE {}(id INT NOT NULL PRIMARY KEY, img_url TEXT NOT NULL)".format(self.name + "_imagestore"))
        self.cur.execute("CREATE TABLE {}(id INT NOT NULL PRIMARY KEY, text TEXT NOT NULL)".format(self.name + "_textstore"))
        self.max_elements = max_elements
        self.dim = None
        self.idx = None
        
    def insert(self, ids, embeddings, items, datatype):
        
        assert datatype in ["image", "text"]
        
        # if first insertion, set dim and construct index
        if self.dim == None:
            self.dim = embeddings.squeeze().shape[-1]
        if self.idx == None:
            self.idx = hnswlib.Index(space='l2', dim=self.dim)
            self.idx.init_index(max_elements=self.max_elements, ef_construction=20, M=100)
            self.idx.set_ef(60)
        
        # add embeddings to index
        self.idx.add_items(embeddings, ids)
        
        # add to sqlite store
        data = list(zip(ids, items))
        if datatype == "image":
            self.cur.executemany("INSERT INTO {} VALUES (?, ?)".format(self.name + "_imagestore"), data)
        elif datatype == "text":
            self.cur.executemany("INSERT INTO {} VALUES (?, ?)".format(self.name + "_textstore"), data)
            
        self.con.commit()
    
    def delete(self, ids):
        self.cur.executemany("DELETE FROM {} WHERE ids = ?".format(self.name + "_imagestore"), ids)
        self.con.commit()
        self.cur.executemany("DELETE FROM {} WHERE ids = ?".format(self.name + "_textstore"), ids)
        self.con.commit()
    
    def query(self, queries, n_results_per_query):
        
        # get ids from hnsw index
        ids, distances = self.idx.knn_query(queries, k=n_results_per_query)
        ids = ids.tolist()
        
        #get objects from stores
        out = {"ids": [], "images": [], "text": []}
        for i in range(len(queries)):
            res_images = self.cur.execute('SELECT img_url FROM {} WHERE id IN ({})'.format(self.name + "_imagestore", ', '.join('?' for _ in ids[i])), ids[i]).fetchall()
            res_text = self.cur.execute('SELECT text FROM {} WHERE id IN ({})'.format(self.name + "_textstore", ', '.join('?' for _ in ids[i])), ids[i]).fetchall()
            self.con.commit()
            out['ids'].append(ids[i])
            out['images'].append(res_images)
            out['text'].append(res_text)
        
        return out
    
    def get_pil_images(self, query_result):
        impaths = query_result['images']
        out = []
        for query_idx in range(len(impaths)):
            current_out = []
            current_query = impaths[query_idx]
            for img_idx in range(len(current_query)):
                current_impath = current_query[img_idx][0]
                current_out.append(Image.open(current_impath))
            out.append(current_out)
        return out
    
    def __del__(self):
        self.con.close()