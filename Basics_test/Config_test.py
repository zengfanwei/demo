# coding=utf-8
import os


# 绝对
CASE_EXCEL_PATH = "D:\\workspace\\UITest_TsumTsum\\Case\\UITestCase.xls"    #用例excel文件位置 
SVN_PATH = 'C:\\Program Files\\TortoiseSVN\\bin'
ADB_PATH = 'F:\\AirtestIDE_2018-10-11_py3_win64\\airtest\\core\\android\\static\\adb\\windows'
LocalAddress = 'D:\\workspace\\UITest_TsumTsum\\Text'
REPORT_PATH = 'D:\\workspace\\UITest_TsumTsum\\Report'
BAT_PATH = 'D:\\workspace\\UITest_TsumTsum\\Case\\Function\\run.bat'
CASE_PATH = 'D:\\workspace\\UITest_TsumTsum\\Case\\Function\\'
LOG_PATH = 'D:\\workspace\\UITest_TsumTsum\\Log\\'

#相对
PROJECT_PATH = os.getcwd()
#print "PROJECT_PATH: ", PROJECT_PATH


#---------------------------------------------------------------------------

APPNAME = "tsumtsum_qa"
API_URL = 'http://config.happyelements.net:8082/api'
USER = 'service_auth'
PASSWORD = 'qwer1234!'

URL = 'http://svn.happyelements.net/repos/svndata3/TsumTsum/Share/mobile-text/'
Uname = 'fanwei.zeng'
PWD = 'Zfw.950420'


IP = {'XiaoMi_Mix2': 'android:///10.130.148.229:6680',
      'OPPO_R9s': 'android:///10.130.149.210:6677',
      'VIVO_x9': 'android:///10.130.150.240:6675',
      'OPPO_R11': 'android:///10.130.144.230:6682',
      'MOTO_Nexus6': 'android:///10.130.148.138:6684',
      'Redmi_Note3': 'android:///10.130.144.128:6686',
      'VIVO_Y66': 'android:///10.130.144.172:6688',
      'XiaoMi_8': 'android:///10.130.150.176:7777',
      'HuaWei_P20': 'android:///10.130.148.60:6681'}
