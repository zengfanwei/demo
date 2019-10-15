#coding:utf-8

from wx.tools import img2py

command_lines = [
    "-F -i -n Logo bmp_source/logo.ico images.py", 
    
    "-a -F -n AndroidDevice bmp_source/androidDevice.png images.py",
    "-a -F -n Excel bmp_source/excel.png images.py",
    "-a -F -n Exe bmp_source/exe.png images.py",
    "-a -F -n Folder bmp_source/folder.png images.py",
    "-a -F -n Page bmp_source/page.png images.py",
    "-a -F -n PyIcon bmp_source/py.png images.py",
    "-a -F -n Rar bmp_source/rar.png images.py",
    "-a -F -n Refresh bmp_source/refresh.png images.py",
    "-a -F -n HTML bmp_source/html.png images.py",
    "-a -F -n TXT bmp_source/txt.png images.py",
    "-a -F -n Word bmp_source/word.png images.py",
    "-a -F -n Play bmp_source/play.png images.py",
    "-a -F -n Stop bmp_source/stop.png images.py",
    "-a -F -n Report bmp_source/report.png images.py",
    
    "-a -F -n Building bmp_source/building.png images.py",
    "-a -F -n Album bmp_source/album.png images.py",
    "-a -F -n Shop bmp_source/shop.png images.py",
    "-a -F -n Guide bmp_source/guide.png images.py",
    "-a -F -n Task bmp_source/task.png images.py",
    "-a -F -n JueSeLieBiao bmp_source/jueseliebiao.png images.py",
    "-a -F -n ChenLieGui bmp_source/chenliegui.png images.py",
    "-a -F -n PVE bmp_source/pve.png images.py",

    
    ]

if __name__ == "__main__":
    for line in command_lines:
        args = line.split()
        img2py.main(args)