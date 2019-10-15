# coding=utf-8

import pandas
import xlrd
import os
import time
from airtest.core.api import *
from functions import getValListFromXml
from poco.drivers.unity3d import UnityPoco
from airtest.core.helper import G
from ReturnHomePage import Return
poco = UnityPoco()
Pagelist = []

def GetCase(address, name):
    worksheet = xlrd.open_workbook(address)
    sheet = worksheet.sheet_by_name(name)
    cols = sheet.col_values(0)
    tips = []
    for i in range(len(cols)):
        a = cols[i].encode('utf-8')
        if len(a.split('\n')) <= 1:
            tips.append(a)
        else:
            for j in a.split('\n'):
                tips.append(j)
    return tips

def Click(botton, photo='', pos=None, resolution=(1080, 2160)):
    '''
    try:
        poco(botton).wait_for_appearance(timeout=timeout)
        poco(botton).click()
    except:
        raise KeyError
    '''
    if photo and pos:
        wait(Template(photo, record_pos=pos, resolution=resolution))
        poco(botton).click()
    else:
        poco(botton).wait()
        poco(botton).click()

def ChildClick(father, children, page):
    try:
        poco(father).child(children).click()
    except:
        GetErrorPage(page)

def GetMeta(xml, data):
    dataList = getValListFromXml(xml, data)
    return dataList

def GetText(localAddress, excelName):
    path = localAddress
    excel = path + '\\' + excelName
    data = pandas.read_excel(excel)
    dic = {}
    key_list = data['key']
    data_list = data['zh_CN']
    for i in range(len(key_list)):
        dic[key_list[i]] = data_list[i]

    return dic

def GetErrorPage(page):
    global Pagelist
    Pagelist.append(page)
    return Pagelist

def GetSnapshot(path):
    G.DEVICE.snapshot(path)

def checkTwoL(l1, l2):
    err = 0
    if len(l1) != len(l2):
        return False
    else:
        for i in l1:
            if i not in l2:
                err += 1
        if err != 0:
            return False
        else:
            return True
def checkTextEqual(control):
    old = poco(control).get_text()
    time.sleep(0.0001)
    new = poco(control).get_text()
    print old
    print new
    if old == new:
        timeLimit = 0.0
        while timeLimit < 2.0:
            old1 = poco(control).get_text()
            time.sleep(0.5)
            timeLimit += 0.5
            new1 = poco(control).get_text()
            print old1
            print new1
            if old1 != old:
                if old1 == new1:
                    break
            else:
                if old1 != new1:
                    continue
