# -*- coding: utf-8 -*-

"""
1.解析OSM文件的tag标签
2.处理单词简写带来的一致性问题
https://docs.python.org/2/library/xml.etree.elementtree.html?highlight=elementtree
"""

import xml.etree.cElementTree as ET
import re
from collections import defaultdict
import pprint

OSMFILE = "Houston.osm"

# =============================================================================

# 1.解析OSM文件的tag标签

def count_tags(filename):
    """
    计算osm文件中各标签的数量
    
    filename:文件名
    返回：包含所有（数据标签:数量）键值对的字典
    """
    tags = {}
    for event, elem in ET.iterparse(filename):           
        if elem.tag not in tags: 
            tags[elem.tag] = 1
        else:
            tags[elem.tag] += 1
    return tags
    



# =============================================================================

# 2.处理单词简写带来的一致性问题

# 需要更正的单词
expected = ["Street", "Road", "Avenue"]     


def audit_street(street_types, street_name): 
    """
    提取街道名末尾单词，用来判断是否是街道
    
    street_types:包含各种街道类型、完整街道名称的字典
    street_name:完整的街道名称    
    """
    # 单词边界+字符(+.)+字符末尾
    regex = re.compile(r'\b\S+\.?$', re.IGNORECASE)      
    
    m = regex.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def audit(filename): 
    """
    满足下列形式的元素才解析街道名称，街道名为v值
    <way ……>
        ……
        <tag k = 'addr:street', v = ……>
    或者：
    <node ……>
        ……
        <tag k = 'addr:street', v = ……>
    
    file：地图文件名
    返回：包含街道类型，完整街道名称的字典
    """
    osm_file = open(filename, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag in ['node', 'way']:
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == 'addr:street':
                    audit_street(street_types, tag.attrib['v'])

    return street_types


def update_name(name):
    """
    如果街道名称最后一个单词在mapping中有需要更换的匹配，按照mapping进行替换
    
    name：完整街道名称
    返回：替换过后的街道名称
    """
    # 需要更改的街道类型映射字典
    mapping = {
           "Ave.": "Avenue",
           "Ave": "Avenue",
           "road": "Road",
           "Rd": "Road",
           "Rd.": "Road",
           "St":"Street",
           "St.":"Street"
            }
    
    name = name.split(' ')
 
    # 根据mapping映射，替换街道名称最后一个单词
    len_ = len(name)
    if name[len_ - 1] in mapping:
        name[len_- 1] = mapping[name[len_- 1]]
        name[len_- 1] = name[len_- 1].title()
    else:
        name[len_- 1] = name[len_- 1].title()
    
    name = ' '.join(name)

    return name


# =============================================================================
    
if __name__ == '__main__':
    
    # 计算文件中各类标签数量
    tags = count_tags(OSMFILE)
    pprint.pprint(tags)
    print '\n'
    
    # 街道类型 : 街道名称
    pprint.pprint(dict(audit(OSMFILE))) 
    print '\n'

    # 替换前名称 --> 替换后名称
    update_street = audit(OSMFILE) 

    for street_type, ways in update_street.iteritems():
        for name in ways:
            updated_name = update_name(name)
            print name, "-->", updated_name
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            