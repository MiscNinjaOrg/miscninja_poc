from .base import Database
import sqlite3

class SQLiteImagestore(Database):
    def __init__(self, name, path=None, persistent=False):
        self.name = name
        if persistent:
            assert path is not None
            self.con = sqlite3.connect(os.path.join(path, "temp.db"))
        else:
            self.con = sqlite3.connect(":memory:")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE {}(id INT NOT NULL PRIMARY KEY, img_url TEXT NOT NULL)".format(self.name + "_imagestore"))
        
    def insert(self, ids, items):
        data = list(zip(ids, items))
        self.cur.executemany("INSERT INTO {} VALUES (?, ?)".format(self.name + "_imagestore"), data)
        self.con.commit()
        
    def delete(self, ids):
        self.cur.executemany("DELETE FROM {} WHERE ids = ?".format(self.name + "_imagestore"), ids)
        self.con.commit()
        
    def query(self, ids):
        out = {"ids": [], "images": []}
        for i in range(len(ids)):
            res_images = self.cur.execute('SELECT img_url FROM {} WHERE id IN ({})'.format(self.name + "_imagestore", ', '.join('?' for _ in ids[i])), ids[i]).fetchall()
            out['ids'].append(ids[i])
            out['images'].append(res_images)
        return out
    
    def __del__(self):
        self.con.close()