# coding=utf-8

import xmlTreeClass
import functions

def GetTsumInfo(info_dic):
    chestlevel_tree = xmlTreeClass.XmlTree("tsum.xml", functions.getXmlContent("tsum.xml"))
    for child in chestlevel_tree.root:
        if "type" == child.tag:
            continue
        tsumId_val = child.get("id")
        familyId_val = child.get("family")
        tsumstar_val = child.get("star")

        if not tsumId_val or not familyId_val or not tsumstar_val:
            continue
        if tsumId_val not in info_dic.keys():
            info_dic[tsumId_val] = [familyId_val, tsumstar_val]
        else:
            if familyId_val != info_dic[tsumId_val][0] or tsumstar_val != info_dic[tsumId_val][1]:
                info_dic[tsumId_val] = [familyId_val, tsumstar_val]
    return info_dic
