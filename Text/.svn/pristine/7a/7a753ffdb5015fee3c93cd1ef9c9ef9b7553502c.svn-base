#coding:utf-8

import os
import codecs
import xlrd
import sys
import re 

KEY_LIST = {}

# /project/assets/resource/text/
def export(lang, rows, target_dir):
    target_dir = os.path.join(target_dir, lang)
    print(os.path.abspath(target_dir))
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    text_file = os.path.join(target_dir, 'text.json')
    cfg = codecs.open(text_file, 'wb', 'utf-8')
    cfg.write('{\n')
    first = True
    for row in rows:
        if not first:
            cfg.write(',\n');
        else:
            first = False
        if lang in row:
            v = row[lang].replace('\\','\\\\')
            v = v.replace('"','\\"')
            v = v.replace('\\\\n','\\n')
            cfg.write('"%s":"%s"'%(row['key'], v))

    cfg.write('\n}')
    cfg.close()

def export2file(langs, result, target_dir):
    for lang in langs:
        export(lang, result, target_dir)

def checkVal(v, field, fileName):
    global KEY_LIST
    
    if "key" == field:
        if v not in KEY_LIST:
            KEY_LIST[v] = fileName
        else:
            print "   × %s和%s中出现重复的key值: %s" %(fileName, KEY_LIST[v], v.encode("utf-8"))
            sys.exit(1)
    '''
    pattern1 = "^.*%[^ds%]{1}.*$"
    pattern2 = "^.*%%.+$"
    pattern3 = "^[^ds]+%{1,2}$"
 
    if (re.match(pattern1, v) and not re.match(pattern2, v)) or re.match(pattern3, v): 
        print "   × '%'使用错误 : ", v
        sys.exit(1)
    '''
    err = False
    count = 0
    for char in v:
        if count == 0 and char == '%':
            count = 1
        elif count == 1:
            if char not in ["s", "d", "%"]:
                err = True
                break
            else:
                count = 0
    if count:
        err = True
    if err:
        print "   × '%'使用错误 : ", v
        sys.exit(1)
        
    return True

def xls2list(langs, result, folder, fileName, startRow):
    workbook = xlrd.open_workbook(folder + "/" + fileName)
    sheet = workbook.sheet_by_index(0)

    fields = sheet.row_values(0)
    for lang in fields[1:2]:
        if (lang not in langs) and len(lang) > 0 and (not lang.startswith('cmt_')):
            langs[lang] = 1

    for i in range(startRow, sheet.nrows):
        row_dict = {}
        for j in range(sheet.ncols-1):
            v = sheet.cell_value(i, j)
            if not fields[j].startswith('cmt_'):
                v = v.replace('\n','\\n')
                if len(v.strip()) > 0 and checkVal(v, fields[j], fileName):
                    row_dict[fields[j]] = v.strip();
        if len(row_dict) > 0:
            result.append(row_dict)

def main():

    if len(sys.argv)<2:
        print("export_lang.py target_dir缺失，没有进行文案检查！！！")
        return

    target_dir = sys.argv[1]
 
    startRow=2
    result = []
    langs = {}
    
    folder = os.path.dirname(os.path.realpath(__file__))
    
    for fileName in os.listdir(folder):
        if fileName.endswith('.xlsx'):
            print '★ Start ', fileName
            xls2list(langs, result, folder, fileName, startRow)
        
    export2file(langs.keys(), result, target_dir)

if __name__=='__main__':
    main()
