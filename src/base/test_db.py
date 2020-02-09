from mini_db import MiniDBPerItem, MiniDB
#import sqlite3

t_db = MiniDB('test0.db')

item0 = MiniDBPerItem('id', 'VARCHAR(255)', True)
item1 = MiniDBPerItem('name', 'VARCHAR(255)', False)

itl = []
itl.append(item0)
itl.append(item1)

t_db.init_tbl('tbl', itl)

item0.set_val('1')
item1.set_val('cf')

#t_db.insert('tbl', itl)

#t_db.insert('tbl', itl)

item0.set_val('1')
item1.set_val('cdd')

t_db.update('tbl', itl)

lookup_l = [item0]

t_db.lookup('tbl', lookup_l)

t_db.close()