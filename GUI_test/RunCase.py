#coding:utf-8

import sys 
sys.path.insert(0, 'D:\workspace\UITest_TsumTsum\Basics_test')
from Config_test import SVN_PATH, URL, Uname, PWD, LocalAddress, IP, BAT_PATH, CASE_PATH, REPORT_PATH, CASE_EXCEL_PATH
from adb_devices import refreshDevices
import os
import unittest
import shutil


def getDevice(devs):
    # 整理要跑脚本的设备
    iplist = []
    mobiles = IP.keys()
    address = IP.values()
    devList = []
    for dev in devs:
        iplist.append(dev[0])
    for i in range(len(address)):
        for ip in iplist:
            if ip in address[i]:
                devList.append(mobiles[i])
    return devList


def getText(url, username, password, localAddress):

    if os.path.exists(localAddress):
        cleanLocalTsumText = 'del /Q %s' % localAddress
        # shutil.rmtree(localAddress)
        os.system(cleanLocalTsumText)
    checkoutTsumText = 'svn checkout %s %s --username %s --password %s' % (url, localAddress, username, password)
    os.system(checkoutTsumText)


def run():
    # 合成写入Bat脚本的字符串
    getText(URL, Uname, PWD, LocalAddress)
    content = '@echo off\n'  # 表示执行了这条命令后关闭所有命令(包括本身这条命令)的回显
    mobiles = refreshDevices()
    if "<type 'str'>" == str(type(mobiles)):
        print mobiles
    else:
        devList = getDevice(mobiles)
        print devList
        for dev in devList:
            cont = 'start python D:\\workspace\\UITest_TsumTsum\\Case\\Function\\startUnittest.py ' + dev + '\n'
            content += cont
        # print content
        # 没有bat文件，创建bat文件
        f = open(BAT_PATH, 'w')
        # 清除数据
        f.truncate()
        f.write(content)
        f.close()

        # 确保报告文件夹存在
        if not os.path.exists(REPORT_PATH):
            os.makedirs(REPORT_PATH + '\\OldReport')
        else:
            if not os.path.exists(REPORT_PATH + '\\OldReport'):
                os.mkdir(REPORT_PATH + '\\OldReport')
        # 执行bat文件
        os.system('start ' + BAT_PATH)

# getText(SVN_PATH, URL, Uname, PWD, LocalAddress)


if __name__ == '__main__':
    run()