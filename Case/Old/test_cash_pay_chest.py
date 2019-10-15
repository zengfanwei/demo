# coding=utf-8

import sys
sys.path.insert(0, 'D:\workspace\UITest_TsumTsum\Basics_test')
from Config_test import CASE_EXCEL_PATH, LocalAddress
from BasicFunction import GetMeta, GetCase, GetText, GetErrorPage, Click, ChildClick, checkTwoL, checkTextEqual
from ReturnHomePage import Return
from functions import getValDicFromXml
from batchAccessControlInfo import accessControlInfo
from GameData import updateData, queryData
from getFamilyTsum import familyTsum


import unittest
from airtest.core.api import *
from poco.drivers.unity3d import UnityPoco
import json
import os

caseList = GetCase(CASE_EXCEL_PATH, 'shop_cash_pay_chest')
ShopPrice = getValDicFromXml('shop.xml', 'costs', 'extends', 'fillCosts')
Tsums = getValDicFromXml('tsum.xml', 'name', 'id')
Stars = getValDicFromXml('tsum.xml', 'id', 'star')
Exps = getValDicFromXml('tsum_levelup.xml', 'star', 'level', 'nextExp')
Puzzles = getValDicFromXml('tsum.xml', 'name', 'puzzle')
Uid = '12011'
UserLevel = queryData(Uid, 'User', 'level')
TextDic = GetText(LocalAddress, 'text.xlsx')
logic1 = 'Shop'
logic2 = 'User'
logic3 = 'Props'
data1 = '''{
      "uid": 12011,
      "cdMap": {
        "1": {
      "cdMillis": 86400000,
      "cdUpdateTime": 2568792580800,
      "cdPaused": false
    },
    "2": {
      "cdMillis": 83207602,
      "cdUpdateTime": 2568792580800,
      "cdPaused": false
    }
      },
      "recordMap": {
        "2": [
          {
            "items": [
              {
                "itemId": 2,
                "num": 1
              }
            ],
            "gachaTime": 1568280860974
          }
        ]
      },
      "dailyRefreshTime": 0,
      "qualifyPointShopItemModels": [],
      "tsumShopItems": [
        {
          "tsumId": 4,
          "num": 1,
          "sold": false
        },
        {
          "tsumId": 14,
          "num": 1,
          "sold": false
        }
      ],
      "tsumShopRefreshTime": 0,
      "appearedTsums": [
        4,
        14
      ],
      "tsumShopLastUpdateTs": 1568280857158,
      "newPlayerSpecialTsumIds": [
        2,
        14
      ]
    }'''
data2 = '''{
  "uid": 12011,
  "coin": 8100,
  "energy": 72,
  "cash": 4700,
  "level": 1,
  "updateTime": 1568617137369,
  "tsumId": 0,
  "material": 46,
  "createTime": 1559673353079,
  "lastLoginTime": 1568617137367,
  "continueLoginDays": 1,
  "activeDays": 5,
  "coinLimit": 10500,
  "qualifyingPoint": 2000,
  "newbie": false
}'''
data3 = '''{
  "uid": 12011,
  "propMap": {
    "1011": {
      "itemId": 1011,
      "num": 0
    },
    "1012": {
      "itemId": 1012,
      "num": 0
    }
  }
}'''
updateData(Uid, logic1, data1)
updateData(Uid, logic2, data2)
updateData(Uid, logic3, data3)
start_app('com.tencent.TsumTsumAndroid')
if wait(Template(r"D:\\workspace\\UITest_TsumTsum\\Case\\photo\\tpl1568629745795.png", record_pos=(-0.008, 0.872), resolution=(1080, 2160)),interval=2):
    poco = UnityPoco()

class ShopCashPayChest(unittest.TestCase):

    def test_A1(self):
        u"""测试在开一盒礼券不足弹窗点击购买按钮，播放开礼盒动画"""
        poco('btn_chest').click()
        sleep(1.0)
        poco('btn_buy_one').click()
        sleep(1.0)
        poco('label_confirm').click()
        sleep(1.0)
        poco('label_confirm').click()
        poco("label_cishu").wait()
        self.assertTrue(poco('ChestRewardPanel').exists(), caseList[0])

    def test_A2(self):
        u"""测试开礼盒界面显示的礼盒数为1"""
        count = poco("label_cishu").get_text()
        self.assertEqual('1', count, caseList[1])

    def test_A3(self):
        u"""测试点击屏幕开启礼盒，礼盒数量减1"""
        poco('label_cishu').click()
        poco('c2_progress_top').wait()
        count = poco("label_cishu").get_text()
        self.assertEqual('0', count, caseList[2])

    def test_A4(self):
        u"""测试开出来的松松在礼盒掉落池中"""
        global UserLevel

        name = poco('label_name').get_text().replace('的碎片', '')
        allTsum = familyTsum(UserLevel)[0]
        self.assertTrue(name in allTsum, caseList[3])

    def test_A5(self):
        u"""测试开出来的松松等级显示正确"""
        global Uid, Tsums

        level = poco("label_level").get_text().replace('级', '')
        name = poco('label_name').get_text().replace('的碎片', '')
        backLevel = str(queryData(Uid, 'Tsums', 'tsumMap')[Tsums[name]]['level'])
        self.assertEqual(level, backLevel, caseList[4])

    def test_A6(self):
        u"""测试开出来的松松进度条显示正确"""
        global Uid, UserLevel, Tsums, Stars, Exps

        sleep(1.0)
        progressBar = poco("label_progress").get_text()
        name = poco('label_name').get_text().replace('的碎片', '')
        exp = str(queryData(Uid, 'Tsums', 'tsumMap')[Tsums[name]]['exp'])
        nextExp = Exps[Stars[Tsums[name]]][str(UserLevel)]
        self.assertEqual(progressBar, exp + '/' + nextExp, caseList[5])

    def test_A7(self):
        u"""测试开完礼盒回到礼盒界面"""
        poco('label_cishu').click()
        poco('btn_buy_one').wait()
        self.assertTrue(poco('tabbar_shop').exists(), caseList[6])

    def test_A8(self):
        u"""测试在十连抽礼券不足弹窗点击购买按钮，播放开礼盒动画"""
        poco('btn_buy_ten').click()
        sleep(1.0)
        poco('label_confirm').click()
        sleep(1.0)
        poco('label_confirm').click()
        poco("label_cishu").wait()
        self.assertTrue(poco('ChestRewardPanel').exists(), caseList[7])

    def test_A9(self):
        u"""测试开礼盒界面显示的礼盒数为10"""
        count = poco("label_cishu").get_text()
        self.assertEqual('10', count, caseList[8])

    def test_B1(self):
        u"""测试点击屏幕开启礼盒，礼盒数量减1"""
        global Uid, UserLevel, Tsums, Stars, Exps, Puzzles

        allTsum = familyTsum(UserLevel)[0]
        poco('label_cishu').click()
        for i in xrange(10):
            oldCount = int(poco('label_cishu').get_text())
            wait(Template(r"D:\\workspace\\UITest_TsumTsum\\Case\\photo\\tpl1568971097645.png", record_pos=(0.119, 0.695), resolution=(1080, 2160)))
            #poco('label_progress').wait()
            newCount = int(poco('label_cishu').get_text())
            if '的碎片' not in poco('label_name').get_text():
                level = poco("label_level").get_text().replace('级', '')
                name = poco('label_name').get_text().replace('的碎片', '')
                progressBarNum = int(poco("label_progress").get_text().split('/')[0])
                progressBarNext = poco("label_progress").get_text().split('/')[1]
                backLevel = str(queryData(Uid, 'Tsums', 'tsumMap')[Tsums[name]]['level'])
                exp = queryData(Uid, 'Tsums', 'tsumMap')[Tsums[name]]['exp']
                nextExp = Exps[Stars[Tsums[name]]][str(UserLevel)]
                self.assertEqual(newCount, oldCount - 1, caseList[9])
                self.assertTrue(name in allTsum, caseList[10])
                self.assertEqual(level, backLevel, caseList[11])
                self.assertTrue(progressBarNum <= exp, caseList[12])
                self.assertEqual(progressBarNext, nextExp, caseList[12])
            else:
                name = poco('label_name').get_text().replace('的碎片', '')
                progressBarNum = int(poco("label_progress").get_text().split('/')[0])
                progressBarNext = poco("label_progress").get_text().split('/')[1]
                exp = queryData(Uid, 'Props', 'propMap')[Puzzles[name].split('#')[0]]['num']
                nextExp = Puzzles[name].split('#')[1]
                self.assertEqual(newCount, oldCount - 1, caseList[9])
                self.assertTrue(name in allTsum, caseList[10])
                self.assertFalse(poco('label_level').exists(), caseList[11])
                self.assertTrue(progressBarNum <= exp, caseList[12])
                self.assertEqual(progressBarNext, nextExp, caseList[12])
            poco('label_progress').click()

    def test_B2(self):
        u"""测试开完十次礼盒显示获得界面"""
        poco('c2_small').wait()
        self.assertTrue(poco('label_get_ten').exists(), caseList[13])

    def test_B3(self):
        u"""测试获得界面显示的豪华礼券数正确"""
        global Uid

        backNum = str(queryData(Uid, 'Props', 'propMap')['1012']['num'])
        couponCount = poco("label_ticket").get_text()
        self.assertEqual(couponCount, '拥有豪华礼券:' + backNum, caseList[14])

    def test_B4(self):
        u"""测试点击确认按钮，回到礼盒界面"""
        poco('label_ok').click()
        poco('btn_buy_one').wait()
        self.assertFalse(poco('OpenChestComp').exists(), caseList[15])

    def test_B5(self):
        u"""测试点击再抽十次，弹出礼券不足弹窗"""
        poco('btn_buy_ten').click()
        sleep(1.0)
        poco('label_confirm').click()
        sleep(1.0)
        poco('label_confirm').click()
        sleep(1.0)
        poco('label_cishu').click()
        while poco('label_cishu').exists():
            if poco('tex_title').exists():
                break
            else:
                poco('label_cishu').click()
        poco('label_get_ten').wait()
        sleep(2.0)
        poco('label_get_ten').click()
        poco('c2_main').wait()
        self.assertTrue(poco('PromptPopupPanel').exists(), caseList[16])

    def test_B6(self):
        u"""测试礼券不足弹窗的文案显示正确"""
        global TextDic

        luxuryChestPrice = 0
        luxuryCouponPrice = 0
        for i in ShopPrice.keys():
            if '1012' in i:
                luxuryChestPrice = int(ShopPrice[i].keys()[0].split('#')[1])
                luxuryCouponPrice = ShopPrice[i]['2000#' + str(luxuryChestPrice)].split('#')[1]

        luxuryCoupon = poco(absoluteName="UI Root/PromptPopupPanel/c2_main/NormalContainer/c2_cost/propIcon_cost/label_count").get_text()
        buy = poco("label_buyTitle").get_text()
        luxuryCouponCount = poco(absoluteName="UI Root/PromptPopupPanel/c2_main/NormalContainer/c2_cost/propIcon_buy/label_count").get_text()
        buyInfo = poco("label_buyInfo").get_text()
        correctBuyInfo = '\n(' + TextDic['item_name_1012'] + 'x1=' + luxuryCouponPrice + TextDic['item_name_3000'] + ')'
        self.assertTrue(('x'+str(int(luxuryCouponPrice)*10) == luxuryCoupon) and (buy == TextDic['shop_buy']) and (luxuryCouponCount == 'x10') and (buyInfo == correctBuyInfo), caseList[17])

    def test_B7(self):
        u"""测试在礼券不足弹窗，点击取消按钮，回到获得界面"""
        poco('label_cancel').click()
        sleep(1.0)
        self.assertFalse(poco('PromptPopupPanel').exists(), caseList[18])

    def test_B8(self):
        u"""测试在礼券不足弹窗，点击购买按钮，播放开启礼盒动画"""
        poco('label_get_ten').click()
        poco('label_confirm').click()
        poco("label_cishu").wait()
        self.assertTrue(poco('OpenChestComp').exists(), caseList[19])

    def test_B9(self):
        u"""测试在礼券不足弹窗，点击购买按钮，弹出钻石不足弹窗"""
        poco('label_cishu').click()
        while poco('label_cishu').exists():
            if poco('tex_title').exists():
                break
            else:
                poco('label_cishu').click()
        poco('label_get_ten').wait()
        sleep(2.0)
        poco('label_get_ten').click()
        sleep(1.0)
        poco('label_confirm').click()
        sleep(1.0)
        title = poco("label_title").get_text()
        self.assertEqual('钻石不足', title, caseList[20])

    def test_C1(self):
        u"""测试钻石不足弹窗文案显示正确"""
        global TextDic

        info = poco("label_info").get_text()
        self.assertEqual(TextDic['shop_skiptoshop'], info, caseList[21])

    def test_C2(self):
        u"""测试钻石不足弹窗点击取消按钮，回到获得界面"""
        poco('label_cancel').click()
        sleep(1.0)
        self.assertFalse(poco('PromptPopupPanel').exists(), caseList[22])

    def test_C3(self):
        u"""测试钻石不足弹窗点击前往按钮，跳转到商店界面"""
        poco('label_get_ten').click()
        sleep(1.0)
        poco('label_confirm').click()
        sleep(1.0)
        poco('label_confirm').click()
        poco('centerList_shopPage').wait()
        self.assertTrue(poco('ShopPanel').exists(), caseList[23])
        poco('c2_back').click()

    @classmethod
    def tearDownClass(cls):
        if not poco('c2_left').exists():
            page = 'homePage'
            pagelist = GetErrorPage(page)
            errorpage = pagelist[0]
            Return(errorpage)
        else:
            pass


if __name__ == "__main__":
    unittest.main()