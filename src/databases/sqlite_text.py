from .base import Database
import sqlite3

class SQLiteTextstore(Database):
    def __init__(self, name, path=None, persistent=False):
        self.name = name
        if persistent:
            assert path is not None
            self.con = sqlite3.connect(os.path.join(path, "temp.db"))
        else:
            self.con = sqlite3.connect(":memory:")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE {}(id INT NOT NULL PRIMARY KEY, text TEXT NOT NULL)".format(self.name + "_textstore"))
        
    def insert(self, ids, items):
        data = list(zip(ids, items))
        self.cur.executemany("INSERT INTO {} VALUES (?, ?)".format(self.name + "_textstore"), data)
        self.con.commit()
        
    def delete(self, ids):
        self.cur.executemany("DELETE FROM {} WHERE ids = ?".format(self.name + "_textstore"), ids)
        self.con.commit()
        
    def query(self, ids):
        out = {"ids": [], "text": []}
        for i in range(len(ids)):
            res_text = self.cur.execute('SELECT text FROM {} WHERE id IN ({})'.format(self.name + "_textstore", ', '.join('?' for _ in ids[i])), ids[i]).fetchall()
            out['ids'].append(ids[i])
            out['text'].append(res_text)
        return out
    
    def __del__(self):
        self.con.close()