#coding:utf-8
import xmlTreeClass
import requests
from Config import *


def getXmlContent(xmlName):
    xml_url = API_URL + "/viewFile.do?appName=%s&fileName=%s" % (APPNAME, xmlName)
    s = requests.Session()
    s.auth = (USER, PASSWORD)
    r = s.get(xml_url)
    return r.content


# 获取所有元素的某个参数的值，保存列表返回，可以是由另一个参数的值来决定是否有效;应用举例 getValListFromXml("tsum_xml", "id", "visible=1")
def getValListFromXml(xml_name, xml_parameter, paraChecker=None):
    other_xml_tree = xmlTreeClass.XmlTree(xml_name, getXmlContent(xml_name))
    root = other_xml_tree.root

    para_vals = []
    if not paraChecker:
        for child in root:
            if "type" == child.tag:
                continue
            if child.get(xml_parameter):  # 有的元素没有某些参数，比如stage.xml中的hiddenStages，此时取到是None，不计入列表
                para_vals.append(child.get(xml_parameter))
    else:
        for child in root:
            if "type" == child.tag:
                continue
            attrCheckerName = paraChecker.split("=")[0]
            attrCheckerValue = paraChecker.split("=")[1]
            v = child.get(attrCheckerName)
            if child.get(xml_parameter) and attrCheckerValue == v:
                para_vals.append(child.get(xml_parameter))

    # 去重，但不打乱顺序
    # para_vals = list(set(para_vals))
    para_vals2 = []
    for p in para_vals:
        if p not in para_vals2:
            para_vals2.append(p)
    return para_vals2


# 获取所有元素中某三个参数，组成字典结构返回，可以由另一个参数决定是什么形式：如{x：{y:z}}或者{x：{y:[z]}}
def getValDicFromXml(xml_name, xml_parameter1, xml_parameter2, xml_parameter3=None, dicValueFormat='str'):
    other_xml_tree = xmlTreeClass.XmlTree(xml_name, getXmlContent(xml_name))
    root = other_xml_tree.root

    dicVals = {}
    if not xml_parameter3:
        # 获取两个参数的字典，value的参数类型为str
        if 'str' == dicValueFormat:
            for child in root:
                if "type" == child.tag:
                    continue
                val1 = child.get(xml_parameter1).encode('utf-8')
                val2 = child.get(xml_parameter2)

                if not val1 or not val2:
                    continue
                if val1 not in dicVals.keys():
                    dicVals[val1] = val2
        # 获取两个参数的字典，value的参数类型为数组
        if 'dic' == dicValueFormat:
            for child in root:
                if "type" == child.tag:
                    continue
                val1 = child.get(xml_parameter1)
                val2 = child.get(xml_parameter2)

                if not val1 or not val2:
                    continue
                if val1 not in dicVals.keys():
                    dicVals[val1] = [val2]
                else:
                    dicVals[val1].append(val2)
    else:
        # 获取三个参数的字典，value的参数类型为str
        if 'str' == dicValueFormat:
            for child in root:
                if "type" == child.tag:
                    continue
                val1 = child.get(xml_parameter1)
                val2 = child.get(xml_parameter2)
                val3 = child.get(xml_parameter3)

                if not val1 or not val2 or not val3:
                    continue
                if val1 not in dicVals.keys():
                    dicVals[val1] = {val2: val3}
                else:
                    if val2 not in dicVals[val1].keys():
                        dicVals[val1][val2] = val3
        # 获取三个参数的字典，value的参数类型为数组
        if 'dic' == dicValueFormat:
            for child in root:
                if "type" == child.tag:
                    continue
                val1 = child.get(xml_parameter1)
                val2 = child.get(xml_parameter2)
                val3 = child.get(xml_parameter3)

                if not val1 or not val2 or not val3:
                    continue
                if val1 not in dicVals.keys():
                    dicVals[val1] = {val2: [val3]}
                else:
                    if val2 not in dicVals[val1].keys():
                        dicVals[val1][val2] = [val3]
                    else:
                        dicVals[val1][val2].append(val3)
    return dicVals


def getGlobalData(key):
    global_xml_tree = xmlTreeClass.XmlTree('global.xml', getXmlContent('global.xml'))
    for child in global_xml_tree.root:
        if key == child.get('key'):
            return child.text
        else:
            continue

                    
                
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    