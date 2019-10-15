# coding=utf-8

import xmlTreeClass
import functions

def GetTsumLevelupInfo(levelupInfo_dic):
    chestlevel_tree = xmlTreeClass.XmlTree("tsum_levelup.xml", functions.getXmlContent("tsum_levelup.xml"))
    for child in chestlevel_tree.root:
        if "type" == child.tag:
            continue
        cost_val = child.get("cost")
        basescore_val = child.get("basescore")
        level_val = child.get("level")
        nextExp_val = child.get("nextExp")
        skillLv_val = child.get('skillLv')
        star_val = child.get('star')

        if not star_val or not skillLv_val or not level_val or not basescore_val:
            continue
        if star_val not in levelupInfo_dic.keys():
            levelupInfo_dic[star_val] = {level_val: [basescore_val, cost_val, nextExp_val, skillLv_val]}
        else:
            if level_val not in levelupInfo_dic[star_val].keys():
                if nextExp_val and cost_val:
                    levelupInfo_dic[star_val][level_val] = [basescore_val, cost_val, nextExp_val, skillLv_val]
                else:
                    levelupInfo_dic[star_val][level_val] = [basescore_val, None, None, skillLv_val]
    return levelupInfo_dic
def GetTsumSkillup(skillup_dic):
    chestlevel_tree = xmlTreeClass.XmlTree("tsum_levelup.xml", functions.getXmlContent("tsum_levelup.xml"))
    for child in chestlevel_tree.root:
        if "type" == child.tag:
            continue
        skillLv_val = child.get("skillLv")
        level_val = child.get("level")
        star_val = child.get('star')

        if not star_val or not skillLv_val or not level_val:
            continue
        if star_val not in skillup_dic.keys():
            skillup_dic[star_val] = {skillLv_val: [level_val]}
        else:
            if skillLv_val not in skillup_dic[star_val].keys():
                skillup_dic[star_val][skillLv_val] = [level_val]
            else:
                skillup_dic[star_val][skillLv_val].append(level_val)
    return skillup_dic
