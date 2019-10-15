# coding=utf-8

import unittest
import json
from TsumTest.Basics.Config import *
from TsumTest.Basics.Get_ChestLevel import chestlevel
from TsumTest.Basics.BasicFunction import GetMeta, GetCase, GetText, GetErrorPage, Click, ChildClick
from TsumTest.Basics.ReturnHomePage import Return
from airtest.core.api import *
from poco.drivers.unity3d import UnityPoco

TsumDrop_dic = {}
FixedRewards_dic = {}

poco = UnityPoco()
commonBox_Tsumdrop = []
caseList = GetCase(TESTAddress, 'rolelist')
commonBox_maxtsum = 0
seniorBox_Tsumdrop = []
seniorBox_maxtsum = 0
luxuryBox_Tsumdrop = []
luxuryBox_maxtsum = 0
userlevel = poco("label_level").get_text()
page = ''
TextDic = GetText(LocalAddress, 'tsum.xlsx')

class Rolelist(unittest.TestCase):
	def test_A1(self):
		u"""测试主界面是否有角色按钮"""
		self.assertTrue(poco('btn_role').exists(), caseList[0])
	def test_A2(self):
		u"""测试点击角色按钮后有没有进入角色列表"""
		page = 'homePage'
		Click('btn_role', page)
		sleep(2.0)
		self.assertTrue(poco('btn_placeholder').exists(), caseList[1])
	def test_A3(self):
		u"""测试角色列表的已拥有松松的列表名是否与配置一致"""
		listname = TextDic['tsumOwn']
		pocolist = poco('scrollView').child('table').offspring('label_info')
		name = pocolist[0].get_text().split(':')[0]
		self.assertEqual(name, listname, caseList[2])
	def test_A4(self):
		u"""测试角色列表的未获得松松的列表名是否与配置一致"""
		pocolist = poco('scrollView').child('table').offspring('label_info')
		if 2 == len(list(pocolist)):
			name = pocolist[1].get_text()
			self.assertEqual(name, '未获得松松列表', caseList[3])

	def test_A5(self):
		u"""测试显示的松松总数量是否正确"""
		tsumlist = GetMeta("tsum.xml", "name")
		pocolist = poco('scrollView').child('table').offspring('label_info')
		tsumnum = pocolist[0].get_text().split('/')[1]
		self.assertEqual(tsumnum, len(tsumlist), caseList[4])
	def test_A6(self):
		u"""测试未获得的松松是否显示未获得"""

	def test_A7(self):
		u"""测试未解锁的松松是否显示解锁信息"""

	def test_A8(self):
		u"""测试点击松松是否弹出详情面板"""

	def test_A9(self):
		u"""测试松松的名字显示是否正确"""

	def test_A10(self):
		u"""测试松松的等级是否与列表里显示的一致"""

	def test_A11(self):
		u"""测试松松队长技能的显示是否与配置一致"""

	def test_A12(self):
		u"""测试技能下方的文案是否与配置一致"""

	def test_A13(self):
		u"""测试当松松可以升级时，是否显示升级的分数加成"""

	def test_A14(self):
		u"""测试点击“设为队长”按钮，松松是否有队长标识"""

	def test_A15(self):
		u"""测试点击“设为队长”按钮，按钮是否置灰不可点击"""

	def test_A16(self):
		u"""测试是否有跳转图鉴的按钮"""

	def test_A17(self):
		u"""测试是否有”升级“按钮"""

	def test_A18(self):
		u"""测试升级按钮显示的金币数是否与配置一致"""

	def test_A19(self):
		u"""测试金币数量充足时点击”升级“按钮后，松松是否升级"""

	def test_A20(self):
		u"""测试金币数量充足时点击”升级“按钮后，前端是否扣除相应的金币数"""

	def test_A21(self):
		u"""测试升级后松松数量不足时，是否显示松松数量不足"""

	def test_A22(self):
		u"""测试金币数量不足时，升级按钮的字体是否变红"""

	def test_A23(self):
		u"""测试金币数量不足时，点击“升级”按钮，是否显示金币不足的提示面板"""

	def test_A24(self):
		u"""测试金币不足的提示弹窗显示的提示文案是否与配置一致"""

	def test_A25(self):
		u"""测试金币不足的提示弹窗是否有“确认”按钮"""

	def test_A26(self):
		u"""测试点击“确认”按钮是否回到松松角色列表"""

	def test_A27(self):
		u"""11.0"""

	@classmethod
	def tearDownClass(cls):
	ui = poco.agent.hierarchy.dump()
		frame = json.dumps(ui, indent=4)
		if 'c2_left' not in frame:
			page = 'homePage'
			pagelist = GetErrorPage(page)
			errorpage = pagelist[len(pagelist)-2]
			Return(errorpage)
		else:
			pass:

if __name__ == '__main__':
	unittest.main()