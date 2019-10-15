#coding:utf-8

import sys 
sys.path.insert(0, 'D:\workspace\UITest_TsumTsum\Basics_test')
from Config_test import PROJECT_PATH
from RunCase import run


import wx
import wx.html2 as webview
import re
import os
import time
#import wx.aui as aui
import wx.lib.agw.aui as aui2
import wx.lib.platebtn as platebtn
from wx import stc
from threading import Thread

import images
from adb_devices import connectDevice, refreshDevices
#import StyledTextCtrl_2
from StyledTextCtrl_2 import PythonSTC
from xlsToPy import xlsToPy0


# 需与 __LayoutPanel1()中buttons label一致
CASE_TO_SHEET = {"新手引导": "?", "城建": "?", "图鉴": "?", 
                 "商店": "shop", "任务": "?", "角色列表": "rolelist", 
                 "陈列柜": "?", "PVE": "?"}


def GetOriginalFilename(name):
    """
                    返回指定文件的路径
    """
    if os.path.isfile(name):
        return name

    # 遍历文件夹，直到找到该文件
    for dirpath, dirnames, filenames in os.walk(PROJECT_PATH):
        if name in filenames:
            return os.path.join(dirpath, name)

    return ""

# ---------------------------------------------------------------------------
# 重定向输出


class RedirectText(object):
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl
    
    def write(self, string):
        # self.out.WriteText(string)
        wx.CallAfter(self.out.WriteText, string)
        
# ---------------------------------------------------------------------------
# 用于在演示中显示源代码的类。首先尝试在StyledTextCtrl_2示例中使用wxSTC，如果出现错误，
# 则返回到wxTextCtrl，例如stc模块不存在。


class DemoCodeEditor(PythonSTC):
    def __init__(self, parent, style=wx.BORDER_NONE):
        PythonSTC.__init__(self, parent, -1, style=style)
        self.SetUpEditor()
    
    ''' 一些方法使其与wxTextCtrl的使用方式兼容 '''
    def SetValue(self, value):
        # if wx.USE_UNICODE:
            # value = value.decode('iso8859_1')
        #在只读模式?
        ready_only_ori = self.GetReadOnly() #False
        self.SetReadOnly(False)
        self.SetText(value)
        self.EmptyUndoBuffer()  # 删除撤消历史记录
        self.SetSavePoint() # 记录撤消历史记录中的当前位置是保存文档的位置
        self.SetReadOnly(ready_only_ori)
    
    def SetEditable(self, booll):
        self.SetReadOnly(not booll)
    
    def IsModified(self):
        return self.GetModify()
    
    def Clear(self):
        self.ClearAll()
    
    def SetInsertionPoint(self, pos):
        self.SetCurrentPos(pos)
        self.SetAnchor(pos)
    
    def ShowPosition(self, pos):
        line = self.LineFromPosition(pos)
        #self.EnsureVisible(line)
        self.GotoLine(line)
    
    def GetLastPosition(self):
        return self.GetLength()
    
    def GetPositionFromLine(self, line):
        return self.PositionFromLine(line)
    
    def GetRange(self, start, end):
        return self.GetTextRange(start, end)
    
    def GetSelection(self):
        return self.GetAnchor(), self.GetCurrentPos()
    
    def SetSelection(self, start, end):
        self.SetSelectionStart(start)
        self.SetSelectionEnd(end)
    
    def SelectLine(self, line):
        start = self.PositionFromLine(line)
        end = self.GetLineEndPosition(line)
        self.SetSelection(start, end)
    
    def SetUpEditor(self):
        """
                        该方法完成了演示编辑器的设置工作。
                        它是分开的，所以不会使init代码混乱。
        """
        import keyword
    
        self.SetLexer(stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(keyword.kwlist))
    
        # 可以折叠
        self.SetProperty("fold", "1" )
    
        # 突出标签/空格合并(shouldn't be any)
        self.SetProperty("tab.timmy.whinge.level", "1")
    
        # 设置左右边距
        self.SetMargins(2,2)
    
        # 在页边空白处设置数字  - #1
        self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        # 合理的值，例如，4-5位的数字 使用mono字体(40 pix)
        self.SetMarginWidth(1, 40)
    
        # 缩进和制表符（Indentation and tab stuff）
        self.SetIndent(4)               # wx禁止缩进尺寸
        self.SetIndentationGuides(True) # 显示缩进指南
        self.SetBackSpaceUnIndents(True)# 回车取消缩进而不是删除一个空格
        self.SetTabIndents(True)        # Tab键缩进
        self.SetTabWidth(4)             # 将Tab键的可见大小更改为空格字符宽度的倍数
        self.SetUseTabs(False)          # 使用空格而不是制表符
                                        # Tab该抱怨!
                                        
        self.SetViewWhiteSpace(False)   # 不展示空格字符
    
        # EOL: Since we are loading/saving ourselves, and the
        # strings will always have \n's in them, set the STC to
        # edit them that way.
        self.SetEOLMode(stc.STC_EOL_LF) # 设置当前行结束模式。
        self.SetViewEOL(False) # 使行字符的末尾可见或不可见。
    
        # 没有右边缘模式指示器
        self.SetEdgeMode(stc.STC_EDGE_NONE)  #STC_EDGE_LINE
    
        # 设置一个边距来保存折叠标记
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)
    
        # 设置折叠标记
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_BOXPLUSCONNECTED,  "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER,  "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNER,  "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,    "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_BOXPLUS,  "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_BOXMINUS, "white", "black")
    
        # 全局默认样式
        if wx.Platform == '__WXMSW__':
            self.StyleSetSpec(stc.STC_STYLE_DEFAULT,
                              'fore:#000000,back:#FFFFFF,face:Courier New')
        elif wx.Platform == '__WXMAC__':
            # TODO: if this looks fine on Linux too, remove the Mac-specific case
            # and use this whenever OS != MSW.
            self.StyleSetSpec(stc.STC_STYLE_DEFAULT,
                              'fore:#000000,back:#FFFFFF,face:Monaco')
        else:
            defsize = wx.SystemSettings.GetFont(wx.SYS_ANSI_FIXED_FONT).GetPointSize()
            self.StyleSetSpec(stc.STC_STYLE_DEFAULT,
                              'fore:#000000,back:#FFFFFF,face:Courier,size:%d'%defsize)
    
        # 清除样式并还原为默认。
        self.StyleClearAll()
        
        # 下面的样式说明只表明与默认值的不同
        # 剩下的保持不变
        
        # 空白处的行号
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER,'fore:#000000,back:#99A9C2')
        # 强调 brace
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT,'fore:#00009D,back:#FFFF00')
        # 不匹配 brace
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD,'fore:#00009D,back:#FF0000')
        # 缩进指南
        self.StyleSetSpec(stc.STC_STYLE_INDENTGUIDE, "fore:#CDCDCD")
    
        # Python样式    
        self.StyleSetSpec(stc.STC_P_DEFAULT, 'fore:#000000')
        # 注释
        self.StyleSetSpec(stc.STC_P_COMMENTLINE,  'fore:#008000,back:#F0FFF0')
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, 'fore:#008000,back:#F0FFF0')
        # 数字
        self.StyleSetSpec(stc.STC_P_NUMBER, 'fore:#008080')
        # 字符串和字符
        self.StyleSetSpec(stc.STC_P_STRING, 'fore:#800080')
        self.StyleSetSpec(stc.STC_P_CHARACTER, 'fore:#800080')
        # 关键字
        self.StyleSetSpec(stc.STC_P_WORD, 'fore:#000080,bold')
        # 三重引号
        self.StyleSetSpec(stc.STC_P_TRIPLE, 'fore:#800080,back:#FFFFEA')
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, 'fore:#800080,back:#FFFFEA')
        # Class名儿
        self.StyleSetSpec(stc.STC_P_CLASSNAME, 'fore:#0000FF,bold')
        # Function 名儿
        self.StyleSetSpec(stc.STC_P_DEFNAME, 'fore:#008080,bold')
        # 运算符
        self.StyleSetSpec(stc.STC_P_OPERATOR, 'fore:#800000,bold')
        # 标识符。没有写得太粗，因为一切看起来都是这样
        # 如果与上述准则不匹配，则为标识符
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, 'fore:#000000')
    
        # 插入符(脱字符)颜色
        self.SetCaretForeground("BLUE")
        # 选择背景
        self.SetSelBackground(1, '#66CCFF')
    
        self.SetSelBackground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.SetSelForeground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
    # 注册修改后的事件

    def RegisterModifiedEvent(self, eventHandler):
        self.Bind(stc.EVT_STC_CHANGE, eventHandler)

# ---------------------------------------------------------------------------
# 输出重定向类


class RedirectText(object):
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl
    
    def write(self, string):
        # self.out.WriteText(string)
        wx.CallAfter(self.out.WriteText, string)
        
# ---------------------------------------------------------------------------


class MyMenu(wx.MenuBar):
    def __init__(self, parent):
        wx.MenuBar.__init__(self)
        self.parent = parent
        
        self.fileMenu = wx.Menu()
        '''
        self.exitItem = wx.MenuItem(self.fileMenu, id = wx.ID_EXIT, text = "退出\tCtrl+Q")
        self.fileMenu.Append(self.exitItem)
        '''
        self.fileMenu.Append(wx.ID_EXIT, "退出\tCtrl+Q", "退出程序")
        
        # fileMenu.AppendSeparator()
        self.Append(self.fileMenu, "文件")
  
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
    
    def OnExit(self, event):
        self.parent.Close()
        
# ---------------------------------------------------------------------------


class MyStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)
        
        # 状态栏分成3个区域
        self.SetFieldsCount(3)
        # 区域宽度比列，如果你想域的宽度随框架的变化而变化，那么应该使用负值
        self.SetStatusWidths([-2, -2, -1])
        # 大小不变
        self.sizeChanged = False

        # 给状态栏设文字
        self.SetStatusText(" 准备", 0)
        self.SetStatusText("感 谢 使 用 本 工 具 !", 1)
        # 状态栏显示时间    
        self.timer = wx.PyTimer(self.Notify)
        # 1000ms刷新
        self.timer.Start(1000)
        self.Notify()
        
    def Notify(self):
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.SetStatusText(t, 2)

# ---------------------------------------------------------------------------


'''
由于引入多线程后，如果adb连接时间交缠，前端体验不好，未来加入loading提示
'''


class ConnectThread(Thread):
    def __init__(self, newDevInfo, myToolBar): 
        print "正在连接设备 %s......" % newDevInfo
        Thread.__init__(self) 
        self.newDevInfo = newDevInfo
        self.myToolBar = myToolBar
        self.start()  # 开始线程

    def run(self): 
        ''' 连接新设备，正确返回(True, str(正确信息)); 错误返回(TrFalseue, str(错误信息))'''
        r = connectDevice(self.newDevInfo)
        is_ok = r[0]
        message = r[1]
        if is_ok:      
            print "已连接设备 %s......" % self.newDevInfo
        else:
            errDlg2 = wx.MessageDialog(None, message, "错误", wx.OK | wx.ICON_ERROR)
            errDlg2.ShowModal()  
            errDlg2.Destroy()   
            return  
        
        ''' 获取当前连接设备列表，正确则返回 [( str(ip:端口), str(ADB Status), str"设备名称" ), ()......]
                                           错误返回错误消息'''       
        devs = refreshDevices()
#        print devs
        if type(devs) is list:
            print "ADB连接设备列表: ", devs  
        else:
            warnDlg = wx.MessageDialog(None, devs, "错误", wx.OK|wx.ICON_ERROR)
            warnDlg.ShowModal() 
            warnDlg.Destroy()   
            return
        
        self.myToolBar._RefreshToolBar(devs)


ID_ToolBar = wx.ID_HIGHEST + 1


class MyToolBar(aui2.AuiToolBar):      
    def __init__(self, parent):
        aui2.AuiToolBar.__init__(self, parent, -1, wx.DefaultPosition, wx.DefaultSize,
                             agwStyle=aui2.AUI_TB_DEFAULT_STYLE)
        
        self.SetToolBitmapSize(wx.Size(20, 20))
          
        self.bmp0 = images.Refresh.GetBitmap()
        self.bmp1 = images.AndroidDevice.GetBitmap()
#        self.bmp = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16))
#        print "self.bmp : ", type(self.bmp ), self.bmp 
        
        self.tc = wx.TextCtrl(self, value="请输入设备信息 （IP:端口）", size=(200, -1))
        # self.tc.SetFont(font)
            
        # 布局
        self.AddControl(self.tc)     
        self.AddSimpleTool(ID_ToolBar+1, "refresh", self.bmp0, short_help_string="刷新/连接")
        self.AddSeparator()
        # 实现工具栏。添加工具后应调用此函数
        self.Realize()
        
        self.Bind(wx.EVT_TOOL, self.OnUpdateTool, id=ID_ToolBar+1) # aui.EVT_AUITOOLBAR_TOOL_DROPDOWN
        
    def OnUpdateTool(self, event):
        newDevInfo = self.tc.GetValue()
        re = self._CheckNewDevInfo(newDevInfo)
        # 处理新设备信息格式错误
        if re == 1:
            errDlg = wx.MessageDialog(None, "输入格式错误，请重新输入!", "错误", wx.OK|wx.ICON_ERROR)
            errDlg.ShowModal()  
            errDlg.Destroy() 
            return     
        # 无新设备连接，过
        elif re == 0:
            devs = refreshDevices()
            if type(devs) is list:
                print "ADB连接设备列表: ", devs  
            else:
                warnDlg = wx.MessageDialog(None, devs, "错误", wx.OK | wx.ICON_ERROR)
                warnDlg.ShowModal() 
                warnDlg.Destroy()   
                return
    
            self._RefreshToolBar(devs)
        # 处理有新设备连接
        else:
            # 多线程，防connect时GUI界面卡死
            ConnectThread(newDevInfo, self)

    def _CheckNewDevInfo(self, newDevInfo):
        p = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):\d{4,5}$"

        if newDevInfo == "请输入设备信息 （IP:端口）".decode("utf-8") or newDevInfo == "":
            return 0
        
        if not re.match(p, newDevInfo):
            return 1
        
        return 2
    
    '''每次正确获取设备连接信息后，刷新工具条'''
    def _RefreshToolBar(self, devs):
        # 先清空工具条
        count_tools = self.GetToolCount()
#        print count_tools

        if count_tools > 3:
            for i in range(1, count_tools-2):
                # print "删除id:", ID_ToolBar + 1 + i
                self.DeleteTool(ID_ToolBar + 1 + i)
  
        j = 2
        for dev in devs:
            short_help_string = dev[0] + "|" + dev[1] + "|" + dev[2]
#            print "增加id:", ID_ToolBar+j

            self.AddSimpleTool(ID_ToolBar+j, "device %s" % str(j-2), self.bmp1, short_help_string)
            # self.AddSeparator()
            j += 1
        
        self.Realize()


class MyToolBar2(aui2.AuiToolBar):      
    def __init__(self, parent):
        aui2.AuiToolBar.__init__(self, parent, -1, wx.DefaultPosition, wx.DefaultSize,
                             agwStyle=aui2.AUI_TB_DEFAULT_STYLE | aui2.AUI_TB_VERTICAL)
        
        self.play_bmp = images.Play.GetBitmap()
        self.stop_bmp = images.Stop.GetBitmap()
        #布局
        self.AddSimpleTool(ID_ToolBar+100, "play", self.play_bmp, short_help_string="运行脚本")
        self.AddSeparator()
        self.AddSimpleTool(ID_ToolBar+101, "stop", self.stop_bmp, short_help_string="结束脚本")
        
        # 实现工具栏。添加工具后应调用此函数
        self.Realize()
        
        self.Bind(wx.EVT_TOOL, self.OnPlayTool, id=ID_ToolBar+100)
    
    def OnPlayTool(self, event):
        run()
        
# ---------------------------------------------------------------------------


class MyDirTreeCtrl(wx.TreeCtrl):
    def __init__(self, parent, size):
        wx.TreeCtrl.__init__(self, parent, -1, wx.DefaultPosition, 
                           size=size, style=wx.TR_DEFAULT_STYLE, )          
        # 图像处理
        self.iconEntries = {}
        # self.iconEntries["default"] = -1
        # self.iconEntries["directory"] = -1
        self.imagelist = wx.ImageList(16,16)

        self.AddIcon2(images.Folder.GetBitmap(), "directory")
        self.AddIcon2(images.Page.GetBitmap(), "default")
        self.AddIcon2(images.Exe.GetBitmap(), ".exe")
        self.AddIcon2(images.Rar.GetBitmap(), ".rar")
        self.AddIcon2(images.Rar.GetBitmap(), ".zip")
        self.AddIcon2(images.PyIcon.GetBitmap(), ".py")
        self.AddIcon2(images.Excel.GetBitmap(), ".xls")
        self.AddIcon2(images.Excel.GetBitmap(), ".xlsx")
        self.AddIcon2(images.HTML.GetBitmap(), ".html")
        self.AddIcon2(images.TXT.GetBitmap(), ".txt")
        self.AddIcon2(images.Word.GetBitmap(), ".docx")
        
        
        '''设置正常图像列表。二者区别：
        SetImageList - The image list assigned with this method will not be deleted by wx.TreeCtrl‘s 
        destructor, you must delete it yourself；
        AssignImageList - Image list assigned with this method will be automatically deleted by wx.TreeCtrl 
        as appropriate (i.e. it takes ownership of the list).'''
        self.AssignImageList(self.imagelist)
        # self.SetImageList(self.imagelist)
        
        # self.ExpandAll() # 展开树中的所有项目。
      
    def AddIcon(self, filePath, name, wxBitmapType = None):
        '''将图标添加到imagelist，并注册到iconEntries dict
                    使用给定的名称。使用，这样您就可以为树分配自定义图标
                    通过传递存储在self.iconentries [name]中的值
        @param filepath:图像的路径
        @param wxBitmapType:文件类型的wx常量-例如wx.BITMAP_TYPE_PNG
        @param name:在self中用作键的名称。iconEntries dict -获取你的imagekey通过调用
        self.iconEntries[名称]
        '''
        try:
            if os.path.exists(filePath):     
                image = self.imagelist.Add(wx.Bitmap(filePath, wxBitmapType))
#                print type(image), image
                self.iconEntries[name] = image
        except Exception, e:
            # print e
            pass
        
    def AddIcon2(self, bitMap, name):
        image = self.imagelist.Add(bitMap)
        self.iconEntries[name] = image
              
    def SetRootDir(self, dire): 
        if not os.path.isdir(dire):
            raise Exception("%s 不是一个文件夹" % dire)
        
        # 删除控件中的所有项目
        self.DeleteAllItems()
        
        # 文件夹路径作为根节点
        self.root = self.AddRoot(dire)
#        print self.GetItemText(self.root)
        self.SetItemImage(self.root, self.iconEntries["directory"])
        self._LoadDir(self.root, dire)
        # 展开给定项目
        self.Expand(self.root)
               
    def _LoadDir(self, item, directory):
        """用于加载文件列表的私有函数;对于给定的目录，并将项追加到树中。
        
        @note: 如果节点已经有子节点，则不添加项"""
        excluded = [".pyc"]
        # 返回分支中的项目数
        if self.GetChildrenCount(item) == 0:
            # 获取文件夹下所有文件
            files = os.listdir(directory)
            # print "files:", type(files), files
            
            files = self.Sort(files[:])
            # 向树中添加节点
            for f in files:
                # 获取文件扩展名
                ext = self.GetFileExtension(f)
                ext = ext.lower()
                
                # 部分文件不做处理
                if f[0] == "." or ext in excluded:
                    continue              
                 
#                print "f:", type(f), f                       
#                print "Path: ", directory, f, os.path.join(directory, f)

                # 处理文件扩展名以构建映像列表
                ima = self.ProcessFileExtension(os.path.join(directory, f), ext)        
                # 如果是文件夹，告诉树它有子目录
                if os.path.isdir(os.path.join(directory, f)):
                    # 将项目追加到父项标识的分支的末尾，返回新的项目ID。
                    child = self.AppendItem(item, f, image = ima) 
                    # 强制显示项目旁边的按钮。
                    self.SetItemHasChildren(child, True)
                    self.SetItemImage(child, self.iconEntries["directory"])
                    
#                    print self.GetItemText(child)
                    self._LoadDir(child, os.path.join(directory, f))
                else:
                    # 如果不是文件夹，直接添加子项目
                        self.AppendItem(item, f, image = ima)
            
                     
    # 获取文件扩展名
    def GetFileExtension(self, fileName):
        if not os.path.isdir(fileName):
            ''' find() 是从字符串左边开始查询子字符串匹配到的第一个索引;
                rfind()是从字符串右边开始查询字符串匹配到的第一个索引,找不到返回-1'''
            point_index = fileName.rfind('.')
            if point_index > -1:
                return fileName[point_index:]
            return ""
        else:
            return "directory"
        
    def ProcessFileExtension(self, fileName, ext):
            """Helper函数。要求文件和收集所有必要的图标进入图像列表，每次都重新传递到树
                (imagelists是处理图像的蹩脚方法)"""
            # print "ext: %s" % ext
            excluded = ["", ".ico", ".png"]
            # 如果没有扩展名或者不在excluded中，则不做处理
            if ext not in excluded:
                if ext not in self.iconEntries.keys():            
                    try: # 防止崩溃
                        # 使用mimemanager获取文件类型和图标
                        filetype = wx.MimeTypesManager.GetFileTypeFromExtension(ext)
                        print type(filetype), filetype
    
                        if hasattr(filetype, 'GetIconInfo'):
                            info = filetype.GetIconInfo()                          
                            if info is not None:
                                icon = info[0]
                                if icon.Ok():
                                    # add to imagelist and store returned key
                                    image = self.imagelist.AddIcon(icon)
                                    self.iconEntries[ext] = image
                                    
                                    # update tree with new imagelist - inefficient
                                    self.AssignImageList(self.imagelist)
    
                                    # return new key
                                    return image
                    except:
                        return self.iconEntries['default']
                            
                else:
                    return self.iconEntries[ext]
                
            elif ext == ".ico":
                try:
                    icon = wx.Icon(fileName, wx.BITMAP_TYPE_ICO)
                    if icon.IsOk():
                        return self.imagelist.Add(icon)
                except Exception, e:
                    # print e
                    return self.iconEntries['default']
            
            elif ext == ".png":
                try:
                    icon = wx.Icon(fileName, wx.BITMAP_TYPE_PNG)
                    if icon.IsOk(): # 如果图标数据存在则返回True
                        return self.imagelist.Add(icon)
                except Exception, e:
                    # print e
                    return self.iconEntries['default']
    
            return self.iconEntries['default']
    
    def Sort(self, old_list):
        folder_list = []
        file_list = []
        unknown_list = []
        for f in old_list:
            ext = self.GetFileExtension(f).lower()
            if ext == "directory":
                folder_list.append(f)
            elif ext == "":
                unknown_list.append(f)
            else:
                file_list.append(f)
        folder_list = sorted(folder_list, self.cmp_ignore_case)
        file_list = sorted(file_list, self.cmp_ignore_case)
        unknown_list = sorted(unknown_list, self.cmp_ignore_case)
        
        new_list = folder_list + file_list + unknown_list
        # print "new_list:", new_list
        return new_list
    
    def cmp_ignore_case(self, s1, s2):
        u1 = s1.upper()
        u2 = s2.upper()
        if u1 < u2:
            return -1
        if u1 > u2:
            return 1
        return 0
    
# ---------------------------------------------------------------------------


class MyNotebook(wx.Notebook):
    def __init__(self, parent, idd, style):      
        wx.Notebook.__init__(self, parent, id=idd, style=style)  


class MyLogNotebook(wx.Notebook):
    def __init__(self, parent, idd, style):      
        wx.Notebook.__init__(self, parent, id=idd, style=style)  

# ---------------------------------------------------------------------------


class UITestFrame(wx.Frame):
    def __init__(self, idd, title, size):
        wx.Frame.__init__(self, None, idd, title, size=size) 
        
        self.width = size[0]
        self.high = size[1]
        
        # 告诉主界面，现在由AuiManager进行布局
        self._mgr = aui2.AuiManager()
        self._mgr.SetManagedWindow(self)
        
        # 设置窗口左上角图标
        self.SetIcon(images.Logo.GetIcon())
#        self.icon = wx.Icon("bmp_source/logo.ico", wx.BITMAP_TYPE_ICO)
#        print type(self.icon)
           
        # 初始化UI
        self.__InitUI()     
        '''程序员将窗格添加到类中，或者更改现有窗格属性（停靠位置，浮动状态，显示状态等）。 
        要应用这些更改，请使用 wx.aui。调用AuiManager的Update 函数。通过一次修改多个窗格，
        然后通过调用一次“提交”所有更改，可以使用此批处理来避免闪烁'''
        self._mgr.Update()    
        
        # 处理左侧目录树，单击事件（其实时树中选中元素改变后的事件）
        self.fileTreePanel.dirTreeCtrl.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)  # 双击事件EVT_TREE_ITEM_ACTIVATED
        
        # 打印重定向到self.logger
        redir = RedirectText(self.logger)
        sys.stdout = redir
         
    def __InitUI(self):  
        self.SetMinSize(wx.Size(500, 500))
            
        # 创建上方菜单栏
        self.menuBar = MyMenu(self)
        self.SetMenuBar(self.menuBar)
        
        # 创建下方状态栏
        self.statusBar = MyStatusBar(self)
        self.SetStatusBar(self.statusBar)
        
        # 创建左上方设备连接状态工具栏
        self.deviceToolBar = MyToolBar(self)     
        
        # 创建右上方运行工具工具栏
        self.playBar = MyToolBar2(self)    

        # 创建左侧文件目录树面板
        self.fileTreePanel = MyFileTreePanel(self, (self.width*0.15, self.high*0.7))
        
        # 创建右侧 Notebook
        self.nootBook = MyNotebook(self, -1, style=wx.CLIP_CHILDREN)
        # 设置图标
        imgList_nootBook = wx.ImageList(16, 16) 
        imgList_nootBook.Add(images.PyIcon.GetBitmap())
        imgList_nootBook.Add(images.Excel.GetBitmap())
        imgList_nootBook.Add(images.Report.GetBitmap())
        self.nootBook.AssignImageList(imgList_nootBook)     
                
        self.codePage = MyCodePage(self.nootBook, (self.width*0.85, self.high*0.75))
        self.casePage = MyCasePage(self.nootBook, (self.width*0.85, self.high*0.75))
        self.reportPage = MyReportPage(self.nootBook, (self.width*0.75, self.high*0.75))
                  
        self.nootBook.AddPage(self.codePage, "Python代码", True, imageId=0)
        self.nootBook.AddPage(self.casePage, "用例同步", False, imageId=1)
        self.nootBook.AddPage(self.reportPage, "测试报告", False, imageId=2)
        
        # 创建下方日志 窗口
        self.logger = wx.TextCtrl(self, size=(self.width, self.high*0.25),
                                      style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        
        self.userAction = wx.TextCtrl(self, size=(self.width, self.high*0.25),
                                      style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
   
        # AUI管理
        self._mgr.AddPane(self.deviceToolBar, aui2.AuiPaneInfo().
                          Name("deviceToolBar").Caption("设备连接状态").
                          ToolbarPane().Top().Row(1))
        
        self._mgr.AddPane(self.playBar, aui2.AuiPaneInfo().
                          Name("playBar").ToolbarPane().Right())
        
        self._mgr.AddPane(self.fileTreePanel, aui2.AuiPaneInfo().
                          Name("fileTreePanel").Caption("工程目录").
                          Left().MinSize((200, -1)).
                          Floatable(False))
        
        self._mgr.AddPane(self.nootBook, aui2.AuiPaneInfo().
                         Name("Notebook").CenterPane())
        
        self._mgr.AddPane(self.userAction, aui2.AuiPaneInfo().
                         Name("userAction").Caption("用户操作记录").Bottom())        
        
        self._mgr.AddPane(self.logger, aui2.AuiPaneInfo().
                         Name("logger").Caption("系统行为日志").Bottom(), target=self._mgr.GetPane("userAction"))

    def OnSelChanged(self, event):  
        tree = self.fileTreePanel.dirTreeCtrl
        item = event.GetItem()
        itemText = tree.GetItemText(item)
#        print(itemText) 
        if itemText.endswith(".py"):
            self.codePage.st.SetLabel(itemText)
            self.codePage.LoadPySource(itemText)  
            self.nootBook.SetSelection(0)
        elif itemText.endswith(".html"):
            self.reportPage.ShowLocalHtml(itemText)
            self.nootBook.SetSelection(2)
        else:
            return
 
# ---------------------------------------------------------------------------


class MyCodePage(wx.Panel):
    def __init__(self, parent, size):
        wx.Panel.__init__(self, parent, size=size)
        
        self.st = wx.StaticText(self, label="代码")
        
        '''self.codeTextCtrl = wx.TextCtrl(self, -1, style =
                                 wx.TE_MULTILINE | wx.HSCROLL | 
                                 wx.TE_RICH2 | wx.TE_NOHIDESEL)'''
        
        self.codeTextCtrl = DemoCodeEditor(self)
       
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.st, 0, wx.EXPAND)
        self.vbox.Add(self.codeTextCtrl, 1, wx.EXPAND)
        self.SetSizer(self.vbox)

    def LoadPySource(self, pyName):    
        filename = GetOriginalFilename(pyName)
        if os.path.exists(filename):
            # print "Loading demo %s..." % pyName
            # self.PyModules = PyModules(pyName)
            f = open(filename, "rt")
            source = f.read()
            f.close() 
            
            self.ShowPySource(source)        
        else:
            raise Exception("没有找到python文件 %s" % pyName.encode("utf-8"))
        
    # 从DemoModules对象加载演示
    def ShowPySource(self, source):
        self.codeTextCtrl.Clear()
        self.codeTextCtrl.SetValue(source)
        self.JumpToLine(0)
      
    def JumpToLine(self, line, highlight=False):
        self.codeTextCtrl.GotoLine(line)
        self.codeTextCtrl.SetFocus()
        if highlight:
            self.codeTextCtrl.SelectLine(line)

# ---------------------------------------------------------------------------


class MyCasePage(wx.Panel):
    def __init__(self, parent, size):
        wx.Panel.__init__(self, parent, size=size)
        
        self.sheetNames = []
        self.pbtns = []
        
        # 布局
        self.__DoLayout()
        
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.AddMany([(self.p1, 2, wx.EXPAND),
                       (self.p2, 1, wx.EXPAND)])
        self.SetSizer(vsizer)
        self.SetAutoLayout(True)
        
    def __DoLayout(self):
        self.p1 = wx.Panel(self) 
        self.p1.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.p2 = wx.Panel(self) 
       
        self.__LayoutPanel1(self.p1, "功能模块: ")
        self.__LayoutPanel2(self.p2, "操作: ")
    
    def __LayoutPanel1(self, panel, label):
        guide = images.Guide.GetBitmap()
        build = images.Building.GetBitmap()
        album = images.Album.GetBitmap()
        shop = images.Shop.GetBitmap()
        task = images.Task.GetBitmap()
        jslb = images.JueSeLieBiao.GetBitmap()
        clg = images.ChenLieGui.GetBitmap()
        pve = images.PVE.GetBitmap()
        
        guide.SetSize((64, 64)) 
        build.SetSize((64, 64))     
        album.SetSize((64, 64))
        shop.SetSize((64, 64))
        task.SetSize((64, 64))
        jslb.SetSize((64, 64))
        clg.SetSize((64, 64))
        pve.SetSize((64, 64))

        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer1.Add((15, 15))
        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer2.Add((15, 15))
        
        # 按钮样式
        default = platebtn.PB_STYLE_DEFAULT
        toggle = default | platebtn.PB_STYLE_TOGGLE | platebtn.PB_STYLE_GRADIENT
   
        '''        
        row = col = i = 0
        for case in CASE_TO_SHEET.keys():
            if col == 7:
                col = 0
                row += 1
            self.caseButtons.append(wx.ToggleButton(self, label=case, size=(60, 30)))
            grid.Add(self.caseButtons[i], pos=(row, col), flag=wx.CENTER)
            self.Bind(wx.EVT_TOGGLEBUTTON, self.caseButtonEve, self.caseButtons[i])
            col += 1
            i  += 1
        '''
        ''' @Note: 增加buttons后，同时增加全局变量 CASE_TO_SHEET'''
        buttons = [  # (0bmp,   1label,     2Style, 3Color, 4Enable)
                     (guide, "新手引导", toggle, None,  True),
                     (build, "城建", toggle, wx.Colour(245, 55, 245),  True),
                     (album, "图鉴", toggle, None,  True),
                     (shop, "商店", toggle, wx.Colour(245, 55, 245),  True),
                     (task, "任务", toggle, None,  True),
                     (jslb, "角色列表", toggle, wx.Colour(245, 55, 245),  True),
                     (clg, "陈列柜", toggle, None,  True),
                     (pve, "PVE", toggle, wx.Colour(245, 55, 245),  True),
                         ]
        
        for btn in buttons:
            
            pbtn = platebtn.PlateButton(panel, wx.ID_ANY, btn[1], btn[0], style=btn[2])   
            self.pbtns.append(pbtn)
            
            if buttons.index(btn) < 5:
                psizer = hsizer1
            elif buttons.index(btn) < 10:
                psizer = hsizer2
            
            if btn[3] is not None:
                pbtn.SetPressColor(btn[3])
            
            # tbtn.Bind(platebtn.EVT_PLATEBTN_DROPARROW_PRESSED, self.OnDropArrowPressed)
            pbtn.Bind(wx.EVT_TOGGLEBUTTON, self.OnPlateButton)

            pbtn.Enable(btn[4])

            psizer.Add(pbtn, 0, flag=wx.EXPAND | wx.LEFT, border=10)
            
        txt_sz = wx.BoxSizer(wx.HORIZONTAL)
        txt_sz.AddMany([((5, 5)), (wx.StaticText(panel, label=label), 0, wx.ALIGN_LEFT)])

        vsizer.AddMany([((10, 10)),
                        (txt_sz, 0, wx.ALIGN_LEFT),
                        ((10, 10)), (hsizer1, 0, wx.EXPAND), ((10, 10)),
                        (hsizer2, 0, wx.EXPAND), ((10, 10))])
    
        panel.SetSizer(vsizer)
    
    def __LayoutPanel2(self, panel, label):
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        '''
        self.resetButton = wx.Button(panel, label="重置", size=(60, 30))
        self.resetButton.Disable() 
        self.Bind(wx.EVT_BUTTON, self.resetButtonEve, self.resetButton)
        '''
        self.synButton = wx.Button(panel, label="同步", size=(60, 30))
        self.synButton.Disable() 
        self.Bind(wx.EVT_BUTTON, self.synButtonEve, self.synButton)        
        
        txt_sz = wx.BoxSizer(wx.HORIZONTAL)
        txt_sz.AddMany([((5, 5)), (wx.StaticText(panel, label=label), 0, wx.ALIGN_LEFT)]) 
        
        # hsizer.Add(self.resetButton, 0, flag=wx.EXPAND|wx.LEFT, border=10)
        hsizer.Add(self.synButton, 0, flag=wx.EXPAND|wx.LEFT, border=10)
        
        vsizer.AddMany([((10, 10)),
                        (txt_sz, 0, wx.ALIGN_LEFT),
                        ((10, 10)), (hsizer, 0, wx.EXPAND), ((10, 10))])
    
        panel.SetSizer(vsizer)
    
    def OnPlateButton(self, event):
        # print "BUTTON CLICKED: Id: %d, Label: %s" % (event.GetId(), event.GetEventObject().LabelText)
                    
        btn_label = event.GetEventObject().GetLabel().encode("utf-8")
        
        if event.GetEventObject().IsPressed():
            self.sheetNames.append(CASE_TO_SHEET[btn_label])
        else:
            self.sheetNames.remove(CASE_TO_SHEET[btn_label])   
#        print self.sheetNames
        
        if len(self.sheetNames) != 0:
            self.synButton.Enable() 
        else:
            self.synButton.Disable() 
            # self.resetButton.Disable()
    '''  @Note: wx.lib.platebtn.PlateButton没有找到切换按钮状态的方法
    def resetButtonEve(self, event): 
        for pbtn in self.pbtns:
            if pbtn.IsPressed():
                
        self.sheetNames = []
        self.synButton.Disable() 
        event.GetEventObject().Disable() 
    '''
            
    def synButtonEve(self, event): 
        confirmDlg = wx.MessageDialog(None, "同步会将用例表中的内容覆盖到对应py文件.\n同步前，请确认表中内容和格式符合编写规范!", "请确认", wx.YES_NO|wx.NO_DEFAULT|wx.ICON_INFORMATION)
        if confirmDlg.ShowModal() == wx.ID_YES:
            confirmDlg.Destroy() 
            xlsToPy0(self.sheetNames)
        else:        
            confirmDlg.Destroy()  

# ---------------------------------------------------------------------------


class MyReportPage(wx.Panel):
    def __init__(self, parent, size):
        wx.Panel.__init__(self, parent, size=size)
        self.wv = webview.WebView.New(self)
        
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.wv, 1, wx.EXPAND)
        self.SetSizer(sizer)
    
    def ShowLocalHtml(self, htmlName):
        local_html_path = GetOriginalFilename(htmlName)
        print "local_html_path: ", local_html_path
        self.wv.LoadURL(local_html_path)
        # self.wv.Reload()
        
       
# ---------------------------------------------------------------------------
   
class MyFileTreePanel(wx.Panel):    
    def __init__(self, parent, size):
        wx.Panel.__init__(self, parent, size=size) 
        self.size = size
        
        self.dirTreeCtrl = MyDirTreeCtrl(self, self.size)
        self.dirTreeCtrl.SetRootDir(PROJECT_PATH)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.dirTreeCtrl, 1, wx.EXPAND)

# ---------------------------------------------------------------------------

    '''
    def openXlsButtonEve(self, event): 
        path = "UITestCase.xls"
        if not os.path.exists(path):
            errDlg = wx.MessageDialog(None, "没有找到文件 %s"%path, "错误", wx.OK|wx.ICON_ERROR)
            errDlg.ShowModal()  
            errDlg.Destroy() 
        else:
            os.startfile(path) 
            #event.GetEventObject().Disable()
            #event.GetEventObject().Enable()'''

def MyFrame():
    app = wx.App()
#   app = wx.PySimpleApp(redirect=True)
    
    title = "UI 自动化测试"
    
    ds = wx.DisplaySize()
    screenWidth = ds[0]
    screenHigh = ds[1]
    w = screenWidth
    h = screenHigh * 0.95
    
    frame = UITestFrame(wx.ID_ANY, title, (w, h))
    frame.CenterOnScreen()
    frame.Show()
    
    app.MainLoop()
    
if __name__ == '__main__':
    MyFrame()
