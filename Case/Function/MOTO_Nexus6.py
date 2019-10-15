# coding=utf-8

from airtest.core.api import init_device
''' 原用法: connect_device(IP['VIVO_x9'])
    由于原用法需要先取IP值，但是如果import IP写在上面，会导致只能跑一台设备，保险起见，
    先使用init_device()写死'''
init_device('android','10.130.148.138:6684')

import sys
sys.path.insert(0, 'D:\workspace\UITest_TsumTsum\Basics_test')
from Config_test import IP, CASE_EXCEL_PATH, REPORT_PATH
from GetClassDef import findClassAndDef

sys.path.insert(0, 'D:\workspace\UITest_TsumTsum\Case')
from test_shop import Shop
from test_rolelist import Rolelist

import os.path
import unittest
import HTMLTestRunnerCN
import time
from shutil import move

device_name = 'MOTO_Nexus6'

now = time.strftime("%Y-%m-%M-%H-%M-%S", time.localtime(time.time()))
filename = now + ' %s report.html' % device_name
report_abspath = os.path.join(REPORT_PATH, filename)
testunit = unittest.TestSuite()
dic = findClassAndDef(os.path.dirname(CASE_EXCEL_PATH))
classList = dic.keys()
for classname in classList:
    a = 'testunit.addTest(' + classname
    for defname in dic[classname]:
        b = a + '("' + defname + '"))'
        eval(b)

#更新报告
if not os.path.exists(REPORT_PATH):
    os.makedirs(REPORT_PATH)
if not os.path.exists(REPORT_PATH + '\\OldReport'):
    os.makedirs(REPORT_PATH + '\\OldReport')
dirs = os.listdir(REPORT_PATH)
for file in dirs:
    if os.path.splitext(file)[1] == ".html" and os.path.splitext(file)[0].endswith('%s report' % device_name):
        filepath = os.path.join(REPORT_PATH, file)
        move(filepath, REPORT_PATH + '\\OldReport')

# 定义报告存放目录,支持相对路径
fp = open(report_abspath, 'wb')
runner = HTMLTestRunnerCN.HTMLTestRunner(fp, title=u'自动化测试报告', description=u'用例执行情况', verbosity=2,
                                                 tester="fanwei")
runner.run(testunit)
fp.close()
