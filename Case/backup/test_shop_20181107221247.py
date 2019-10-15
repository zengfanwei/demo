# coding=utf-8

import unittest
from Basics_test.Config import CASE_EXCEL_PATH, LocalAddress
from Basics_test.Get_ChestLevel import chestlevel
from Basics_test.BasicFunction import GetMeta, GetCase, GetText, GetErrorPage, Click, ChildClick
from Basics_test.ReturnHomePage import Return

from airtest.core.api import time, sleep
from poco.drivers.unity3d import UnityPoco

TsumDrop_dic = {}
FixedRewards_dic = {}

poco = UnityPoco()
commonBox_Tsumdrop = []
caseList = GetCase(CASE_EXCEL_PATH, 'shop')
commonBox_maxtsum = 0
seniorBox_Tsumdrop = []
seniorBox_maxtsum = 0
luxuryBox_Tsumdrop = []
luxuryBox_maxtsum = 0
userlevel = poco("label_level").get_text()
page = ''
TextDic = GetText(LocalAddress, 'shop.xlsx')

class Shop(unittest.TestCase):
    def test_A1(self):
        u"""测试主界面是否有商店按钮"""
        #assert_exists(Template(r"F:\\my-testflow-master\\hh.jpg"), "lllllllllllllllllllllllllllllllllllllllllllllllllllll")
        self.assertTrue(poco('btn_shop').exists(), caseList[0])
    def test_A2(self):
        u"""测试点击商店按钮是否进入到商店模块"""
        page = 'homePage'
        Click('btn_shop', page)
        sleep(2.0)
        self.assertTrue(poco('tex_bg').exists(), caseList[1])
    def test_A3(self):
        u"""测试购买普通礼盒的金币数是否与meta一致"""
        CostList = GetMeta("shop.xml", "costs")
        commonBox_metacoin = int(CostList[0].replace("2000#", ""))
        common_items = poco("UI Root").child("ShopPanel").offspring("label_count")
        common_coin = int(common_items[2].get_text())
        self.assertEqual(common_coin, commonBox_metacoin, caseList[2])
    def test_A4(self):
        u"""测试普通礼盒显示开出的松松数是否与meta一致"""
        global TsumDrop_dic, FixedRewards_dic, commonBox_maxtsum
        if not TsumDrop_dic and not FixedRewards_dic:
            chestlevel(TsumDrop_dic, FixedRewards_dic)
        for common_tsum in TsumDrop_dic["2001"][userlevel].split(","):
            common_num = len(common_tsum.split("#"))
            commonBox_Tsumdrop.append(common_tsum.split("#")[common_num - 1])
            commonBox_maxtsum += int(common_tsum.split("#")[common_num - 1])
        common_items = poco("UI Root").child("ShopPanel").offspring("label_count")
        common_tsumNum = int(common_items[0].get_text().replace("x", ""))
        self.assertEqual(common_tsumNum, commonBox_maxtsum, caseList[3])
    def test_A5(self):
        u"""测试普通礼盒显示开出的稀有松松数是否与meta一致"""
        global TsumDrop_dic, FixedRewards_dic, commonBox_maxtsum
        if not TsumDrop_dic and not FixedRewards_dic:
            chestlevel(TsumDrop_dic, FixedRewards_dic)
        for common_tsum in TsumDrop_dic["2001"][userlevel].split(","):
            common_num = len(common_tsum.split("#"))
            commonBox_Tsumdrop.append(common_tsum.split("#")[common_num - 1])
        common_meta_rareTsum_R = int(commonBox_Tsumdrop[len(commonBox_Tsumdrop) - 1])
        common_items = poco("UI Root").child("ShopPanel").offspring("label_count")
        common_rareTsum_R = int(common_items[1].get_text().replace("x", ""))
        self.assertEqual(common_rareTsum_R, common_meta_rareTsum_R, caseList[4])
    def test_A6(self):
        u"""测试是否有普通礼盒的购买按钮"""
        self.assertTrue(poco('btn_cost').exists(), caseList[5])
        #self.assertIn('btn_cost', frame, caseList[5])
    def test_A7(self):
        u"""测试点击普通礼盒的购买按钮是否弹出提示弹窗"""
        page = 'shopInterface'
        Click('btn_cost', page)
        time.sleep(2.0)
        self.assertTrue(poco('label_btn_popup_orange').exists(), caseList[6])
    def test_A8(self):
        u"""测试普通礼盒的提示弹窗显示的文案是否与配置一致"""
        CostList = GetMeta("shop.xml", "costs")
        commonBox_metacoin = int(CostList[0].replace("2000#", ""))
        currency = poco("UI Root").child("HeaderPart").offspring("label_count")
        coin = int(currency[1].get_text())
        if coin >= commonBox_metacoin:
            combox_adequate_info = poco("label_info").get_text()
            infotext = TextDic['shop_confirm']
            cointext = TextDic['shop_type_title_2']
            boxtext = TextDic['shop_box_1']
            mergtext = '个Lv.%s' % userlevel
            alltext = infotext % (commonBox_metacoin, cointext, 1, mergtext + boxtext)
            self.assertEqual(combox_adequate_info, alltext, caseList[7])
        else:
            combox_less_info = poco("label_info").get_text()
            cointext = TextDic['shop_type_title_2']
            infotext = TextDic['shop_supplement']
            self.assertEqual(combox_less_info, infotext % cointext, caseList[8])
    def test_A9(self):
        u"""测试普通礼盒的提示弹窗显示的按钮文案是否预配置一致"""
        CostList = GetMeta("shop.xml", "costs")
        commonBox_metacoin = int(CostList[0].replace("2000#", ""))
        currency = poco("UI Root").child("HeaderPart").offspring("label_count")
        coin = int(currency[1].get_text())
        if coin >= commonBox_metacoin:
            combox_adequate_botton = poco("label_btn_popup_orange").get_text()
            goaltext = TextDic['shop_buy']
            self.assertEqual(combox_adequate_botton, goaltext, caseList[9])
        else:
            combox_less_botton = poco("label_btn_popup_orange").get_text()
            goaltext = TextDic['shop_guide']
            self.assertEqual(combox_less_botton, goaltext, caseList[10])
    def test_A10(self):
        u"""测试点击普通礼盒的提示弹窗的按钮"""
        page = 'purchase_popup'
        CostList = GetMeta("shop.xml", "costs")
        commonBox_metacoin = int(CostList[0].replace("2000#", ""))
        currency = poco("UI Root").child("HeaderPart").offspring("label_count")
        coin = int(currency[1].get_text())
        if coin >= commonBox_metacoin:
            Click('label_btn_popup_orange', page)
            page = 'openbox3_interface'
            Click('label_cishu', page)
            page = 'openbox4_interface'
            poco('label_share').wait_for_appearance()
            sleep(2.0)
            Click('label_cishu', page)
            page = 'openbox5_interface'
            poco('label_share').wait_for_appearance()
            sleep(2.0)
            Click('label_cishu', page)
            page = 'settleInterface'
            # 获取开完宝箱后的金币数量
            time.sleep(3.0)
            Click('label_ok', page)
            sleep(1.0)
            if poco('sprite_bg_header').exists():
                page = 'album_share'
                Click('btn_close', page)
                if poco('sprite_bg_header').exists():
                    page = 'album_share'
                    Click('btn_close', page)
            currencyNew = poco("UI Root").child("HeaderPart").offspring("label_count")
            coinnew = int(currencyNew[1].get_text())
            # 检查前端金币数量变化是否正确
            self.assertEqual(coinnew, coin - commonBox_metacoin, caseList[11])
        else:
            Click('label_btn_popup_orange', page)
            page = 'shopInterface'
            self.assertTrue(poco('sprite_gold_1').exists(), caseList[12])
            Click('label_chest', page)
    def test_A11(self):
        u"""测试点击向右翻动的按钮有没有翻到高级礼盒"""
        page = 'shopInterface'
        Click('btn_next', page)
        self.assertTrue(poco('sprite_cash_title').exists(), caseList[13])
    def test_A12(self):
        u"""测试购买高级礼盒的钻石数是否与meta一致"""
        CostList = GetMeta("shop.xml", "costs")
        seniorBox_metacash = int(CostList[1].replace("3000#", ""))
        senior_dataList = poco("UI Root").child("ShopPanel").offspring("label_count")
        senior_cash = int(senior_dataList[4].get_text())
        self.assertEqual(senior_cash, seniorBox_metacash, caseList[14])
    def test_A13(self):
        u"""测试购买高级礼盒的钻石数是否与meta一致"""
        global seniorBox_Tsumdrop, seniorBox_maxtsum, seniorBox_meta_coin
        if not TsumDrop_dic and not FixedRewards_dic:
            chestlevel(TsumDrop_dic, FixedRewards_dic)
        for senior_tsum in TsumDrop_dic["2002"][userlevel].split(","):
            senior_num = len(senior_tsum.split("#"))
            seniorBox_Tsumdrop.append(senior_tsum.split("#")[senior_num - 1])
            seniorBox_maxtsum += int(senior_tsum.split("#")[senior_num - 1])
        senior_dataList = poco("UI Root").child("ShopPanel").offspring("label_count")
        senior_tsum = int(senior_dataList[1].get_text().replace("x", ""))
        self.assertEqual(senior_tsum, seniorBox_maxtsum, caseList[15])
    def test_A14(self):
        u"""测试购买高级礼盒的钻石数是否与meta一致"""
        global seniorBox_Tsumdrop, seniorBox_maxtsum, seniorBox_meta_coin
        if not TsumDrop_dic and not FixedRewards_dic:
            chestlevel(TsumDrop_dic, FixedRewards_dic)
        for senior_tsum in TsumDrop_dic["2002"][userlevel].split(","):
            senior_num = len(senior_tsum.split("#"))
            seniorBox_Tsumdrop.append(senior_tsum.split("#")[senior_num - 1])
        senior_meta_rareTsum_R = int(seniorBox_Tsumdrop[len(seniorBox_Tsumdrop) - 2])
        senior_dataList = poco("UI Root").child("ShopPanel").offspring("label_count")
        senior_raretsum_R = int(senior_dataList[2].get_text().replace("x", ""))
        self.assertEqual(senior_raretsum_R, senior_meta_rareTsum_R, caseList[16])
    def test_A15(self):
        u"""测试购买高级礼盒的钻石数是否与meta一致"""
        global seniorBox_Tsumdrop, seniorBox_maxtsum, seniorBox_meta_coin
        if not TsumDrop_dic and not FixedRewards_dic:
            chestlevel(TsumDrop_dic, FixedRewards_dic)
        for senior_tsum in TsumDrop_dic["2002"][userlevel].split(","):
            senior_num = len(senior_tsum.split("#"))
            seniorBox_Tsumdrop.append(senior_tsum.split("#")[senior_num - 1])
        senior_meta_rareTsum_SR = int(seniorBox_Tsumdrop[len(seniorBox_Tsumdrop) - 1])
        senior_dataList = poco("UI Root").child("ShopPanel").offspring("label_count")
        senior_raretsum_SR = int(senior_dataList[3].get_text().replace("x", ""))
        self.assertEqual(senior_raretsum_SR, senior_meta_rareTsum_SR, caseList[17])
    def test_A16(self):
        u"""测试购买高级礼盒的钻石数是否与meta一致"""
        global seniorBox_Tsumdrop, seniorBox_maxtsum
        if not TsumDrop_dic and not FixedRewards_dic:
            chestlevel(TsumDrop_dic, FixedRewards_dic)
        seniorBox_meta_coin = int(FixedRewards_dic["2002"][userlevel].split("#")[1])
        senior_dataList = poco("UI Root").child("ShopPanel").offspring("label_count")
        senior_coin = int(senior_dataList[0].get_text())
        self.assertEqual(senior_coin, seniorBox_meta_coin, caseList[18])
    def test_A17(self):
        u"""测试是否有高级礼盒的购买按钮"""
        self.assertTrue(poco('btn_cost').exists(), caseList[19])
    def test_A18(self):
        u"""测试点击高级礼盒的购买按钮是否弹出提示弹窗"""
        page = 'shopInterface'
        Click('btn_cost', page)
        time.sleep(2.0)
        self.assertTrue(poco('label_btn_popup_orange').exists(), caseList[20])
    def test_A19(self):
        u"""测试高级礼盒的提示弹窗显示的文案是否与配置一致"""
        CostList = GetMeta("shop.xml", "costs")
        seniorBox_metacash = int(CostList[1].replace("3000#", ""))
        if not TsumDrop_dic and not FixedRewards_dic:
            chestlevel(TsumDrop_dic, FixedRewards_dic)
        seniorBox_meta_coin = int(FixedRewards_dic["2002"][userlevel].split("#")[1])
        itemsOld = poco("UI Root").child("HeaderPart").offspring("label_count")
        cashold = int(itemsOld[0].get_text())
        if cashold >= seniorBox_metacash:
            senbox_adequate_info = poco("label_info").get_text()
            infotext = TextDic['shop_confirm_special']
            cashtext = TextDic['shop_type_title_3']
            cointext = TextDic['shop_type_title_2']
            boxtext = TextDic['shop_box_2']
            mergtext = 'Lv.%s' % userlevel
            alltext = infotext % (seniorBox_metacash, cashtext, seniorBox_meta_coin, cointext, mergtext + boxtext)
            self.assertEqual(senbox_adequate_info, alltext, caseList[21])
        else:
            senbox_less_info = poco("label_info").get_text()
            cashtext = TextDic['shop_type_title_3']
            infotext = TextDic['shop_supplement']
            self.assertEqual(senbox_less_info, infotext % cashtext, caseList[22])
    def test_A20(self):
        u"""测试高级礼盒的提示弹窗显示的按钮文案是否预配置一致"""
        CostList = GetMeta("shop.xml", "costs")
        seniorBox_metacash = int(CostList[1].replace("3000#", ""))
        itemsOld = poco("UI Root").child("HeaderPart").offspring("label_count")
        cashold = int(itemsOld[0].get_text())
        if cashold >= seniorBox_metacash:
            senbox_adequate_botton = poco("label_btn_popup_orange").get_text()
            goaltext = TextDic['shop_buy']
            self.assertEqual(senbox_adequate_botton, goaltext, caseList[23])
        else:
            senbox_less_botton = poco("label_btn_popup_orange").get_text()
            goaltext = TextDic['shop_guide']
            self.assertEqual(senbox_less_botton, goaltext, caseList[24])
    def test_A21(self):
        u"""测试点击高级礼盒的提示弹窗的按钮"""
        page = 'purchase_popup'
        CostList = GetMeta("shop.xml", "costs")
        seniorBox_metacash = int(CostList[1].replace("3000#", ""))
        if not TsumDrop_dic and not FixedRewards_dic:
            chestlevel(TsumDrop_dic, FixedRewards_dic)
        seniorBox_meta_coin = int(FixedRewards_dic["2002"][userlevel].split("#")[1])
        itemsOld = poco("UI Root").child("HeaderPart").offspring("label_count")
        cashold = int(itemsOld[0].get_text())
        coinold = int(itemsOld[1].get_text())
        if cashold >= seniorBox_metacash:
            Click('label_btn_popup_orange', page)
            page = 'openbox1_interface'
            Click('label_cishu', page)
            page = 'openbox2_interface'
            poco('label_share').wait_for_appearance()
            sleep(2.0)
            Click('label_cishu', page)
            page = 'openbox3_interface'
            poco('label_share').wait_for_appearance()
            sleep(2.0)
            Click('label_cishu', page)
            page = 'openbox4_interface'
            poco('label_share').wait_for_appearance()
            sleep(2.0)
            Click('label_cishu', page)
            page = 'openbox5_interface'
            poco('label_share').wait_for_appearance()
            sleep(2.0)
            Click('label_cishu', page)
            page = 'settleInterface'
            # 获取高级礼盒开出的金币数量
            senior_CoinList = poco("UI Root").child("ChestRewardPanel").offspring("label_count")
            senior_getcoin = int(senior_CoinList[0].get_text().replace("+", ""))
            # 检查数量是否正确
            self.assertEqual(senior_getcoin, seniorBox_meta_coin, caseList[25])
            time.sleep(3.0)
            Click('label_ok', page)
            sleep(1.0)
            if poco('sprite_bg_header').exists():
                page = 'album_share'
                Click('btn_close', page)
                if poco('sprite_bg_header').exists():
                    page = 'album_share'
                    Click('btn_close', page)
            senior_itemsNew = poco("UI Root").child("HeaderPart").offspring("label_count")
            senior_cashnew = int(senior_itemsNew[0].get_text())
            senior_coinnew = int(senior_itemsNew[1].get_text())
            # 检查前端金币数量变化是否正确
            self.assertEqual(senior_cashnew, cashold - seniorBox_metacash, caseList[26])
            self.assertEqual(senior_coinnew, coinold + seniorBox_meta_coin, caseList[27])
        else:
            Click('label_btn_popup_orange', page)
            page = 'shopInterface'
            self.assertTrue(poco('tex_light').exists(), caseList[28])
            Click('label_chest', page)
    def test_A22(self):
        u"""测试点击向右翻动的按钮有没有翻到豪华礼盒"""
        page = 'shopInterface'
        Click('btn_next', page)
        self.assertFalse(poco('btn_next').exists(), caseList[29])
    def test_A23(self):
        u"""测试购买豪华礼盒的钻石数是否与meta一致"""
        CostList = GetMeta("shop.xml", "costs")
        luxuryBox_metacash = int(CostList[2].replace("3000#", ""))
        luxury_dataList = poco("UI Root").child("ShopPanel").offspring("label_count")
        luxury_cash = int(luxury_dataList[4].get_text())
        self.assertEqual(luxury_cash, luxuryBox_metacash, caseList[30])
    def test_A24(self):
        u"""测试购买豪华礼盒的钻石数是否与meta一致"""
        global luxuryBox_Tsumdrop, luxuryBox_maxtsum
        if not TsumDrop_dic and not FixedRewards_dic:
            chestlevel(TsumDrop_dic, FixedRewards_dic)
        for luxury_tsum in TsumDrop_dic["2003"][userlevel].split(","):
            luxury_num = len(luxury_tsum.split("#"))
            luxuryBox_Tsumdrop.append(luxury_tsum.split("#")[luxury_num - 1])
            luxuryBox_maxtsum += int(luxury_tsum.split("#")[luxury_num - 1])
        luxury_dataList = poco("UI Root").child("ShopPanel").offspring("label_count")
        luxury_tsum = int(luxury_dataList[1].get_text().replace("x", ""))
        self.assertEqual(luxury_tsum, luxuryBox_maxtsum, caseList[31])
    def test_A25(self):
        u"""测试购买豪华礼盒的钻石数是否与meta一致"""
        global luxuryBox_Tsumdrop, luxuryBox_maxtsum
        if not TsumDrop_dic and not FixedRewards_dic:
            chestlevel(TsumDrop_dic, FixedRewards_dic)
        for luxury_tsum in TsumDrop_dic["2003"][userlevel].split(","):
            luxury_num = len(luxury_tsum.split("#"))
            luxuryBox_Tsumdrop.append(luxury_tsum.split("#")[luxury_num - 1])
        luxury_meta_rareTsum_R = int(luxuryBox_Tsumdrop[len(luxuryBox_Tsumdrop) - 2])
        luxury_dataList = poco("UI Root").child("ShopPanel").offspring("label_count")
        luxury_raretsum_R = int(luxury_dataList[2].get_text().replace("x", ""))
        self.assertEqual(luxury_raretsum_R, luxury_meta_rareTsum_R, caseList[32])
    def test_A26(self):
        u"""测试购买豪华礼盒的钻石数是否与meta一致"""
        global luxuryBox_Tsumdrop, luxuryBox_maxtsum
        if not TsumDrop_dic and not FixedRewards_dic:
            chestlevel(TsumDrop_dic, FixedRewards_dic)
        for luxury_tsum in TsumDrop_dic["2003"][userlevel].split(","):
            luxury_num = len(luxury_tsum.split("#"))
            luxuryBox_Tsumdrop.append(luxury_tsum.split("#")[luxury_num - 1])
        luxury_meta_rareTsum_SR = int(luxuryBox_Tsumdrop[len(luxuryBox_Tsumdrop) - 1])
        luxury_dataList = poco("UI Root").child("ShopPanel").offspring("label_count")
        luxury_raretsum_SR = int(luxury_dataList[3].get_text().replace("x", ""))
        self.assertEqual(luxury_raretsum_SR, luxury_meta_rareTsum_SR, caseList[33])
    def test_A27(self):
        u"""测试购买豪华礼盒的钻石数是否与meta一致"""
        global luxuryBox_Tsumdrop, luxuryBox_maxtsum
        if not TsumDrop_dic and not FixedRewards_dic:
            chestlevel(TsumDrop_dic, FixedRewards_dic)
        luxuryBox_meta_coin = int(FixedRewards_dic["2003"][userlevel].split("#")[1])
        luxury_dataList = poco("UI Root").child("ShopPanel").offspring("label_count")
        luxury_coin = int(luxury_dataList[0].get_text())
        self.assertEqual(luxury_coin, luxuryBox_meta_coin, caseList[34])
    def test_A28(self):
        u"""测试是否有豪华礼盒的购买按钮"""
        self.assertTrue(poco('btn_cost').exists(), caseList[35])
    def test_A29(self):
        u"""测试点击豪华礼盒的购买按钮是否弹出提示弹窗"""
        page = 'shopInterface'
        Click('btn_cost', page)
        time.sleep(2.0)
        self.assertTrue(poco('label_btn_popup_orange').exists(), caseList[36])
    def test_A30(self):
        u"""测试豪华礼盒的提示弹窗显示的文案是否与配置一致"""
        CostList = GetMeta("shop.xml", "costs")
        luxuryBox_metacash = int(CostList[2].replace("3000#", ""))
        if not TsumDrop_dic and not FixedRewards_dic:
            chestlevel(TsumDrop_dic, FixedRewards_dic)
        luxuryBox_meta_coin = int(FixedRewards_dic["2003"][userlevel].split("#")[1])
        itemsOld = poco("UI Root").child("HeaderPart").offspring("label_count")
        cashold = int(itemsOld[0].get_text())
        if cashold >= luxuryBox_metacash:
            luxbox_adequate_info = poco("label_info").get_text()
            infotext = TextDic['shop_confirm_special']
            cashtext = TextDic['shop_type_title_3']
            cointext = TextDic['shop_type_title_2']
            boxtext = TextDic['shop_box_3']
            mergtext = 'Lv.%s' % userlevel
            alltext = infotext % (luxuryBox_metacash, cashtext, luxuryBox_meta_coin, cointext, mergtext + boxtext)
            self.assertEqual(luxbox_adequate_info, alltext, caseList[37])
        else:
            luxbox_less_info = poco("label_info").get_text()
            cashtext = TextDic['shop_type_title_3']
            infotext = TextDic['shop_supplement']
            self.assertEqual(luxbox_less_info, infotext % cashtext, caseList[38])
    def test_A31(self):
        u"""测试豪华礼盒的提示弹窗显示的按钮文案是否预配置一致"""
        CostList = GetMeta("shop.xml", "costs")
        luxuryBox_metacash = int(CostList[2].replace("3000#", ""))
        itemsOld = poco("UI Root").child("HeaderPart").offspring("label_count")
        cashold = int(itemsOld[0].get_text())
        if cashold >= luxuryBox_metacash:
            luxbox_adequate_botton = poco("label_btn_popup_orange").get_text()
            goaltext = TextDic['shop_buy']
            self.assertEqual(luxbox_adequate_botton, goaltext, caseList[39])
        else:
            luxbox_less_botton = poco("label_btn_popup_orange").get_text()
            goaltext = TextDic['shop_guide']
            self.assertEqual(luxbox_less_botton, goaltext, caseList[40])
    def test_A32(self):
        u"""测试点击豪华礼盒的提示弹窗的按钮"""
        page = 'purchase_popup'
        CostList = GetMeta("shop.xml", "costs")
        luxuryBox_metacash = int(CostList[2].replace("3000#", ""))
        if not TsumDrop_dic and not FixedRewards_dic:
            chestlevel(TsumDrop_dic, FixedRewards_dic)
        luxuryBox_meta_coin = int(FixedRewards_dic["2003"][userlevel].split("#")[1])
        itemsOld = poco("UI Root").child("HeaderPart").offspring("label_count")
        cashold = int(itemsOld[0].get_text())
        coinold = int(itemsOld[1].get_text())
        if cashold >= luxuryBox_metacash:
            Click('label_btn_popup_orange', page)
            page = 'openbox1_interface'
            Click('label_cishu', page)
            page = 'openbox2_interface'
            poco('label_share').wait_for_appearance()
            sleep(2.0)
            Click('label_cishu', page)
            page = 'openbox3_interface'
            poco('label_share').wait_for_appearance()
            sleep(2.0)
            Click('label_cishu', page)
            page = 'openbox4_interface'
            poco('label_share').wait_for_appearance()
            sleep(2.0)
            Click('label_cishu', page)
            page = 'openbox5_interface'
            poco('label_share').wait_for_appearance()
            sleep(2.0)
            Click('label_cishu', page)
            page = 'settleInterface'
            # 获取高级礼盒开出的金币数量
            luxury_tsumList = poco("UI Root").child("ChestRewardPanel").offspring("label_count")
            luxury_getcoin = int(luxury_tsumList[0].get_text().replace("+", ""))
            # 检查数量是否正确
            self.assertEqual(luxury_getcoin, luxuryBox_meta_coin, caseList[41])
            time.sleep(3.0)
            Click('label_ok', page)
            sleep(1.0)
            if poco('sprite_bg_header').exists():
                page = 'album_share'
                Click('btn_close', page)
                if poco('sprite_bg_header').exists():
                    page = 'album_share'
                    Click('btn_close', page)
            luxury_itemsNew = poco("UI Root").child("HeaderPart").offspring("label_count")
            luxury_cashnew = int(luxury_itemsNew[0].get_text())
            luxury_coinnew = int(luxury_itemsNew[1].get_text())
            # 检查前端金币数量变化是否正确
            self.assertEqual(luxury_cashnew, cashold - luxuryBox_metacash, caseList[42])
            self.assertEqual(luxury_coinnew, coinold + luxuryBox_meta_coin, caseList[43])
        else:
            Click('label_btn_popup_orange', page)
            page = 'shopInterface'
            self.assertTrue(poco('tex_light').exists(), caseList[44])
            Click('label_chest', page)
    def test_A33(self):
        u"""测试是否有标签页按钮"""
        self.assertTrue(poco('tabbar_shop').exists(), caseList[45])
    def test_A34(self):
        u"""测试点击金币标签页是否到购买金币模块"""
        page = 'shopInterface'
        Click('label_coin', page)
        self.assertTrue(poco('sprite_gold_1').exists(), caseList[46])
    def test_A35(self):
        u"""测试第一个金币堆的金币数显示是否与meta一致"""
        CoinList = GetMeta('shop.xml', 'items')
        coin1_meta = int(CoinList[3].replace("2000#", ""))
        coin1 = int(poco("0001").child("label_get").get_text())
        self.assertEqual(coin1, coin1_meta, caseList[47])
    def test_A36(self):
        u"""测试第二个金币堆的金币数显示是否与meta一致"""
        CoinList = GetMeta('shop.xml', 'items')
        coin2_meta = int(CoinList[4].replace("2000#", ""))
        coin2 = int(poco("0002").child("label_get").get_text())
        self.assertEqual(coin2, coin2_meta, caseList[48])
    def test_A37(self):
        u"""测试第三个金币堆的金币数显示是否与meta一致"""
        CoinList = GetMeta('shop.xml', 'items')
        coin3_meta = int(CoinList[5].replace("2000#", ""))
        coin3 = int(poco("0003").child("label_get").get_text())
        self.assertEqual(coin3, coin3_meta, caseList[49])
    def test_A38(self):
        u"""测试购买第一个金币堆所需的钻石数是否与meta一致"""
        CostList = GetMeta("shop.xml", "costs")
        coin1_metacash = int(CostList[3].replace("3000#", ""))
        cash1 = int(poco("0001").offspring("propIcon_cost").child("label_count").get_text())
        self.assertEqual(cash1, coin1_metacash, caseList[50])
    def test_A39(self):
        u"""测试购买第二个金币堆所需的钻石数是否与meta一致"""
        CostList = GetMeta("shop.xml", "costs")
        coin2_metacash = int(CostList[4].replace("3000#", ""))
        cash2 = int(poco("0002").offspring("propIcon_cost").child("label_count").get_text())
        self.assertEqual(cash2, coin2_metacash, caseList[51])
    def test_A40(self):
        u"""测试购买第三个金币堆所需的钻石数是否与meta一致"""
        CostList = GetMeta("shop.xml", "costs")
        coin3_metacash = int(CostList[5].replace("3000#", ""))
        cash3 = int(poco("0003").offspring("propIcon_cost").child("label_count").get_text())
        self.assertEqual(cash3, coin3_metacash, caseList[52])
    def test_A41(self):
        u"""测试是否有第一个金币堆的购买按钮"""
        self.assertTrue(poco('btn_cost').exists(), caseList[53])# 需要修改！！！
    def test_A42(self):
        u"""测试点击第一个金币堆的购买按钮后有没有弹出确认提示弹窗"""
        page = 'shopInterface'
        ChildClick('0001', 'btn_cost', page)
        self.assertTrue(poco('label_btn_popup_orange').exists(), caseList[54])
    def test_A43(self):
        u"""测试第一个金币堆确认提示弹窗显示的文案是否与配置一致"""
        coin1_adequate_info = poco("label_info").get_text()
        CoinList = GetMeta('shop.xml', 'items')
        coin1_meta = int(CoinList[3].replace("2000#", ""))
        CostList = GetMeta("shop.xml", "costs")
        coin1_metacash = int(CostList[3].replace("3000#", ""))
        infotext = TextDic['shop_confirm']
        cashtext = TextDic['shop_type_title_3']
        cointext = TextDic['shop_type_title_2']
        alltext = infotext % (coin1_metacash, cashtext, coin1_meta, cointext)
        self.assertEqual(coin1_adequate_info, alltext, caseList[55])
    def test_A44(self):
        u"""测试第一个金币堆确认提示弹窗显示的按钮是否与配置一致"""
        btntext = poco('label_btn_popup_orange').get_text()
        goaltext = TextDic['shop_buy']
        self.assertEqual(btntext, goaltext, caseList[56])
    def test_A45(self):
        u"""测试点击第一个金币堆确认提示弹窗显示的按钮"""
        page = 'purchase_popup'
        CostList = GetMeta("shop.xml", "costs")
        coin1_metacash = int(CostList[3].replace("3000#", ""))
        CoinList = GetMeta('shop.xml', 'items')
        coin1_meta = int(CoinList[3].replace("2000#", ""))
        items = poco("UI Root").child("HeaderPart").offspring("label_count")
        cash = int(items[0].get_text())
        coin = int(items[1].get_text())
        if cash >= coin1_metacash:
            Click('btn_confirm', page)
            time.sleep(2.0)
            coin_itemsNew = poco("UI Root").child("HeaderPart").offspring("label_count")
            coin_cashnew = int(coin_itemsNew[0].get_text())
            coin_coinnew = int(coin_itemsNew[1].get_text())
            self.assertEqual(coin_coinnew, coin + coin1_meta, caseList[57])
            self.assertEqual(coin_cashnew, cash - coin1_metacash, caseList[58])
        else:
            Click('btn_confirm', page)
            coin1_cash_less_info = poco("label_info").get_text()
            cashtext = TextDic['shop_type_title_3']
            infotext = TextDic['shop_supplement']
            self.assertEqual(coin1_cash_less_info, infotext % cashtext, caseList[59])
            coin1_less_botton = poco("label_btn_popup_orange").get_text()
            goaltext = TextDic['shop_guide']
            self.assertEqual(coin1_less_botton, goaltext, caseList[60])
            Click('label_btn_popup_orange', page)
            page = 'shopInterface'
            self.assertTrue(poco('tex_light').exists(), caseList[61])# 需要修改！！！
            Click('label_coin', page)
    def test_A46(self):
        u"""测试是否有第二个金币堆的购买按钮"""
        self.assertTrue(poco('btn_cost').exists(), caseList[62])# 需要修改！！！
    def test_A47(self):
        u"""测试点击第二个金币堆的购买按钮后有没有弹出确认提示弹窗"""
        page = 'shopInterface'
        ChildClick('0002', 'btn_cost', page)
        self.assertTrue(poco('label_btn_popup_orange').exists(), caseList[63])
    def test_A48(self):
        u"""测试第二个金币堆确认提示弹窗显示的文案是否与配置一致"""
        coin1_adequate_info = poco("label_info").get_text()
        CoinList = GetMeta('shop.xml', 'items')
        coin2_meta = int(CoinList[4].replace("2000#", ""))
        CostList = GetMeta("shop.xml", "costs")
        coin2_metacash = int(CostList[4].replace("3000#", ""))
        infotext = TextDic['shop_confirm']
        cashtext = TextDic['shop_type_title_3']
        cointext = TextDic['shop_type_title_2']
        alltext = infotext % (coin2_metacash, cashtext, coin2_meta, cointext)
        self.assertEqual(coin1_adequate_info, alltext, caseList[64])
    def test_A49(self):
        u"""测试第二个金币堆确认提示弹窗显示的按钮是否与配置一致"""
        btntext = poco('label_btn_popup_orange').get_text()
        goaltext = TextDic['shop_buy']
        self.assertEqual(btntext, goaltext, caseList[65])
    def test_A50(self):
        u"""测试点击第二个金币堆确认提示弹窗显示的按钮"""
        page = 'purchase_popup'
        CostList = GetMeta("shop.xml", "costs")
        coin2_metacash = int(CostList[4].replace("3000#", ""))
        CoinList = GetMeta('shop.xml', 'items')
        coin2_meta = int(CoinList[4].replace("2000#", ""))
        items = poco("UI Root").child("HeaderPart").offspring("label_count")
        cash = int(items[0].get_text())
        coin = int(items[1].get_text())
        if cash >= coin2_metacash:
            Click('btn_confirm', page)
            time.sleep(2.0)
            coin_itemsNew = poco("UI Root").child("HeaderPart").offspring("label_count")
            coin_cashnew = int(coin_itemsNew[0].get_text())
            coin_coinnew = int(coin_itemsNew[1].get_text())
            self.assertEqual(coin_coinnew, coin + coin2_meta, caseList[66])
            self.assertEqual(coin_cashnew, cash - coin2_metacash, caseList[67])
        else:
            Click('btn_confirm', page)
            coin1_cash_less_info = poco("label_info").get_text()
            cashtext = TextDic['shop_type_title_3']
            infotext = TextDic['shop_supplement']
            self.assertEqual(coin1_cash_less_info, infotext % cashtext, caseList[68])
            coin1_less_botton = poco("label_btn_popup_orange").get_text()
            goaltext = TextDic['shop_guide']
            self.assertEqual(coin1_less_botton, goaltext, caseList[69])
            Click('label_btn_popup_orange', page)
            page = 'shopInterface'
            self.assertTrue(poco('tex_light').exists(), caseList[70])# 需要修改！！！
            Click("label_coin", page)
    def test_A51(self):
        u"""测试是否有第三个金币堆的购买按钮"""
        self.assertTrue(poco('btn_cost').exists(), caseList[71])# 需要修改！！！
    def test_A52(self):
        u"""测试点击第三个金币堆的购买按钮后有没有弹出确认提示弹窗"""
        page = 'shopInterface'
        ChildClick('0003', 'btn_cost', page)
        self.assertTrue(poco('label_btn_popup_orange').exists(), caseList[72])
    def test_A53(self):
        u"""测试第三个金币堆确认提示弹窗显示的文案是否与配置一致"""
        coin1_adequate_info = poco("label_info").get_text()
        CoinList = GetMeta('shop.xml', 'items')
        coin3_meta = int(CoinList[5].replace("2000#", ""))
        CostList = GetMeta("shop.xml", "costs")
        coin3_metacash = int(CostList[5].replace("3000#", ""))
        infotext = TextDic['shop_confirm']
        cashtext = TextDic['shop_type_title_3']
        cointext = TextDic['shop_type_title_2']
        alltext = infotext % (coin3_metacash, cashtext, coin3_meta, cointext)
        self.assertEqual(coin1_adequate_info, alltext, caseList[73])
    def test_A54(self):
        u"""测试第三个金币堆确认提示弹窗显示的按钮是否与配置一致"""
        btntext = poco('label_btn_popup_orange').get_text()
        goaltext = TextDic['shop_buy']
        self.assertEqual(btntext, goaltext, caseList[74])
    def test_A55(self):
        u"""测试点击第三个金币堆确认提示弹窗显示的按钮"""
        page = 'purchase_popup'
        CostList = GetMeta("shop.xml", "costs")
        coin3_metacash = int(CostList[5].replace("3000#", ""))
        CoinList = GetMeta('shop.xml', 'items')
        coin3_meta = int(CoinList[5].replace("2000#", ""))
        items = poco("UI Root").child("HeaderPart").offspring("label_count")
        cash = int(items[0].get_text())
        coin = int(items[1].get_text())
        if cash >= coin3_metacash:
            Click('btn_confirm', page)
            time.sleep(2.0)
            coin_itemsNew = poco("UI Root").child("HeaderPart").offspring("label_count")
            coin_cashnew = int(coin_itemsNew[0].get_text())
            coin_coinnew = int(coin_itemsNew[1].get_text())
            self.assertEqual(coin_coinnew, coin + coin3_meta, caseList[75])
            self.assertEqual(coin_cashnew, cash - coin3_metacash, caseList[76])
        else:
            Click('btn_confirm', page)
            coin1_cash_less_info = poco("label_info").get_text()
            cashtext = TextDic['shop_type_title_3']
            infotext = TextDic['shop_supplement']
            self.assertEqual(coin1_cash_less_info, infotext % cashtext, caseList[77])
            coin1_less_botton = poco("label_btn_popup_orange").get_text()
            goaltext = TextDic['shop_guide']
            self.assertEqual(coin1_less_botton, goaltext, caseList[78])
            Click('label_btn_popup_orange', page)
            page = 'shopInterface'
            self.assertTrue(poco('tex_light').exists(), caseList[79])# 需要修改！！！
            Click('label_coin', page)
    def test_A56(self):
        u"""测试是否有返回城建的按钮"""
        self.assertTrue(poco('btn_back').exists(), caseList[80])
    def test_A57(self):
        u"""测试点击返回城建按钮是否返回到城建界面"""
        page = 'shopInterface'
        Click('btn_back', page)
        #ui = poco.agent.hierarchy.dump()
        #frame = json.dumps(ui, indent=4)
        sleep(3.0)
        self.assertTrue(poco('c2_left').exists(), caseList[81])
        #self.assertIn('c2_left', frame, caseList[81])
        time.sleep(1.0)
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