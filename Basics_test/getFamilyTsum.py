# coding=utf-8

import xmlTreeClass
import functions

def familyTsum(level):
    familys = functions.getValListFromXml('user_levelup.xml', 'familyId')
    familyTsum = functions.getValDicFromXml('tsum.xml', 'family', 'name', dicValueFormat='dic')

    allTsumData = []
    for i in familys:
        allTsumData += familyTsum[i]

    unlockedTsumData = []
    for n in xrange(int(level)):
        unlockedTsumData += familyTsum[familys[n]]

    return allTsumData, unlockedTsumData