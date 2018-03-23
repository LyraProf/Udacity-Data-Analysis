# -*- coding: utf-8 -*-

"""
由csv文件生成数据库
http://www.runoob.com/sqlite/sqlite-python.html
"""

import csv, sqlite3

con = sqlite3.connect("Houston_1.db")
con.text_factory = str     # 把字符串入库之前转成unicode string，参考https://www.cnblogs.com/lightwind/p/4499193.html
cur = con.cursor()


# nodes
cur.execute("CREATE TABLE nodes (id, lat, lon, user, uid, version, changeset, timestamp);")
with open('nodes.csv','rb') as f:
    dr = csv.DictReader(f) 
    for line in dr:
        rec = [line['id'], line['lat'], line['lon'], line['user'], line['uid'], \
               line['version'], line['changeset'], line['timestamp']]
        cur.execute("INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);", rec)   
con.commit()


# nodes_tags
cur.execute("CREATE TABLE nodes_tags (id, key, value, type);")
with open('nodes_tags.csv','rb') as f:
    dr = csv.DictReader(f) 
    for line in dr:
        rec = [line['id'], line['key'], line['value'], line['type']]
        cur.execute("INSERT INTO nodes_tags (id, key, value, type) VALUES (?, ?, ?, ?);", rec)

con.commit()


# ways 
cur.execute("CREATE TABLE ways (id, user, uid, version, changeset, timestamp);")
with open('ways.csv','rb') as f:
    dr = csv.DictReader(f) 
    for line in dr:
        rec = [line['id'], line['user'], line['uid'], line['version'], line['changeset'], line['timestamp']]
        cur.execute("INSERT INTO ways (id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);",\
                    rec)

con.commit()


# ways_nodes 
cur.execute("CREATE TABLE ways_nodes (id, node_id, position);")
with open('ways_nodes.csv','rb') as f:
    dr = csv.DictReader(f) 
    for line in dr:
        rec = [line['id'], line['node_id'], line['position']]
        cur.execute("INSERT INTO ways_nodes (id, node_id, position) VALUES (?, ?, ?);", rec)

con.commit()


# ways_tags
cur.execute("CREATE TABLE ways_tags (id, key, value, type);")
with open('ways_tags.csv','rb') as f:
    dr = csv.DictReader(f) 
    for line in dr:
        rec = [line['id'], line['key'], line['value'], line['type']]
        cur.execute("INSERT INTO ways_tags (id, key, value, type) VALUES (?, ?, ?, ?);", rec)

con.commit()











