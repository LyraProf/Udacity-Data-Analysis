# -*- coding: utf-8 -*-

"""
清理原始数据，生成csv文件，用于建立数据库
只针对标签为'node'和'way'的数据进行清理
"""
  
import csv
import codecs
import re
import xml.etree.cElementTree as ET


def shape_element(element):
    """
    整理XML节点数据，输出为字典格式
    element: 元素
    输出：'node'和'way'的元素字典
    """

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  
    
    # 原始数据各字段
    NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
    WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
    
    # 字符串：字符串，如"addr:housenumber"
    COLON_CHAR = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
                                 
    # 常规字符串，如"building"
    NOR_CHAR = re.compile(r'^[a-zA-Z]+$')

    if element.tag == 'node':   # 'node'节点
        for attrib in element.attrib:
            if attrib in NODE_FIELDS:
                node_attribs[attrib] = element.attrib[attrib]
        
        for child in element:
            node_tag = {}
                
            # 如果tag是包含字母和冒号，如<tag k="addr:housenumber" v="4818"/>，需要解析成
            # {'id': 2050269305, 'key': 'housenumber', 'value': '4818', 'type': 'addr'}
            if COLON_CHAR.match(child.attrib['k']):    
                node_tag['id'] = element.attrib['id']
                node_tag['key'] = child.attrib['k'].split(':')[1]
                node_tag['value'] = child.attrib['v']
                node_tag['type'] = child.attrib['k'].split(':')[0]
                tags.append(node_tag)
                
            # tag常规字符串，如<tag k="building" v="house"/>，需要解析成
            # {'id': 2061901866, 'key': 'building', 'value': 'house', 'type': 'regular'}
            elif NOR_CHAR.match(child.attrib['k']):
                node_tag['id'] = element.attrib['id']
                node_tag['key'] = child.attrib['k']
                node_tag['value'] = child.attrib['v']
                node_tag['type'] = 'regular'
                tags.append(node_tag)
        
        return {'node': node_attribs, 'node_tags': tags}
        
    
    elif element.tag == 'way':  # 'way'节点
        for attrib in element.attrib:
            if attrib in WAY_FIELDS:
                way_attribs[attrib] = element.attrib[attrib]
        
        position = 0    #计数,用于填充way下面nd子标签的position的值
        for child in element:
            way_tag = {}
            way_node = {}
            if child.tag == 'tag':
                if COLON_CHAR.match(child.attrib['k']):
                    way_tag['type'] = child.attrib['k'].split(':')[0]
                    way_tag['key'] = child.attrib['k'].split(':')[1]
                    way_tag['id'] = element.attrib['id']
                    way_tag['value'] = child.attrib['v']
                    tags.append(way_tag)

                elif NOR_CHAR.match(child.attrib['k']):
                    way_tag['type'] = 'regular'
                    way_tag['key'] = child.attrib['k']
                    way_tag['id'] = element.attrib['id']
                    way_tag['value'] = child.attrib['v']
                    tags.append(way_tag)
                    
            elif child.tag == 'nd':
                way_node['id'] = element.attrib['id']
                way_node['node_id'] = child.attrib['ref']
                way_node['position'] = position
                position += 1
                way_nodes.append(way_node)
            
        
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


def get_element(osm_file):
    """
    如果标签正确，生成XML元素，只考虑node和way
    osm_file: 文件名
    返回：生成元素
    """
    """
    参考： https://www.cnblogs.com/luhuajun/p/7977561.html
    """
    
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in ('node', 'way'):
            yield elem
            root.clear()


class UnicodeDictWriter(csv.DictWriter, object):
    """
    参考： https://www.cnblogs.com/luhuajun/p/7977561.html
    """

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)



#==============================================================================
            
if __name__ == '__main__':

    OSMFILE = "Houston.osm"
    
    # main(OSMFILE)
    NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
    WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
    WAY_NODES_FIELDS = ['id', 'node_id', 'position']
    
    NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
    WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
    
    # node节点生成两个文件：node属性信息、下级tag标签信息
    NODES_PATH = "nodes.csv"
    NODE_TAGS_PATH = "nodes_tags.csv"

    # way节点生成三个文件：way属性信息、下级node标签信息、下级tag标签信息
    WAYS_PATH = "ways.csv"
    WAY_NODES_PATH = "ways_nodes.csv"
    WAY_TAGS_PATH = "ways_tags.csv"
    
    # 数据文件两类元素共生产5个csv文件
    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        # 调用UnicodeDictWriter父类csv.DictWriter方法
        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        for element in get_element(OSMFILE):
            elem = shape_element(element)
            if elem:
                # 分别按照'node'和'way'向文件中写数据
                if element.tag == 'node':
                    nodes_writer.writerow(elem['node'])
                    node_tags_writer.writerows(elem['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(elem['way'])
                    way_nodes_writer.writerows(elem['way_nodes'])
                    way_tags_writer.writerows(elem['way_tags'])
    
    print '\nDone!'
    
    
    
    