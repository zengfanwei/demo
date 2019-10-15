# coding=utf-8
import os
import re

def findClassAndDef(path):
    dirs = os.listdir(path)
    caselist = []
    for file in dirs:
        if os.path.splitext(file)[1] == '.py' and os.path.splitext(file)[0].startswith('test_'):
            caselist.append(file)
    #print caselist
    dic = {}
    for filename in caselist:
        name = path + '\\' + filename
        file = open(name, 'r').readlines()
        deflist = []
        className = ''
        for i in file:
            if i.startswith('class'):
                className += re.search(r' (.*?)\(', i).group(1)
            elif i.startswith('    def'):
                deflist += re.findall(r'test_A[1-9]?\d?', i)
            else:
                pass
        dic[className] = deflist
        #print dic
    return dic

