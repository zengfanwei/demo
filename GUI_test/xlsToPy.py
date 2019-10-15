#coding:utf-8

import sys 
sys.path.insert(0, 'D:\workspace\UITest_TsumTsum\Basics_test')
import Config_test

import os, shutil
import sys
import xlrd
from xlwt import Workbook
import win32com.client as win32

import re
import time


CASE_EXCEL_PATH = Config_test.CASE_EXCEL_PATH

START_STRING = "# coding=utf-8\nimport MyCase\nimport unittest\nfrom TsumTest.Basics.Config import *\n" + \
                "from TsumTest.Basics.BasicFunction import GetMeta, GetCase, GetText, GetErrorPage, Click\n" + \
                "from TsumTest.Basics.ReturnHomePage import Return\n" + \
                "from airtest.core.api import *\n" + \
                "from airtest.core.helper import G\n" + \
                "from poco.drivers.unity3d import UnityPoco\n\n"

END_STRING = "@classmethod\n" +\
         "\tdef tearDownClass(cls):\n" +\
         "\t\tif not poco('c2_left').exists():\n" + \
         "\t\t\tpage = 'homePage'\n" + \
         "\t\t\tpagelist = GetErrorPage(page)\n" + \
         "\t\t\terrorpage = pagelist[0]\n" + \
         "\t\t\tReturn(errorpage)\n" + \
         "\t\telse:\n" + \
         "\t\t\tpass\n\n" + \
         "if __name__ == '__main__':\n\tunittest.main()"

#保存用例状态值
STATES = ["OK", "ADD", "DELETE", "CHANGE"] 

def xlsToPy1(sheet):
    #sheet name是小写，转化为首字母大写
    s = "class %s(unittest.TestCase):\n" % (sheet.name[0].upper() + sheet.name[1:]).encode("utf-8")
    #print type(s)
    nrows = sheet.nrows
    for row in range(nrows):
        v = sheet.cell_value(row, 0)
        #print v, type(v)
        if str(type(v)) == "<type 'unicode'>":
            v = v.encode("utf-8")
        #print v, type(v)
        s += "\tdef test_%s(self):\n" % ("A" + str(row+1)) + \
            "\t\tu\"\"\"%s\"\"\"\n\n" % v
    s += "\t"        
    return s

def xlsToPy2(sheet, pyName, states):
    pyFile = open(pyName, "r")
    content_old = pyFile.read()
    pyFile.close()
    #print type(content_old), content_old
    r = re.compile("test_.+:\n([\s\w\W]+?)def")
    casesFromPy = r.findall(content_old)
    if len(casesFromPy) == 0:
        print "Error，.py中已没有用例代码，请删除py文件，从新初始化!"
        sys.exit(0)        
    
    #获取py和表中用例数
    casesFromPy_count_old = len(casesFromPy)
    casesFromPy_count_old_copy = casesFromPy_count_old
    casesFromXls_count = len(states)
    
    #容错
    if casesFromXls_count < casesFromPy_count_old:
        print "Error，工作表%s中，用例个数少于.py，请确认!"
        sys.exit(0)
    
    #去掉数组最后一个元素末尾的 "@classmethod"
    #因为字符串是不可变对象，也就是不支持原地修改的!!!!!!!!!!!!!!!!!!!!!!!
    p = casesFromPy[casesFromPy_count_old-1].find("@classmethod")
    casesFromPy[casesFromPy_count_old-1] = casesFromPy[casesFromPy_count_old-1][0:p]
    
    #新增的用例空补齐
    add_case_count = casesFromXls_count - casesFromPy_count_old
    for i in range(add_case_count):
        casesFromPy.append("") 
    casesFromPy_count_new = len(casesFromPy)
    
    add_cases = []
    change_cases = []
    delete_cases = []
    for i in range(casesFromXls_count-1, -1, -1):
        #记录CHANGE和ADD的顺序，以便修改用例描述
        if states[i] == "ADD":
            add_cases.append(i)
        if states[i] == "CHANGE":
            change_cases.append(i)
        if states[i] == "DELETE":
            delete_cases.append(i)
            
        #如果有新增用例，状态倒叙查找，对OK、CHANGE的用例顺序进行对调
        if add_case_count > 0:
            
            if states[i] != "ADD":
                j = casesFromPy[casesFromPy_count_old_copy - 1]
                casesFromPy[casesFromPy_count_old_copy - 1] = casesFromPy[casesFromPy_count_new - 1]
                casesFromPy[casesFromPy_count_new - 1] = j
                casesFromPy_count_new -=1
                casesFromPy_count_old_copy -=1
            else:
                casesFromPy_count_new -=1
    
    #容错
    if len(add_cases) + casesFromPy_count_old != casesFromXls_count:
        print "Error，表中ADD的用例数  + py中的用例数 ≠表中的用例总数，请确认!"
        sys.exit(0)
    
    #处理CHANGE和ADD状态用例，更新用例描述
    for i in  add_cases:
        if str(type(sheet.cell_value(i, 0))) == "<type 'unicode'>":
            casesFromPy[i] = '\t\tu\"\"\"%s\"\"\"\n\n\t' % sheet.cell_value(i, 0).encode("utf-8")
        else:
            casesFromPy[i] = '\t\tu\"\"\"%s\"\"\"\n\n\t' % sheet.cell_value(i, 0)
    for i in  change_cases:
        if str(type(sheet.cell_value(i, 0))) == "<type 'unicode'>":
            casesFromPy[i] = re.sub('"""([\w\W\s]*?)"""', '"""%s"""' % sheet.cell_value(i, 0).encode("utf-8"), casesFromPy[i], 1)
        else:
            casesFromPy[i] = re.sub('"""([\w\W\s]*?)"""', '"""%s"""' % sheet.cell_value(i, 0), casesFromPy[i], 1)
    
    #处理DELETE状态用例
    for i in delete_cases:
        del casesFromPy[i];
    '''
    print len(casesFromPy)
    i = 1
    for c in casesFromPy:
        print "第%d个" % i
        print c
        i += 1
    '''
    i = 1
    content = "class %s(MyCase.Case):\n" % (sheet.name[0].upper() + sheet.name[1:]).encode("utf-8")
    for c in casesFromPy:
        if i ==1:
            content += "\tdef test_%s(self):\n" % ("A" + str(i))
        else:
            content += "def test_%s(self):\n" % ("A" + str(i))
        content += c
        i += 1
    return content

def initXls(sheetName, sheet, caseDirPath):
    #打开EXCEL
    xlApp = win32.Dispatch('Excel.Application')
    xlBook = xlApp.Workbooks.Open(os.path.join(caseDirPath, 'UITestCase.xls'))
    xlSheet = xlBook.Worksheets(sheetName) 
    
    del_row = []
    for row in range(sheet.nrows):
        #记录删除的行号
        if sheet.cell_value(row, 1) == "DELETE":
            del_row.append(row + 1)
        elif sheet.cell_value(row, 1) == "OK":
            continue
        else:
            xlSheet.Cells(row+1, 2).Value = "OK" 
    #删除行
    del_num = 0
    for dr in del_row:
        if del_num == 0:
            xlSheet.Rows(dr).Delete()    
        else:
            xlSheet.Rows(dr - del_num).Delete()
        del_num += 1

    xlBook.Close(SaveChanges=1) #完成 关闭保存文件
    del xlApp 
        
#获取特定列的数据
def getColVal(sheet, colNo):
    vals = []
    nrows = sheet.nrows
    for row in range(nrows):
        vals.append(sheet.cell_value(row, colNo))
    return vals

#检查用例状态列是否规范
def checkStates(states, nrows):
    if "" in states or states.count("OK") == nrows:
        return False
    for state in states:
        if state not in STATES:
            return False
    return True 
        
def xlsToPy0(sheetNames):
    if not os.path.exists(CASE_EXCEL_PATH):  
        print "Error，没有找到用例文件'%s'，正在自动创建......" % CASE_EXCEL_PATH
        #创建excel,python在使用xlwt创建excel并写入数据后,手动打开demo.xlsx时提示文件扩展名无效，将xlsx改为xls，可解决
        wb = Workbook()
        wb.add_sheet('Sheet1')
        # 保存Excel
        wb.save(CASE_EXCEL_PATH)
        print "创建完毕! 请去手动填写用例内容"
        return
    
    #打开excel
    workbook = xlrd.open_workbook(CASE_EXCEL_PATH)
    #逐个工作表同步
    for sheetName in sheetNames:
        try:
            sheet = workbook.sheet_by_name(sheetName)
        except:
            print "Error，没有找到工作表'%s'，同步失败" % sheetName
            return
        
        #是否备份
        backup = True
        #是否初始化工作表
        isInit = False
        # dirname 去掉文件名，返回目录 
#        print "os.path.abspath(os.path.pardir): ", os.path.abspath(os.path.pardir)
#        print "os.path.dirname(__file__): ", os.path.dirname(__file__) 
#        print "os.getcwd(): ", os.getcwd()
        caseDirPath = os.path.join(os.getcwd(), "Case")
#        print "caseDirPath: ", caseDirPath
#        print "__file__: ", __file__

        pyName = "test_%s.py" % sheetName
#        print "type(pyName):", type(pyName)
        
        #工作表内容为空，不做同步
        if sheet.nrows == 0:
            print "Warning，工作表%s内容为空，不做同步，请确认!" % sheetName
            continue

        #如果同名.py不存在，则创建
        pyPath = os.path.join(caseDirPath, pyName)
#        print "pyPath: ", pyPath
        if not os.path.exists(pyPath):
            print "没有找到文件 %s，正在自动创建并填写代码框架......" % pyPath
            #获取填充内容
            content = START_STRING + xlsToPy1(sheet) + END_STRING     
            backup = False
        #同步py
        else:
            #获取表格B列，即用例状态数据，发现除OK外数据，则需要同步到py
            states = getColVal(sheet, 1)
            #print type(states), len(states), states
            #如有不符合规范内容则提示用户，不做同步
            if not checkStates(states, sheet.nrows):
                print "Warning，在工作表%s中，发现用例状态列（B列）数据不符合规范，或者没有需要同步的用例，请确认!" % sheet.name.encode("utf-8")
                continue
            else:
                print "★正在同步%s表......" % sheetName 
                content = START_STRING + xlsToPy2(sheet, pyPath, states) + END_STRING
                isInit = True
        #备份.py
        if backup:      
            # 用例py文件的，备份文件夹
            backup_dir = os.path.join(caseDirPath, "backup")
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            # 进行备份    
            shutil.copyfile(pyPath, backup_dir + "/" + pyName.split(".")[0] + "_" + \
                            time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+ ".py") 
            
            print "已备份原py文件!"
        #初始化sheet
        if isInit:
            initXls(sheetName, sheet, caseDirPath)
        
        print "正在改写py文件..."    
        pyFile = open(pyPath, "w")
        pyFile.write(content)
        pyFile.close()     
        print "完毕!"

if __name__ == '__main__':
    xlsToPy0(["shop"])
