# coding=utf-8

import sys 
sys.path.insert(0, 'D:\workspace\UITest_TsumTsum\Basics_test')
from Config_test import ADB_PATH, IP, LOG_PATH
# from Basics_test.Config import ADB_PATH, IP

import os

# reload(sys)
# sys.getdefaultencoding()


def getDevice():
    result = os.popen('adb devices')
    adbConnectText = result.read()
    result.close()

    connectedDevice = adbConnectText.replace('List of devices attached', '').strip('\n')
    if '' == connectedDevice:
        return "还没有设备成功连接！"
    elif 'adb server didn\'t ACK' in connectedDevice or '** daemon still not running' in connectedDevice:
        return adbConnectText
    elif '* daemon not running. starting it now at tcp:5037 *' in connectedDevice:
        return adbConnectText
    else:
        devList = connectedDevice.split('\n')
        return devList

# 连接设备


def connectDevice(address):
    result = os.popen('adb connect ' + address)
    text = result.read()
    result.close()
    devices = IP.keys()
    ips = IP.values()
    device_name = ''
    for i in range(len(ips)):
        if address in ips[i]:
            device_name = devices[i]
    output1 = 'connected to '+address+'\n'

    if str(text) == str(output1):
        return (True, "设备连接成功！,%s" % device_name)
    else:
        return (False, text+device_name)
    
# 刷新设备


def refreshDevices():
    devlist = getDevice()
    if "<type 'str'>" == str(type(devlist)):
        return devlist
    else:
        devicesList = IP.keys()
        ipsList = IP.values()
        deviceName = ''
        datalist = [1, 2, 3]
        statelist = []
        for i in range(len(devlist)):
            datalist[0] = devlist[i].split('\t')[0]
            datalist[1] = devlist[i].split('\t')[1]
            for j in range(len(ipsList)):
                if devlist[i].split('\t')[0] in ipsList[j]:
                    deviceName = devicesList[j]
            datalist[2] = deviceName
            tup = tuple(datalist)
            statelist.append(tup)
        return statelist

# 获取运行设备的LOG信息


def getDeviceLog():
    onlineDevicesList = refreshDevices()
    for i in onlineDevicesList:
        if 'device' == i[1]:
            ip = i[0]
            deviceName = i[2]
            # 获取当前的进程id
            cmd1 = 'adb -s ' + ip + ' shell "ps | grep com.tencent.TsumTsumAndroid"'
            processText = os.popen(cmd1)
            process = processText.read()
            infoList = process.split('\n')
            allpid = []
            for info in infoList:
                pidList = info[13:].split(' ')
                allpid.append(pidList[0])
            pid = ''
            # 将应用的多个PID的log都输出到LOG_PATH本地
            for tsumPid in allpid:
                if '' != tsumPid:
                    pid = pid + '-e ' + tsumPid + ' '
            cmd2 = 'adb -s ' + ip + ' shell "logcat -d | grep ' + pid + '" > ' + LOG_PATH + deviceName + '.txt'
            os.system(cmd2)

