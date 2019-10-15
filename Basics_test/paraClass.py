#coding:utf-8
import functions

IncrementData = {}
NotRepeatData = {}

class ParaClass:
    def __init__(self, name, patterns, notes, inXml, necessary, otherXmlRules, increment, firstValue, notRepeat, other_rules):
        self.name = name
        self.patterns = patterns
        self.notes = notes
        self.inXml = inXml
        self.necessary = necessary
        self.otherXmlData = self.__getOtherXmlData(otherXmlRules)
        self.increment = increment
        self.firstValue = firstValue
        self.notRepeat = notRepeat
        self.other_rules = other_rules
    

    def __getOtherXmlData(self, otherXmlRules):
        if not otherXmlRules:
            return None
        dic = {}
        other_xml_name = otherXmlRules.split(",")[0] 
        if "/" not in otherXmlRules.split(",")[1]:
            other_xml_parameter = otherXmlRules.split(",")[1]
            other_xml_vals = functions.getValListFromXml(other_xml_name, other_xml_parameter)
        else:
            other_xml_parameter = otherXmlRules.split(",")[1].split("/")[0]
            other_xml_parameter_extend = otherXmlRules.split(",")[1].split("/")[1]
            other_xml_vals = functions.getValListFromXml(other_xml_name, other_xml_parameter, other_xml_parameter_extend)
            
        dic["other_xml_name"] = other_xml_name
        dic["other_xml_parameter"] = other_xml_parameter      
        dic["other_xml_vals"] = other_xml_vals   
        '''    
        if "itemId.xml" == other_xml_name:
            other_xml_parameter = "松松+道具+碎片+金币+钻石+体力+Gacha券"
            tsum_xml = XmlTree("tsum.xml", getXmlContent("tsum.xml")) 
            tsumIds = tsum_xml.getValList("id")
            prop_xml = XmlTree("prop.xml", getXmlContent("prop.xml")) 
            propIds = prop_xml.getValList("id")
            fragment_xml = XmlTree("fragment.xml", getXmlContent("fragment.xml"))
            fragmentIds = fragment_xml.getValList("id")
            other_xml_vals = tsumIds + propIds + fragmentIds + ["2000", "3000", "4000", "1011"]
        '''   
 
        if 3 == len(otherXmlRules.split(",")):
            dic["separatorAndIndex"] = otherXmlRules.split(",")[2]
        
        return dic


        
        
        
        
        
        
        
        
        
        
    
    
    