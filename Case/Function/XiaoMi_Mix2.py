# coding=utf-8

from airtest.core.api import init_device
''' 原用法: connect_device(IP['VIVO_x9'])
    由于原用法需要先取IP值，但是如果import IP写在上面，会导致只能跑一台设备，保险起见，
    先使用init_device()写死'''
init_device('android', '10.130.148.229:6680')

import sys
sys.path.insert(0, 'D:\workspace\UITest_TsumTsum\Basics_test')
from Config_test import IP, CASE_EXCEL_PATH, REPORT_PATH
from GetClassDef import findClassAndDef

sys.path.insert(0, 'D:\workspace\UITest_TsumTsum\Case')
# from test_shop import Shop
# from test_free_chest import ShopFreeChest
# from test_rolelist import Rolelist
# from test_not_enough_pay_chest import ShopNotEnoughPayChest
from test_cash_pay_chest import ShopCashPayChest

import os.path
import unittest
import HTMLTestRunnerCN
import time
from shutil import move


def startCase(dev, testunit):
    device_name = dev
    '''
    testunit = unittest.TestSuite()  # 一个测试套件对象
    dic = findClassAndDef(os.path.dirname(CASE_EXCEL_PATH))
    classList = dic.keys()
    for classname in classList:
        a = 'testunit.addTest(' + classname
        for defname in dic[classname]:
            b = a + '("' + defname + '"))'
            eval(b)
    
    discover = unittest.defaultTestLoader.discover(os.path.dirname(CASE_EXCEL_PATH), pattern='test*.py', top_level_dir=None)
    testunit.addTest(discover)
    '''
    '''
    # 更新报告
    if not os.path.exists(REPORT_PATH):
        os.makedirs(REPORT_PATH + '\\OldReport')
    else:
        if not os.path.exists(REPORT_PATH + '\\OldReport'):
            os.mkdir(REPORT_PATH + '\\OldReport')
    '''
    dirs = os.listdir(REPORT_PATH)
    for file in dirs:
        if os.path.splitext(file)[1] == ".html" and os.path.splitext(file)[0].endswith('%s report' % device_name):
            filepath = os.path.join(REPORT_PATH, file)
            move(filepath, REPORT_PATH + '\\OldReport')

    # 定义报告存放目录,支持相对路径
    now = time.strftime("%Y-%m-%M-%H-%M-%S", time.localtime(time.time()))
    filename = now + ' %s report.html' % device_name
    report_path = os.path.join(REPORT_PATH, filename)  # 文件夹和文件合并成路径
    fp = open(report_path, 'wb')
    runner = HTMLTestRunnerCN.HTMLTestRunner(fp, title=u'自动化测试报告', description=u'用例执行情况', verbosity=2,
                                                     tester="fanwei")
    runner.run(testunit)
    fp.close()


if __name__ == '__main__':
    deviceName = 'XiaoMi_Mix2'
