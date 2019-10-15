#coding:utf-8

import sys 
sys.path.insert(0, 'D:\workspace\UITest_TsumTsum\GUI_test')
from TestFrame import MyFrame

import wx
import re
import os
import time
import wx.lib.agw.aui as aui2
import xlrd
import win32com.client as win32
import unittest
import HTMLTestRunnerCN
import pandas
import wx.html2 as webview

from shutil import move
from wx import stc
from wx.lib.embeddedimage import PyEmbeddedImage
import wx.lib.platebtn as platebtn
from xlwt import Workbook
from threading import Thread
from airtest.core.api import *
from poco.drivers.unity3d import UnityPoco

if __name__ == '__main__':
    MyFrame()