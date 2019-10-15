# coding=utf-8

import xmlTreeClass
import functions

def chestlevel(TsumDrop_dic, FixedRewards_dic):
    chestlevel_tree = xmlTreeClass.XmlTree("chest_level.xml", functions.getXmlContent("chest_level.xml"))
    for child in chestlevel_tree.root:
        if "type" == child.tag:
            continue
        chestId_val = child.get("chestId")
        userLevel_val = child.get("level")
        tsumDrop_val = child.get("tsumDrops")
        fixedRewards_val = child.get("fixedRewards")

        if not chestId_val or not userLevel_val or not tsumDrop_val:
            continue
        if chestId_val not in TsumDrop_dic.keys():
            TsumDrop_dic[chestId_val] = {userLevel_val: tsumDrop_val}
            FixedRewards_dic[chestId_val] = {userLevel_val: fixedRewards_val}
        else:
            if userLevel_val not in TsumDrop_dic[chestId_val].keys():
                TsumDrop_dic[chestId_val][userLevel_val] = tsumDrop_val
                FixedRewards_dic[chestId_val][userLevel_val] = fixedRewards_val
    return TsumDrop_dic, FixedRewards_dic
