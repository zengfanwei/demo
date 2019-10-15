# coding=utf-8

import sys
sys.path.insert(0, 'D:\workspace\UITest_TsumTsum\Basics_test')
from Config_test import CASE_EXCEL_PATH
from BasicFunction import GetMeta, GetCase, GetText, GetErrorPage, Click, ChildClick, checkTwoL
from ReturnHomePage import Return
from batchAccessControlInfo import accessControlInfo
from GameData import updateData, queryData
from getFamilyTsum import familyTsum


import unittest
from airtest.core.api import *
from poco.drivers.unity3d import UnityPoco
import json
import os


caseList = GetCase(CASE_EXCEL_PATH, 'shop_free_chest')
LuxuryChestDetails = []
OrdinaryChestDetails = []
Uid = '12011'
OldCoin = 0
UserLevel = queryData(Uid, 'User', 'level')
logic = 'Shop'
data = '''{
      "uid": 12011,
      "cdMap": {
        "1": {
          "cdMillis": 0,
          "cdUpdateTime": 2568884053679,
          "cdPaused": false
        },
        "2": {
          "cdMillis": 0,
          "cdUpdateTime": 2568884053679,
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
updateData(Uid, logic, data)
start_app('com.tencent.TsumTsumAndroid')
if wait(Template(r"D:\\workspace\\UITest_TsumTsum\\Case\\photo\\tpl1568629745795.png", record_pos=(-0.008, 0.872), resolution=(1080, 2160)),interval=2):
    poco = UnityPoco()

class ShopFreeChest(unittest.TestCase):

    def test_A1(self):
        u"""测试主界面是否有商店按钮"""
        self.assertTrue(poco('btn_chest').exists(), caseList[0])

    def test_A2(self):
        u"""测试点击商店按钮后有没有进入商店模块"""
        poco("btn_chest").click()
        sleep(2.0)
        self.assertTrue(poco('go_box').exists(), caseList[1])

    def test_A3(self):
        u"""测试点击普通礼盒tab，显示普通礼盒"""
        poco("btn_chest_6").click()
        sleep(1.0)
        couponInfo = poco("label_info").get_text().split(":")[0]
        self.assertEqual("拥有普通礼券", couponInfo, caseList[2])

    def test_A4(self):
        u"""测试在普通礼盒界面，显示奖池随家族解锁变化"""
        showInfo = poco("label_pool_desc").get_text()
        self.assertEqual("奖池根据家族解锁进度变化", showInfo, caseList[3])

    def test_A5(self):
        u"""测试在普通礼盒界面，点击？号，显示解锁家族松松"""
        poco("btn_info").click()
        sleep(2.0)
        self.assertTrue(poco('label_title').exists(), caseList[4])

    def test_A6(self):
        u"""测试普通礼盒详情显示的松松，是当前已解锁家族的松松"""
        global OrdinaryChestDetails, UserLevel

        unlockedFamilyTsum = familyTsum(UserLevel)[1]
        OrdinaryChestDetails = accessControlInfo('list_pool_reward', 'label_name')
        self.assertTrue(checkTwoL(OrdinaryChestDetails, unlockedFamilyTsum), caseList[5])

    def test_A7(self):
        u"""测试点击关闭按钮，关闭普通礼盒详情"""
        poco(absoluteName="UI Root/ShopPoolPopupPanel/btn_close").click()
        sleep(1.0)
        self.assertFalse(poco('ShopPoolPopupPanel').exists(), caseList[6])

    def test_A8(self):
        u"""测试点击豪华礼盒tab，显示豪华礼盒"""
        poco("btn_chest_7").click()
        sleep(1.0)
        couponInfo = poco("label_info").get_text().split(":")[0]
        self.assertEqual("拥有豪华礼券", couponInfo, caseList[7])

    def test_A9(self):
        u"""测试豪华礼盒十连抽上显示保底信息"""
        self.assertTrue(poco("c2_must_get").exists(), caseList[8])

    def test_B1(self):
        u"""测试在豪华礼盒界面，点击？号，显示所有松松"""
        poco("btn_info").click()
        sleep(1.0)
        self.assertTrue(poco('label_title').exists(), caseList[9])

    def test_B2(self):
        u"""测试豪华礼盒详情显示的松松，是所有松松"""
        global LuxuryChestDetails, UserLevel

        allTsum = familyTsum(UserLevel)[0]
        sleep(1.0)
        poco("tex_chest_bg").swipe([-0.0046, -0.2178])
        LuxuryChestDetails = accessControlInfo('list_pool_reward', 'label_name')
        self.assertTrue(checkTwoL(LuxuryChestDetails, allTsum), caseList[10])
        sleep(1.0)
        poco("tex_chest_bg").swipe([0.0, 0.2489])

    def test_B3(self):
        u"""测试点击关闭按钮，关闭豪华礼盒详情"""
        poco(absoluteName="UI Root/ShopPoolPopupPanel/btn_close").click()
        sleep(1.0)
        self.assertFalse(poco('ShopPoolPopupPanel').exists(), caseList[11])

    def test_B4(self):
        u"""测试有免费开启豪华礼盒的机会，开一盒按钮显示为免费"""
        global OldCoin

        assertResult = poco('btn_buy_animation').exists() and not poco('btn_buy_one').exists()
        OldCoin = int(poco(absoluteName="UI Root/HeaderPart/c2_currency/c2_coin/propIcon/label_count").get_text())
        self.assertTrue(assertResult, caseList[12])

    def test_B5(self):
        u"""测试有免费开启豪华礼盒的机会，点击免费按钮，播放开礼盒动画"""
        poco("btn_buy_animation").click()
        sleep(2.0)
        self.assertTrue(poco('BuyCoinContainer').exists(), caseList[13])

    def test_B6(self):
        u"""测试开礼盒动画上豪华礼盒数量显示为1"""
        chestCount = poco("label_cishu").get_text()
        self.assertEqual("1", chestCount, caseList[14])

    def test_B7(self):
        u"""测试点击打开豪华礼盒，播放获得动画"""
        poco("label_cishu").click()
        sleep(3.0)
        self.assertTrue(poco("sprite_progress_bg"), caseList[15])

    def test_B8(self):
        u"""测试开出来的松松在豪华礼盒能开出来的松松中"""
        global LuxuryChestDetails

        tsumName = poco("label_name").get_text()
        tsumName = tsumName.replace('的碎片', '')
        self.assertTrue(tsumName in LuxuryChestDetails, caseList[16])

    def test_B9(self):
        u"""测试开出松松后豪华礼盒的数量变为0"""
        chestCount = poco("label_cishu").get_text()
        sleep(1.0)
        self.assertEqual("0", chestCount, caseList[17])

    def test_C1(self):
        u"""测试关闭开礼盒界面，回到gacha界面"""
        poco("label_name").click()
        sleep(2.0)
        self.assertFalse(poco('ChestRewardPanel').exists(), caseList[18])

    def test_C2(self):
        u"""测试开启一次豪华礼盒，获得100金币"""
        global OldCoin, Uid

        newCoin = int(poco(absoluteName="UI Root/HeaderPart/c2_currency/c2_coin/propIcon/label_count").get_text())
        print newCoin
        backCoin = queryData(Uid, 'User', 'coin')
        print backCoin
        self.assertTrue((newCoin == OldCoin + 100) and (newCoin == backCoin), caseList[19])

    def test_C3(self):
        u"""测试回到gacha界面后，显示开一盒按钮，上方显示倒计时"""
        assertResult = poco('btn_buy_one').exists() and poco('label_count_down').exists()
        self.assertTrue(assertResult, caseList[20])

    def test_C4(self):
        u"""测试有免费开启普通礼盒的机会，开一盒按钮显示为免费"""
        poco("btn_chest_6").click()
        sleep(1.0)
        assertResult = poco('btn_buy_animation').exists() and not poco('btn_buy_one').exists()
        self.assertTrue(assertResult, caseList[21])

    def test_C5(self):
        u"""测试有免费开启普通礼盒的机会，点击免费按钮，播放开礼盒动画"""
        poco("btn_buy_animation").click()
        sleep(3.0)
        self.assertTrue(poco('BuyCoinContainer').exists(), caseList[22])

    def test_C6(self):
        u"""测试开礼盒动画上普通礼盒数量显示为1"""
        chestCount = poco("label_cishu").get_text()
        self.assertEqual("1", chestCount, caseList[23])

    def test_C7(self):
        u"""测试点击打开普通礼盒，播放获得动画"""
        poco("label_cishu").click()
        sleep(3.0)
        self.assertTrue(poco("sprite_progress_bg"), caseList[24])

    def test_C8(self):
        u"""测试开出来的松松在普通礼盒能开出来的松松中"""
        global OrdinaryChestDetails

        tsumName = poco("label_name").get_text()
        tsumName = tsumName.replace('的碎片', '')
        self.assertTrue(tsumName in OrdinaryChestDetails, caseList[25])

    def test_C9(self):
        u"""测试开出松松后普通礼盒的数量变为0"""
        sleep(1.0)
        chestCount = poco("label_cishu").get_text()
        self.assertEqual("0", chestCount, caseList[26])

    def test_D1(self):
        u"""测试关闭开礼盒界面，回到gacha界面"""
        poco("label_cishu").click()
        sleep(2.0)
        self.assertFalse(poco('ChestRewardPanel').exists(), caseList[27])

    def test_D2(self):
        u"""测试回到gacha界面后，显示开一盒按钮，上方显示倒计时"""
        assertResult = poco('btn_buy_one').exists() and poco('label_count_down').exists()
        self.assertTrue(assertResult, caseList[28])

    def test_D3(self):
        u"""测试点击关闭按钮，回到主界面"""
        poco("btn_close").click()
        sleep(1.0)
        #ui = poco.agent.hierarchy.dump()
        #frame = json.dumps(ui, indent=4)
        self.assertFalse(poco('ShopGachaPanel').exists(), caseList[29])
        #self.assertIn('c2_left', frame, caseList[81])
        sleep(1.0)

    @classmethod
    def tearDownClass(cls):
        if not poco('c2_left').exists():
            page = 'homePage'
            pagelist = GetErrorPage(page)
            errorpage = pagelist[0]
            Return(errorpage)
#        stop_app('com.tencent.TsumTsumAndroid')


if __name__ == "__main__":
    unittest.main()