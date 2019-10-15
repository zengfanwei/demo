##coding:utf-8

import xml.etree.ElementTree as ET
import re
from paraClass import ParaClass

'''
创建xml树类，同时在本地生成.xml文件
'''
class XmlTree:
    def __init__(self, xmlName, xmlContent, xmlRules_root=""):
        self.name = xmlName     
        self.root = ET.fromstring(xmlContent)#返回解析输的根节点
        if "" != xmlRules_root:
            self.paras = self.__createParaObj(xmlRules_root)
            
    def check(self):
        err = 0
        warn = 0
        first = True
        for child in self.root:
            if "type" == child.tag:
                continue
            id_val = child.get("id")
            parasFromXml = child.attrib.keys()
            self.__checkParaNumber(parasFromXml, id_val)
            
            for key in self.paras:
                pObj = self.paras[key]
                paraVal = child.get(pObj.name)
                if not paraVal:
                    continue
                i = 0
                for pattern in pObj.patterns:
                    if not re.match(pattern, paraVal):
                        pObj.errMsg(i, id_val, paraVal)
                        err += 1
                    i += 1
