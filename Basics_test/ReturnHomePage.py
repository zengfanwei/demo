# coding=utf-8

import sys
import time
from poco.drivers.unity3d import UnityPoco
poco = UnityPoco()

def Return(page):
    # 商店界面
    if 'shopInterface' == page:
        poco('btn_back').click()
    # 商店购买确认弹窗\金币、钻石不足提示弹窗
    elif 'purchase_popup' == page:
        poco('btn_cancel').click()
        poco('btn_back').click()
    # 开启礼盒界面1
    elif 'openbox1_interface' == page:
        poco('label_cishu').click()
        time.sleep(8.0)
        poco('label_cishu').click()
        time.sleep(8.0)
        poco('label_cishu').click()
        time.sleep(8.0)
        poco('label_cishu').click()
        time.sleep(8.0)
        poco('label_cishu').click()
        time.sleep(5.0)
        poco('label_ok').click()
        poco('btn_back').click()
    # 开启礼盒界面2
    elif 'openbox2_interface' == page:
        poco('label_cishu').click()
        time.sleep(8.0)
        poco('label_cishu').click()
        time.sleep(8.0)
        poco('label_cishu').click()
        time.sleep(8.0)
        poco('label_cishu').click()
        time.sleep(5.0)
        poco('label_ok').click()
        poco('btn_back').click()
    # 开启礼盒界面3
    elif 'openbox3_interface' == page:
        poco('label_cishu').click()
        time.sleep(8.0)
        poco('label_cishu').click()
        time.sleep(8.0)
        poco('label_cishu').click()
        time.sleep(5.0)
        poco('label_ok').click()
        poco('btn_back').click()
    # 开启礼盒界面4
    elif 'openbox4_interface' == page:
        poco('label_cishu').click()
        time.sleep(8.0)
        poco('label_cishu').click()
        time.sleep(5.0)
        poco('label_ok').click()
        poco('btn_back').click()
    # 开启礼盒界面5
    elif 'openbox5_interface' == page:
        poco('label_cishu').click()
        time.sleep(5.0)
        poco('label_ok').click()
        poco('btn_back').click()
    # 礼盒结算界面
    elif 'settleInterface' == page:
        poco('label_ok').click()
        poco('btn_back').click()
    #图鉴分享弹窗
    elif 'album_share' == page:
        poco('btn_close').click()
        poco('btn_back').click()
    else:
        pass
