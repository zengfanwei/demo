# coding=utf-8

import sys
sys.path.insert(0, 'D:\workspace\UITest_TsumTsum\Basics_test')
from Config_test import CASE_EXCEL_PATH, LocalAddress
from BasicFunction import GetMeta, GetCase, GetText, GetErrorPage, Click, ChildClick, checkTwoL
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

caseList = GetCase(CASE_EXCEL_PATH, 'shop_not_enough_pay_chest')
ShopPrice = getValDicFromXml('shop.xml', 'costs', 'extends', 'fillCosts')
LuxuryChestPrice = 0
LuxuryCouponPrice = 0
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
      "cdUpdateTime": 2568884053679,
      "cdPaused": false
    },
    "2": {
      "cdMillis": 172794147,
      "cdUpdateTime": 2568884053679,
      "cdPaused": false
    }
  },
  "recordMap": {
    "2": [
      {
        "items": [
          {
            "itemId": 3,
            "num": 1
          }
        ],
        "gachaTime": 1568883658154
      },
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
      "tsumId": 2,
      "num": 1,
      "sold": false
    },
    {
      "tsumId": 3,
      "num": 1,
      "sold": false
    }
  ],
  "tsumShopRefreshTime": 0,
  "appearedTsums": [
    2,
    3,
    4,
    14
  ],
  "tsumShopLastUpdateTs": 1568883468830,
  "newPlayerSpecialTsumIds": [
    2,
    14,
    3
  ]
}
'''
data2 = '''{
  "uid": 12011,
  "coin": 8100,
  "energy": 72,
  "cash": 50,
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
  }
}'''
updateData(Uid, logic1, data1)
updateData(Uid, logic2, data2)
updateData(Uid, logic3, data3)
start_app('com.tencent.TsumTsumAndroid')
if wait(Template(r"D:\\workspace\\UITest_TsumTsum\\Case\\photo\\tpl1568629745795.png", record_pos=(-0.008, 0.872), resolution=(1080, 2160)),interval=2):
    poco = UnityPoco()

class ShopNotEnoughPayChest(unittest.TestCase):

    def test_A1(self):
        u"""测试豪华礼盒开一盒按钮上显示倒计时"""
        poco("btn_chest").click()
        sleep(2.0)
        self.assertTrue(poco('label_count_down').exists(), caseList[0])

    def test_A2(self):
        u"""测试普通礼盒开一盒按钮上显示倒计时"""
        poco("btn_chest_6").click()
        sleep(1.0)
        self.assertTrue(poco('label_count_down').exists(), caseList[1])

    def test_A3(self):
        u"""测试点击豪华礼盒的开一盒，弹出确认购买弹窗"""
        poco("btn_chest_7").click()
        poco("btn_buy_one").click()
        sleep(1.0)
        self.assertTrue(poco('c2_main').exists(), caseList[2])

    def test_A4(self):
        u"""测试确认购买弹窗显示的文案与配置一致"""
        global ShopPrice, TextDic, LuxuryChestPrice

        for i in ShopPrice.keys():
            if '1012' in i:
                LuxuryChestPrice = int(ShopPrice[i].keys()[0].split('#')[1])

        textInfo = poco("label_costInfo").get_text()
        luxuryChestCount = poco(absoluteName="UI Root/PromptPopupPanel/c2_main/NormalContainer/c2_cost/propIcon_cost/label_count").get_text()
        correctText = TextDic['shop_confirm_special2'] % (LuxuryChestPrice, TextDic['shop_type_title_2'], 1)
        self.assertTrue((luxuryChestCount == 'x1') and (correctText == textInfo), caseList[3])

    def test_A5(self):
        u"""测试在确认购买弹窗点击取消按钮，关闭弹窗，回到礼盒界面"""
        poco("label_cancel").click()
        sleep(2.0)
        self.assertFalse(poco('c2_main').exists(), caseList[4])

    def test_A6(self):
        u"""测试在确认购买弹窗点击购买按钮，弹出礼券不足弹窗"""
        global TextDic

        poco("btn_buy_one").click()
        sleep(1.0)
        poco("label_confirm").click()
        sleep(1.0)
        title = poco("label_title").get_text()
        self.assertEqual(TextDic['shop_lack_ticket'], title, caseList[5])

    def test_A7(self):
        u"""测试礼券不足弹窗显示的文案与配置一致"""
        global TextDic, ShopPrice, LuxuryChestPrice, LuxuryCouponPrice

        for i in ShopPrice.keys():
            if '1012' in i:
                LuxuryCouponPrice = ShopPrice[i]['2000#' + str(LuxuryChestPrice)].split('#')[1]

        luxuryCoupon = poco(absoluteName="UI Root/PromptPopupPanel/c2_main/NormalContainer/c2_cost/propIcon_cost/label_count").get_text()
        buy = poco("label_buyTitle").get_text()
        luxuryCouponCount = poco(absoluteName="UI Root/PromptPopupPanel/c2_main/NormalContainer/c2_cost/propIcon_buy/label_count").get_text()
        buyInfo = poco("label_buyInfo").get_text()
        correctBuyInfo = '\n(' + TextDic['item_name_1012'] + 'x1=' + LuxuryCouponPrice + TextDic['item_name_3000'] + ')'
        self.assertTrue(('x' + LuxuryCouponPrice == luxuryCoupon) and (buy == TextDic['shop_buy']) and (luxuryCouponCount == 'x1') and (buyInfo == correctBuyInfo), caseList[6])

    def test_A8(self):
        u"""测试在礼券不足弹窗点击取消按钮，关闭弹窗，回到礼盒界面"""
        poco("btn_cancel").click()
        sleep(2.0)
        self.assertFalse(poco('c2_main').exists(), caseList[7])

    def test_A9(self):
        u"""测试在礼券不足弹窗点击购买按钮，弹出钻石不足弹窗"""
        poco("btn_buy_one").click()
        sleep(1.0)
        poco("label_confirm").click()
        sleep(1.0)
        poco("label_confirm").click()
        sleep(2.0)
        self.assertEqual('钻石不足', poco("label_title").get_text(), caseList[8])

    def test_B1(self):
        u"""测试钻石不足弹窗显示的文案与配置一致"""
        global TextDic

        labelInfo = poco(absoluteName="UI Root/PromptPopupPanel/c2_main/NormalContainer/label_info").get_text()
        self.assertEqual(TextDic['shop_skiptoshop'], labelInfo, caseList[9])

    def test_B2(self):
        u"""测试在钻石不足弹窗点击取消按钮，关闭弹窗，回到礼盒界面"""
        poco("btn_cancel").click()
        sleep(2.0)
        self.assertFalse(poco('c2_main').exists(), caseList[10])

    def test_B3(self):
        u"""测试在钻石不足弹窗点击前往按钮，跳转到商店，钻石购买模块"""
        poco("btn_buy_one").click()
        sleep(1.0)
        poco("btn_confirm").click()
        sleep(1.0)
        poco("btn_confirm").click()
        sleep(1.0)
        poco("btn_confirm").click()
        sleep(2.0)
        self.assertTrue(poco('ShopPanel').exists(), caseList[11])

    def test_B4(self):
        u"""测试点击豪华礼盒的开十盒，弹出确认购买弹窗"""
        poco("c2_back").click()
        sleep(1.0)
        poco("btn_chest").click()
        sleep(2.0)
        poco("btn_buy_ten").click()
        sleep(1.0)
        self.assertTrue(poco('c2_main').exists(), caseList[12])

    def test_B5(self):
        u"""测试确认购买弹窗显示的文案与配置一致"""
        global ShopPrice, TextDic, LuxuryChestPrice

        textInfo = poco("label_costInfo").get_text()
        print textInfo
        luxuryChestCount = poco(
            absoluteName="UI Root/PromptPopupPanel/c2_main/NormalContainer/c2_cost/propIcon_cost/label_count").get_text()
        print luxuryChestCount
        correctText = TextDic['shop_confirm_special2'] % (LuxuryChestPrice * 10, TextDic['shop_type_title_2'], 10)
        print correctText
        self.assertTrue((luxuryChestCount == 'x10') and (correctText == textInfo), caseList[13])

    def test_B6(self):
        u"""测试在确认购买弹窗点击取消按钮，关闭弹窗，回到礼盒界面"""
        poco("label_cancel").click()
        sleep(2.0)
        self.assertFalse(poco('c2_main').exists(), caseList[14])

    def test_B7(self):
        u"""测试在确认购买弹窗点击购买按钮，弹出礼券不足弹窗"""
        global TextDic

        poco("btn_buy_ten").click()
        sleep(1.0)
        poco("label_confirm").click()
        sleep(1.0)
        title = poco("label_title").get_text()
        self.assertEqual(TextDic['shop_lack_ticket'], title, caseList[15])

    def test_B8(self):
        u"""测试礼券不足弹窗显示的文案与配置一致"""
        global TextDic, LuxuryCouponPrice

        luxuryCoupon = poco(
            absoluteName="UI Root/PromptPopupPanel/c2_main/NormalContainer/c2_cost/propIcon_cost/label_count").get_text()
        buy = poco("label_buyTitle").get_text()
        luxuryCouponCount = poco(
            absoluteName="UI Root/PromptPopupPanel/c2_main/NormalContainer/c2_cost/propIcon_buy/label_count").get_text()
        buyInfo = poco("label_buyInfo").get_text()
        correctBuyInfo = '\n(' + TextDic['item_name_1012'] + 'x1=' + LuxuryCouponPrice + TextDic['item_name_3000'] + ')'
        self.assertTrue(('x' + str(int(LuxuryCouponPrice) * 10) == luxuryCoupon) and (buy == TextDic['shop_buy']) and (
                    luxuryCouponCount == 'x10') and (buyInfo == correctBuyInfo), caseList[16])

    def test_B9(self):
        u"""测试在礼券不足弹窗点击取消按钮，关闭弹窗，回到礼盒界面"""
        poco("btn_cancel").click()
        sleep(2.0)
        self.assertFalse(poco('c2_main').exists(), caseList[17])

    def test_C1(self):
        u"""测试在礼券不足弹窗点击购买按钮，弹出钻石不足弹窗"""
        poco("btn_buy_ten").click()
        sleep(1.0)
        poco("label_confirm").click()
        sleep(1.0)
        poco("label_confirm").click()
        sleep(2.0)
        self.assertEqual('钻石不足', poco("label_title").get_text(), caseList[18])

    def test_C2(self):
        u"""测试钻石不足弹窗显示的文案与配置一致"""
        global TextDic

        labelInfo = poco(absoluteName="UI Root/PromptPopupPanel/c2_main/NormalContainer/label_info").get_text()
        self.assertEqual(TextDic['shop_skiptoshop'], labelInfo, caseList[19])

    def test_C3(self):
        u"""测试在钻石不足弹窗点击取消按钮，关闭弹窗，回到礼盒界面"""
        poco("btn_cancel").click()
        sleep(2.0)
        self.assertFalse(poco('c2_main').exists(), caseList[20])

    def test_C4(self):
        u"""测试在钻石不足弹窗点击前往按钮，跳转到商店，钻石购买模块"""
        poco("btn_buy_one").click()
        sleep(1.0)
        poco("btn_confirm").click()
        sleep(1.0)
        poco("btn_confirm").click()
        sleep(1.0)
        poco("btn_confirm").click()
        sleep(2.0)
        self.assertTrue(poco('ShopPanel').exists(), caseList[21])

    def test_C5(self):
        u"""测试点击普通礼盒的开一盒，弹出礼券不足轻提示"""
        poco("c2_back").click()
        sleep(2.0)
        poco("btn_chest").click()
        sleep(2.0)
        poco("btn_chest_6").click()
        sleep(1.0)
        poco("btn_buy_one").click()
        sleep(1.0)
        self.assertTrue(poco('label').exists(), caseList[22])

    def test_C6(self):
        u"""测试轻提示显示的文案与配置一致"""
        self.assertEqual("普通礼券不足啦", poco("label").get_text(), caseList[23])

    def test_C7(self):
        u"""测试点击普通礼盒的开十盒，弹出礼券不足轻提示"""
        poco("btn_buy_ten").click()
        sleep(1.0)
        self.assertTrue(poco('label').exists(), caseList[24])

    def test_C8(self):
        u"""测试轻提示显示的文案与配置一致"""
        self.assertEqual("普通礼券不足啦", poco("label").get_text(), caseList[25])
        poco("btn_close").click()

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