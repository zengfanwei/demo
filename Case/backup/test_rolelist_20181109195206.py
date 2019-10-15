# coding=utf-8

import sys 
sys.path.insert(0, 'D:\workspace\UITest_TsumTsum\Basics_test')
from Config_test import CASE_EXCEL_PATH, LocalAddress
from GetTsuminfo import GetTsumInfo
from GetTsumLevelUPInfo import GetTsumLevelupInfo, GetTsumSkillup
from BasicFunction import GetCase, GetText, Click

import unittest
import json

from airtest.core.api import sleep
from airtest.core.helper import G
from poco.drivers.unity3d import UnityPoco # cmd: pip install pocoui

TsumInfo_dic = {}
TsumLevelupInfo_dic = {}
TsumSkillup_dic = {}
poco = UnityPoco()
commonBox_Tsumdrop = []
caseList = GetCase(CASE_EXCEL_PATH, 'rolelist')
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
		sleep(2.5)
		poco('scrollView').child('table').offspring('label_info')[1].swipe([0, -0.5])
		poco('scrollView').child('table').offspring('label_info')[1].swipe([0, 0.5])
		self.assertTrue(poco('btn_placeholder').exists(), caseList[1])
	def test_A3(self):
		u"""测试角色列表的已拥有松松的列表名是否与配置一致"""
		listname = TextDic['tsumOwn'].encode('utf-8')
		pocolist = poco('scrollView').child('table').offspring('label_info')
		name = pocolist[0].get_text().split(':')[0]
		self.assertEqual(name, listname, caseList[2])
	def test_A4(self):
		u"""测试角色列表的未获得松松的列表名是否与配置一致
		测试角色列表不含有未获得的松松是否不显示未获得松松的表头"""
		pocolist = poco('scrollView').child('table').offspring('label_info')
		if 2 == len(list(pocolist)):
			name = pocolist[1].get_text()
			self.assertEqual(name, '未获得松松列表', caseList[3])
		else:
			self.assertFalse(poco('c2_no_obtained').exists(), caseList[4])
	def test_A5(self):
		u"""测试显示的松松总数量是否正确"""
		#tsumlist = GetMeta("tsum.xml", "name")
		pocolist = poco('scrollView').child('table').offspring('label_info')
		tsumnum = int(pocolist[0].get_text().split('/')[1])
		self.assertEqual(tsumnum, 23, caseList[5])
	def test_A6(self):
		u"""测试未获得的松松是否显示未获得"""
		pocolist = poco('scrollView').child('table').offspring('label_no_obtained')
		if len(list(pocolist)) >= 1:
			for i in range(len(list(pocolist))):
				tsumtext = pocolist[i].get_text()
				self.assertEqual(tsumtext, '未获得', caseList[6])
	def test_A7(self):
		u"""测试未解锁的松松是否显示解锁信息
		测试不含有未解锁的松松是否不显示未解锁松松"""
		pocolist = poco('scrollView').child('table').offspring('label_unlock_tip')
		if poco('label_unlock_tip').exists():
			if len(list(pocolist))/6 >= 1:
				for i in range(6):
					for j in range(len(list(pocolist))/6):
						tsumtext = pocolist[i + 6*j].get_text()
						svntext = (TextDic['tsum_unlock2'] % (int(userlevel) + 1 + j)).encode('utf-8')
						self.assertEqual(tsumtext, svntext, caseList[7])
		else:
			self.assertFalse(poco('label_unlock_tip').exists(), caseList[8])
	def test_A8(self):
		u"""测试队长松松是否有队长标识
		测试非队长松松是否没有队长标识
		测试可以升级的松松是否升级的标识
		测试不能升级的松松是否没有升级的标识
		测试点击松松是否弹出详情面板
		测试松松的名字显示是否与配置一致
		测试松松的家族名字是否与配置一致
		测试升级后松松的技能等级不会增加的技能等级显示是否与配置一致
		测试升级后松松的技能等级会加一的技能等级显示是否加一
		测试松松的技能描述是否与配置一致
		测试松松详情面板上显示的松松等级是否与角色列表里显示的一致
		测试可以升级的松松的详情面板是否显示升级标识
		测试不能升级的松松的详情面板是否不显示升级标识
		测试队长松松的详情面板是否显示队长标识
		测试非队长的松松的详情面板是否不显示队长标识
		测试松松详情面板上是否有跳转图鉴的按钮
		测试松松详情面板上是否有设为队长按钮
		测试松松详情面板上的设为队长按钮的文案显示是否与配置一致
		测试松松详情面板上是否有升级按钮
		测试松松详情面板上的升级按钮的文案是否与配置一致
		测试松松详情面板上是否有松松数量不足的按钮
		测试送送详情面板上的松松数量不足按钮的文案是否与配置一致
		测试不能升级的松松的分数显示是否与meta配置一致
		测试可以升级的松松的分数显示是否显示了升级需要加上的分数
		测试可以升级的松松的升级按钮上的升级金币显示是否与meta配置一致
		测试点击空白处是否关闭详情面板"""
		global TsumInfo_dic, TsumLevelupInfo_dic, TsumSkillup_dic
		pocolist = poco('scrollView').child('table').offspring('c2_progress')
		pocolist1 = poco('scrollView').child('table').offspring('c2_tsum')
		#获取tsum的meta信息
		if not TsumInfo_dic:
			GetTsumInfo(TsumInfo_dic)
		if not TsumLevelupInfo_dic:
			GetTsumLevelupInfo(TsumLevelupInfo_dic)
		if not TsumSkillup_dic:
			GetTsumSkillup(TsumSkillup_dic)
		#将所有已获得的松松都点击一遍
		for i in range(len(list(pocolist))):
			#获取松松等级
			levelinfo = poco('scrollView').child('table').offspring('label_tsum_level')[i].get_text()
			tsumlevel = levelinfo.replace('级', '')
			num = poco('scrollView').child('table').offspring('label_tsum_level_info')[i].get_text()
			exp_max = TextDic['tsum_exp_max']
			#判断松松是否为队长松松
			captain = poco('scrollView').child('table').offspring('tsumContainer')[i]
			if captain.child('c2_obtained').offspring('sprite_captain').exists():
				self.assertTrue(captain.child('c2_obtained').offspring('sprite_captain').exists(), caseList[9])
				#判断松松是否可以升级
				if num == exp_max:
					pocouiname = poco('scrollView').child('table').offspring('c2_progress')[i].child()
					self.assertFalse(pocouiname.offspring('spine_arrowhead').exists(), caseList[12])
					# 点击松松
					pocolist[i].click()
					tsumid = pocolist1[i].child().get_name().split('_')[1]
					tsumname = TextDic['tsum_name_' + tsumid].encode('utf-8')
					sleep(1.0)
					# 检查是否打开了松松详情面板
					self.assertTrue(poco('mask').exists(), caseList[13])
					tsumname_game = poco('label_tsum_name').get_text()
					# 检查松松的名字显示是否正确
					self.assertEqual(tsumname_game, tsumname, caseList[14])
					familyid = TsumInfo_dic[tsumid][0]
					familyname = TextDic['tsum_family_' + familyid].encode('utf-8')
					familyname_game = poco('label_tsum_family').get_text().strip('[]')
					# 检查松松的家族名字是否正确
					self.assertEqual(familyname_game, familyname, caseList[15])
					# 检查技能等级的显示
					tsumstar = TsumInfo_dic[tsumid][1]
					skillinfo = poco('label_skill').get_text()
					index1 = poco('label_skill_level').get_text().find(']')
					index2 = poco('label_skill_level').get_text()[index1 + 1:].find('[')
					skill_level1 = '(' + poco('label_skill_level').get_text()[index1 + 4:index1 + 1 + index2] + ')'
					skill_level2 = '(' + poco('label_skill_level').get_text()[index1 + 4:index1 + 1 + index2] + '+1)'
					skilllv = TsumLevelupInfo_dic[tsumstar][tsumlevel][3]
					uplist = []
					for lv in TsumSkillup_dic[tsumstar][skilllv]:
						uplist.append(int(lv))
					level_to_skillup = max(uplist)
					if int(tsumlevel) < level_to_skillup:
						skill_svn1 = (TextDic['tsum_skill_level'] % (int(skilllv), '')).encode('utf-8')
						self.assertEqual(skillinfo + skill_level1, skill_svn1, caseList[16])
					if int(tsumlevel) == level_to_skillup:
						skill_svn2 = (TextDic['tsum_skill_level'] % (int(skilllv), '+1')).encode('utf-8')
						self.assertEqual(skillinfo + skill_level2, skill_svn2, caseList[17])
					skill_game = TextDic['tsum_skill_des_' + tsumid].encode('utf-8')
					skill = poco('label_skill_desc').get_text()
					# 检查松松的技能描述是否正确
					self.assertEqual(skill_game, skill, caseList[18])
					level_details = poco('label_tsum_level').get_text()
					# 检查松松详情面板显示的松松等级是否与角色列表一致
					self.assertEqual(level_details, levelinfo, caseList[19])
					# 检查松松详情面板是否不显示升级箭头
					ui = poco('RoleInfoContainer').child('c2_tsum_info').offspring('spine_arrowhead')
					self.assertFalse(ui.exists(), caseList[21])
					# 检查是否有队长标识
					captain_ui = poco('RoleInfoContainer').child('c2_tsum_info').offspring('sprite_captain')
					self.assertTrue(captain_ui.exists(), caseList[23])
					self.assertTrue(poco("btn_forward").exists(), caseList[24])
					# 检查设为队长按钮
					self.assertTrue(poco('btn_set_leader').exists(), caseList[25])
					setcaptain = TextDic['tsumSetCaptain'].encode('utf-8')
					setcaptain_game = poco('label_set_leader').get_text()
					self.assertEqual(setcaptain_game, setcaptain, caseList[26])
					# 检查松松已达到满级按钮
					self.assertTrue(poco('btn_max_level').exists(), caseList[29])
					upgrade = poco('label_max_level').get_text()
					upgrade_svn = '已达到满级'
					self.assertEqual(upgrade, upgrade_svn, caseList[30])
					# 检查松松的分数显示
					basescore = int(TsumLevelupInfo_dic[tsumstar][tsumlevel][0])
					scoreinfo = poco('label_score_info').get_text()
					score = poco('label_score').get_text()
					info = TextDic['tsum_socre'].encode('utf-8')
					self.assertEqual(scoreinfo + score, info % (basescore, ''), caseList[31])
					# 检查是否关闭了详情面板
					size = poco.get_screen_size()
					G.DEVICE.touch([0.4277778 * size[0], 0.0222222228 * size[1]])
					sleep(0.5)
					self.assertFalse(poco('mask').exists(), caseList[34])
				elif int(num.split('/')[0]) >= int(num.split('/')[1]):
					pocouiname = poco('scrollView').child('table').offspring('c2_progress')[i].child()
					#检查可以升级的松松是否有升级箭头
					self.assertTrue(pocouiname.offspring('spine_arrowhead').exists(), caseList[11])
					#点击松松
					pocolist[i].click()
					tsumid = pocolist1[i].child().get_name().split('_')[1]
					tsumname = TextDic['tsum_name_'+tsumid].encode('utf-8')
					sleep(1.0)
					#检查是否打开了松松详情面板
					self.assertTrue(poco('mask').exists(), caseList[13])
					tsumname_game = poco('label_tsum_name').get_text()
					#检查松松的名字显示是否正确
					self.assertEqual(tsumname_game, tsumname, caseList[14])
					familyid = TsumInfo_dic[tsumid][0]
					familyname = TextDic['tsum_family_'+familyid].encode('utf-8')
					familyname_game = poco('label_tsum_family').get_text().strip('[]')
					#检查松松的家族名字是否正确
					self.assertEqual(familyname_game, familyname, caseList[15])
					# 检查技能等级的显示
					tsumstar = TsumInfo_dic[tsumid][1]
					skillinfo = poco('label_skill').get_text()
					index1 = poco('label_skill_level').get_text().find(']')
					index2 = poco('label_skill_level').get_text()[index1 + 1:].find('[')
					skill_level1 = '(' + poco('label_skill_level').get_text()[index1 + 4:index1 + 1 + index2] + ')'
					skill_level2 = '(' + poco('label_skill_level').get_text()[index1 + 4:index1 + 1 + index2] + '+1)'
					skilllv = TsumLevelupInfo_dic[tsumstar][tsumlevel][3]
					uplist = []
					for lv in TsumSkillup_dic[tsumstar][skilllv]:
						uplist.append(int(lv))
					level_to_skillup = max(uplist)
					if int(tsumlevel) < level_to_skillup:
						skill_svn1 = (TextDic['tsum_skill_level'] % (int(skilllv), '')).encode('utf-8')
						self.assertEqual(skillinfo + skill_level1, skill_svn1, caseList[16])
					if int(tsumlevel) == level_to_skillup:
						skill_svn2 = (TextDic['tsum_skill_level'] % (int(skilllv), '+1')).encode('utf-8')
						self.assertEqual(skillinfo + skill_level2, skill_svn2, caseList[17])
					skill_game = TextDic['tsum_skill_des_'+tsumid].encode('utf-8')
					skill = poco('label_skill_desc').get_text()
					#检查松松的技能描述是否正确
					self.assertEqual(skill_game, skill, caseList[18])
					level_details = poco('label_tsum_level').get_text()
					#检查松松详情面板显示的松松等级是否与角色列表一致
					self.assertEqual(level_details, levelinfo, caseList[19])
					#检查松松详情面板是否也显示升级箭头
					ui = poco('RoleInfoContainer').child('c2_tsum_info').offspring('spine_arrowhead')
					self.assertTrue(ui.exists(), caseList[20])
					#检查是否有队长标识
					captain_ui = poco('RoleInfoContainer').child('c2_tsum_info').offspring('sprite_captain')
					self.assertTrue(captain_ui.exists(), caseList[22])
					self.assertTrue(poco("btn_forward").exists(), caseList[24])
					#检查设为队长按钮
					self.assertTrue(poco('btn_set_leader').exists(), caseList[25])
					setcaptain = TextDic['tsumSetCaptain'].encode('utf-8')
					setcaptain_game = poco('label_set_leader').get_text()
					self.assertEqual(setcaptain_game, setcaptain, caseList[26])
					#检查升级按钮
					self.assertTrue(poco('btn_upgrade').exists(), caseList[27])
					upgrade = poco('btn_upgrade').child().child()[1].get_text().split(' ')[0]
					self.assertEqual(upgrade, '升级', caseList[28])
					#检查松松的分数显示
					basescore = int(TsumLevelupInfo_dic[tsumstar][tsumlevel][0])
					scorechange = int(TsumLevelupInfo_dic[tsumstar][str(int(tsumlevel) + 1)][0]) - basescore
					scoreinfo = poco('label_score_info').get_text()
					score = poco('label_score').get_text()
					info = TextDic['tsum_socre'].encode('utf-8')
					scoreinfo_svn = info % (basescore, '[FFD11AFF]+' + str(scorechange) + '[-]')
					self.assertEqual(scoreinfo + score, scoreinfo_svn, caseList[32])
					#检查升级按钮上的金币数量
					cost = TsumLevelupInfo_dic[tsumstar][tsumlevel][1]
					numstart = int(poco('btn_upgrade').child().child()[1].get_text().find(']'))
					cost_game = poco('btn_upgrade').child().child()[1].get_text()[numstart+1:-3]
					self.assertEqual(int(cost), int(cost_game), caseList[33])
					#检查是否关闭了详情面板
					size = poco.get_screen_size()
					G.DEVICE.touch([0.4277778 * size[0], 0.0222222228 * size[1]])
					sleep(0.5)
					self.assertFalse(poco('mask').exists(), caseList[34])
				else:
					pocouiname = poco('scrollView').child('table').offspring('c2_progress')[i].child()
					self.assertFalse(pocouiname.offspring('spine_arrowhead').exists(), caseList[12])
					# 点击松松
					pocolist[i].click()
					tsumid = pocolist1[i].child().get_name().split('_')[1]
					tsumname = TextDic['tsum_name_' + tsumid].encode('utf-8')
					sleep(1.0)
					# 检查是否打开了松松详情面板
					self.assertTrue(poco('mask').exists(), caseList[13])
					tsumname_game = poco('label_tsum_name').get_text()
					# 检查松松的名字显示是否正确
					self.assertEqual(tsumname_game, tsumname, caseList[14])
					familyid = TsumInfo_dic[tsumid][0]
					familyname = TextDic['tsum_family_' + familyid].encode('utf-8')
					familyname_game = poco('label_tsum_family').get_text().strip('[]')
					# 检查松松的家族名字是否正确
					self.assertEqual(familyname_game, familyname, caseList[15])
					# 检查技能等级的显示
					tsumstar = TsumInfo_dic[tsumid][1]
					skillinfo = poco('label_skill').get_text()
					index1 = poco('label_skill_level').get_text().find(']')
					index2 = poco('label_skill_level').get_text()[index1 + 1:].find('[')
					skill_level1 = '('+poco('label_skill_level').get_text()[index1 + 4:index1 + 1 + index2] + ')'
					skill_level2 = '('+poco('label_skill_level').get_text()[index1 + 4:index1 + 1 + index2] + '+1)'
					skilllv = TsumLevelupInfo_dic[tsumstar][tsumlevel][3]
					uplist = []
					for lv in TsumSkillup_dic[tsumstar][skilllv]:
						uplist.append(int(lv))
					level_to_skillup = max(uplist)
					if int(tsumlevel) < level_to_skillup:
						skill_svn1 = (TextDic['tsum_skill_level'] % (int(skilllv), '')).encode('utf-8')
						self.assertEqual(skillinfo + skill_level1, skill_svn1, caseList[16])
					if int(tsumlevel) == level_to_skillup:
						skill_svn2 = (TextDic['tsum_skill_level'] % (int(skilllv), '+1')).encode('utf-8')
						self.assertEqual(skillinfo + skill_level2, skill_svn2, caseList[17])
					skill_game = TextDic['tsum_skill_des_' + tsumid].encode('utf-8')
					skill = poco('label_skill_desc').get_text()
					# 检查松松的技能描述是否正确
					self.assertEqual(skill_game, skill, caseList[18])
					level_details = poco('label_tsum_level').get_text()
					# 检查松松详情面板显示的松松等级是否与角色列表一致
					self.assertEqual(level_details, levelinfo, caseList[19])
					# 检查松松详情面板是否不显示升级箭头
					ui = poco('RoleInfoContainer').child('c2_tsum_info').offspring('spine_arrowhead')
					self.assertFalse(ui.exists(), caseList[21])
					# 检查是否有队长标识
					captain_ui = poco('RoleInfoContainer').child('c2_tsum_info').offspring('sprite_captain')
					self.assertTrue(captain_ui.exists(), caseList[23])
					self.assertTrue(poco("btn_forward").exists(), caseList[24])
					# 检查设为队长按钮
					self.assertTrue(poco('btn_set_leader').exists(), caseList[25])
					setcaptain = TextDic['tsumSetCaptain'].encode('utf-8')
					setcaptain_game = poco('label_set_leader').get_text()
					self.assertEqual(setcaptain_game, setcaptain, caseList[26])
					# 检查松松不足按钮
					self.assertTrue(poco('btn_upgrade').exists(), caseList[29])
					upgrade = poco('label_upgrade_tip').get_text()
					upgrade_svn = TextDic['tsum_num_short'].encode('utf-8')
					self.assertEqual(upgrade, upgrade_svn, caseList[30])
					#检查松松的分数显示
					basescore = int(TsumLevelupInfo_dic[tsumstar][tsumlevel][0])
					scoreinfo = poco('label_score_info').get_text()
					score = poco('label_score').get_text()
					info = TextDic['tsum_socre'].encode('utf-8')
					self.assertEqual(scoreinfo + score, info % (basescore, ''), caseList[31])
					#检查是否关闭了详情面板
					size = poco.get_screen_size()
					G.DEVICE.touch([0.4277778 * size[0], 0.0222222228 * size[1]])
					sleep(0.5)
					self.assertFalse(poco('mask').exists(), caseList[34])
			else:
				self.assertFalse(captain.child('c2_obtained').offspring('sprite_captain').exists(), caseList[10])
				# 判断松松是否可以升级
				if num == exp_max:
					pocouiname = poco('scrollView').child('table').offspring('c2_progress')[i].child()
					self.assertFalse(pocouiname.offspring('spine_arrowhead').exists(), caseList[12])
					# 点击松松
					pocolist[i].click()
					tsumid = pocolist1[i].child().get_name().split('_')[1]
					tsumname = TextDic['tsum_name_' + tsumid].encode('utf-8')
					sleep(1.0)
					# 检查是否打开了松松详情面板
					self.assertTrue(poco('mask').exists(), caseList[13])
					tsumname_game = poco('label_tsum_name').get_text()
					# 检查松松的名字显示是否正确
					self.assertEqual(tsumname_game, tsumname, caseList[14])
					familyid = TsumInfo_dic[tsumid][0]
					familyname = TextDic['tsum_family_' + familyid].encode('utf-8')
					familyname_game = poco('label_tsum_family').get_text().strip('[]')
					# 检查松松的家族名字是否正确
					self.assertEqual(familyname_game, familyname, caseList[15])
					# 检查技能等级的显示
					tsumstar = TsumInfo_dic[tsumid][1]
					skillinfo = poco('label_skill').get_text()
					index1 = poco('label_skill_level').get_text().find(']')
					index2 = poco('label_skill_level').get_text()[index1 + 1:].find('[')
					skill_level1 = '(' + poco('label_skill_level').get_text()[index1 + 4:index1 + 1 + index2] + ')'
					skill_level2 = '(' + poco('label_skill_level').get_text()[index1 + 4:index1 + 1 + index2] + '+1)'
					skilllv = TsumLevelupInfo_dic[tsumstar][tsumlevel][3]
					uplist = []
					for lv in TsumSkillup_dic[tsumstar][skilllv]:
						uplist.append(int(lv))
					level_to_skillup = max(uplist)
					if int(tsumlevel) < level_to_skillup:
						skill_svn1 = (TextDic['tsum_skill_level'] % (int(skilllv), '')).encode('utf-8')
						self.assertEqual(skillinfo + skill_level1, skill_svn1, caseList[16])
					if int(tsumlevel) == level_to_skillup:
						skill_svn2 = (TextDic['tsum_skill_level'] % (int(skilllv), '+1')).encode('utf-8')
						self.assertEqual(skillinfo + skill_level2, skill_svn2, caseList[17])
					skill_game = TextDic['tsum_skill_des_' + tsumid].encode('utf-8')
					skill = poco('label_skill_desc').get_text()
					# 检查松松的技能描述是否正确
					self.assertEqual(skill_game, skill, caseList[18])
					level_details = poco('label_tsum_level').get_text()
					# 检查松松详情面板显示的松松等级是否与角色列表一致
					self.assertEqual(level_details, levelinfo, caseList[19])
					# 检查松松详情面板是否不显示升级箭头
					ui = poco('RoleInfoContainer').child('c2_tsum_info').offspring('spine_arrowhead')
					self.assertFalse(ui.exists(), caseList[21])
					# 检查是否有队长标识
					captain_ui = poco('RoleInfoContainer').child('c2_tsum_info').offspring('sprite_captain')
					self.assertFalse(captain_ui.exists(), caseList[23])
					self.assertTrue(poco("btn_forward").exists(), caseList[24])
					# 检查设为队长按钮
					self.assertTrue(poco('btn_set_leader').exists(), caseList[25])
					setcaptain = TextDic['tsumSetCaptain'].encode('utf-8')
					setcaptain_game = poco('label_set_leader').get_text()
					self.assertEqual(setcaptain_game, setcaptain, caseList[26])
					# 检查松松已达到满级按钮
					self.assertTrue(poco('btn_max_level').exists(), caseList[29])
					upgrade = poco('label_max_level').get_text()
					upgrade_svn = '已达到满级'
					self.assertEqual(upgrade, upgrade_svn, caseList[30])
					# 检查松松的分数显示
					basescore = int(TsumLevelupInfo_dic[tsumstar][tsumlevel][0])
					scoreinfo = poco('label_score_info').get_text()
					score = poco('label_score').get_text()
					info = TextDic['tsum_socre'].encode('utf-8')
					self.assertEqual(scoreinfo + score, info % (basescore, ''), caseList[31])
					# 检查是否关闭了详情面板
					size = poco.get_screen_size()
					G.DEVICE.touch([0.4277778 * size[0], 0.0222222228 * size[1]])
					sleep(0.5)
					self.assertFalse(poco('mask').exists(), caseList[34])
				elif int(num.split('/')[0]) >= int(num.split('/')[1]):
					pocouiname = poco('scrollView').child('table').offspring('c2_progress')[i].child()
					# 检查可以升级的松松是否有升级箭头
					self.assertTrue(pocouiname.offspring('spine_arrowhead').exists(), caseList[11])
					# 点击松松
					pocolist[i].click()
					tsumid = pocolist1[i].child().get_name().split('_')[1]
					tsumname = TextDic['tsum_name_' + tsumid].encode('utf-8')
					sleep(1.0)
					# 检查是否打开了松松详情面板
					self.assertTrue(poco('mask').exists(), caseList[13])
					tsumname_game = poco('label_tsum_name').get_text()
					# 检查松松的名字显示是否正确
					self.assertEqual(tsumname_game, tsumname, caseList[14])
					familyid = TsumInfo_dic[tsumid][0]
					familyname = TextDic['tsum_family_' + familyid].encode('utf-8')
					familyname_game = poco('label_tsum_family').get_text().strip('[]')
					# 检查松松的家族名字是否正确
					self.assertEqual(familyname_game, familyname, caseList[15])
					# 检查技能等级的显示
					tsumstar = TsumInfo_dic[tsumid][1]
					skillinfo = poco('label_skill').get_text()
					index1 = poco('label_skill_level').get_text().find(']')
					index2 = poco('label_skill_level').get_text()[index1 + 1:].find('[')
					skill_level1 = '(' + poco('label_skill_level').get_text()[index1 + 4:index1 + 1 + index2] + ')'
					skill_level2 = '(' + poco('label_skill_level').get_text()[index1 + 4:index1 + 1 + index2] + '+1)'
					skilllv = TsumLevelupInfo_dic[tsumstar][tsumlevel][3]
					uplist = []
					for lv in TsumSkillup_dic[tsumstar][skilllv]:
						uplist.append(int(lv))
					level_to_skillup = max(uplist)
					if int(tsumlevel) < level_to_skillup:
						skill_svn1 = (TextDic['tsum_skill_level'] % (int(skilllv), '')).encode('utf-8')
						self.assertEqual(skillinfo + skill_level1, skill_svn1, caseList[16])
					if int(tsumlevel) == level_to_skillup:
						skill_svn2 = (TextDic['tsum_skill_level'] % (int(skilllv), '+1')).encode('utf-8')
						self.assertEqual(skillinfo + skill_level2, skill_svn2, caseList[17])
					skill_game = TextDic['tsum_skill_des_' + tsumid].encode('utf-8')
					skill = poco('label_skill_desc').get_text()
					# 检查松松的技能描述是否正确
					self.assertEqual(skill_game, skill, caseList[18])
					level_details = poco('label_tsum_level').get_text()
					# 检查松松详情面板显示的松松等级是否与角色列表一致
					self.assertEqual(level_details, levelinfo, caseList[19])
					# 检查松松详情面板是否也显示升级箭头
					ui = poco('RoleInfoContainer').child('c2_tsum_info').offspring('spine_arrowhead')
					self.assertTrue(ui.exists(), caseList[20])
					# 检查是否没有有队长标识
					self.assertFalse(poco('RoleInfoContainer').child('c2_tsum_info').offspring('sprite_captain').exists(), caseList[21])
					self.assertTrue(poco("btn_forward").exists(), caseList[24])
					# 检查设为队长按钮
					self.assertTrue(poco('btn_set_leader').exists(), caseList[25])
					setcaptain = TextDic['tsumSetCaptain'].encode('utf-8')
					setcaptain_game = poco('label_set_leader').get_text()
					self.assertEqual(setcaptain_game, setcaptain, caseList[26])
					# 检查升级按钮
					self.assertTrue(poco('btn_upgrade').exists(), caseList[27])
					upgrade = poco('btn_upgrade').child().child()[1].get_text().split(' ')[0]
					self.assertEqual(upgrade, '升级', caseList[28])
					#检查松松的分数显示
					basescore = int(TsumLevelupInfo_dic[tsumstar][tsumlevel][0])
					scorechange = int(TsumLevelupInfo_dic[tsumstar][str(int(tsumlevel) + 1)][0]) - basescore
					scoreinfo = poco('label_score_info').get_text()
					score = poco('label_score').get_text()
					info = TextDic['tsum_socre'].encode('utf-8')
					scoreinfo_svn = info % (basescore, '[FFD11AFF]+' + str(scorechange) + '[-]')
					self.assertEqual(scoreinfo + score, scoreinfo_svn, caseList[32])
					#检查升级按钮上的金币数量
					cost = TsumLevelupInfo_dic[tsumstar][tsumlevel][1]
					numstart = int(poco('btn_upgrade').child().child()[1].get_text().find(']'))
					cost_game = poco('btn_upgrade').child().child()[1].get_text()[numstart+1:-3]
					self.assertEqual(int(cost), int(cost_game), caseList[33])
					#检查是否关闭了详情面板
					size = poco.get_screen_size()
					G.DEVICE.touch([0.4277778 * size[0], 0.0222222228 * size[1]])
					sleep(0.5)
					self.assertFalse(poco('mask').exists(), caseList[34])
				else:
					pocouiname = poco('scrollView').child('table').offspring('c2_progress')[i].child()
					self.assertFalse(pocouiname.offspring('spine_arrowhead').exists(), caseList[12])
					# 点击松松
					pocolist[i].click()
					tsumid = pocolist1[i].child().get_name().split('_')[1]
					tsumname = TextDic['tsum_name_' + tsumid].encode('utf-8')
					sleep(1.0)
					# 检查是否打开了松松详情面板
					self.assertTrue(poco('mask').exists(), caseList[13])
					tsumname_game = poco('label_tsum_name').get_text()
					# 检查松松的名字显示是否正确
					self.assertEqual(tsumname_game, tsumname, caseList[14])
					familyid = TsumInfo_dic[tsumid][0]
					familyname = TextDic['tsum_family_' + familyid].encode('utf-8')
					familyname_game = poco('label_tsum_family').get_text().strip('[]')
					# 检查松松的家族名字是否正确
					self.assertEqual(familyname_game, familyname, caseList[15])
					#检查技能等级的显示
					tsumstar = TsumInfo_dic[tsumid][1]
					skillinfo = poco('label_skill').get_text()
					index1 = poco('label_skill_level').get_text().find(']')
					index2 = poco('label_skill_level').get_text()[index1 + 1:].find('[')
					skill_level1 = '(' + poco('label_skill_level').get_text()[index1 + 4:index1 + 1 + index2] + ')'
					skill_level2 = '(' + poco('label_skill_level').get_text()[index1 + 4:index1 + 1 + index2] + '+1)'
					skilllv = TsumLevelupInfo_dic[tsumstar][tsumlevel][3]
					uplist = []
					for lv in TsumSkillup_dic[tsumstar][skilllv]:
						uplist.append(int(lv))
					level_to_skillup = max(uplist)
					if int(tsumlevel) < level_to_skillup:
						skill_svn1 = (TextDic['tsum_skill_level'] % (int(skilllv), '')).encode('utf-8')
						self.assertEqual(skillinfo + skill_level1, skill_svn1, caseList[16])
					if int(tsumlevel) == level_to_skillup:
						skill_svn2 = (TextDic['tsum_skill_level'] % (int(skilllv), '+1')).encode('utf-8')
						self.assertEqual(skillinfo + skill_level2, skill_svn2, caseList[17])
					skill_game = TextDic['tsum_skill_des_' + tsumid].encode('utf-8')
					skill = poco('label_skill_desc').get_text()
					# 检查松松的技能描述是否正确
					self.assertEqual(skill_game, skill, caseList[18])
					level_details = poco('label_tsum_level').get_text()
					# 检查松松详情面板显示的松松等级是否与角色列表一致
					self.assertEqual(level_details, levelinfo, caseList[19])
					# 检查松松详情面板是否不显示升级箭头
					ui = poco('RoleInfoContainer').child('c2_tsum_info').offspring('spine_arrowhead')
					self.assertFalse(ui.exists(), caseList[21])
					# 检查是否没有有队长标识
					self.assertFalse(
						poco('RoleInfoContainer').child('c2_tsum_info').offspring('sprite_captain').exists(),caseList[21])
					self.assertTrue(poco("btn_forward").exists(), caseList[24])
					# 检查设为队长按钮
					self.assertTrue(poco('btn_set_leader').exists(), caseList[25])
					setcaptain = TextDic['tsumSetCaptain'].encode('utf-8')
					setcaptain_game = poco('label_set_leader').get_text()
					self.assertEqual(setcaptain_game, setcaptain, caseList[26])
					# 检查松松数量不足按钮
					self.assertTrue(poco('btn_upgrade').exists(), caseList[29])
					upgrade = poco('label_upgrade_tip').get_text()
					upgrade_svn = TextDic['tsum_num_short'].encode('utf-8')
					self.assertEqual(upgrade, upgrade_svn, caseList[30])
					#检查松松的分数显示
					basescore = int(TsumLevelupInfo_dic[tsumstar][tsumlevel][0])
					scoreinfo = poco('label_score_info').get_text()
					score = poco('label_score').get_text()
					info = TextDic['tsum_socre'].encode('utf-8')
					self.assertEqual(scoreinfo+score, info % (basescore, ''), caseList[31])
					#检查是否关闭了详情面板
					size = poco.get_screen_size()
					G.DEVICE.touch([0.4277778 * size[0], 0.0222222228 * size[1]])
					sleep(0.5)
					self.assertFalse(poco('mask').exists(), caseList[34])
	def test_A9(self):
		u"""测试在松松详情面板点击设为队长按钮，该松松角色列表里是否有队长标识
		测试在松松详情面板点击设为队长按钮，该松松详情面板里是否有队长标识
		测试设为队长后设为队长按钮是否置灰不可点击"""
		pocolist = poco('scrollView').child('table').offspring('c2_progress')
		for i in range(len(list(pocolist))):
			captain = poco('scrollView').child('table').offspring('tsumContainer')[i]
			if not captain.child('c2_obtained').offspring('sprite_captain').exists():
				pocolist[i].click()
				page = 'details_panel'
				Click('label_set_leader', page)
				#检查松松设为队长后是否显示队长标识
				captain = poco('scrollView').child('table').offspring('tsumContainer')[i]
				self.assertTrue(captain.child('c2_obtained').offspring('sprite_captain').exists(), caseList[35])
				captain_ui = poco('RoleInfoContainer').child('c2_tsum_info').offspring('sprite_captain')
				self.assertTrue(captain_ui.exists(), caseList[36])
				ui = poco.agent.hierarchy.dump()
				frame = json.dumps(ui, indent=4)
				i = frame.find('btn_set_leader')
				j = frame[i:].find("clickable")
				m = frame[i + j:].find(',')
				self.assertEqual(frame[i + j + 12:i + j + m], 'false', caseList[37])
				sleep(1.0)
				size = poco.get_screen_size()
				G.DEVICE.touch([0.4277778 * size[0], 0.0222222228 * size[1]])
	def test_A10(self):
		u"""测试角色列表里松松显示的升级下级需要的松松的数量显示是否与meta配置一致"""
		global TsumLevelupInfo_dic,TsumInfo_dic
		pocolist = poco('scrollView').child('table').offspring('c2_progress')
		pocolist1 = poco('scrollView').child('table').offspring('c2_tsum')
		if not TsumLevelupInfo_dic:
			GetTsumLevelupInfo(TsumLevelupInfo_dic)
		if not TsumInfo_dic:
			GetTsumInfo(TsumInfo_dic)
		for i in range(len(list(pocolist))):
			# 获取松松信息
			tsumid = pocolist1[i].child().get_name().split('_')[1]
			levelinfo = poco('scrollView').child('table').offspring('label_tsum_level')[i].get_text()
			num = poco('scrollView').child('table').offspring('label_tsum_level_info')[i].get_text()
			tsumlevel = levelinfo.replace('级', '')
			tsumstar = TsumInfo_dic[tsumid][1]
			if 5 != int(tsumlevel):
				nextExp = TsumLevelupInfo_dic[tsumstar][tsumlevel][2]
				#检查松松的升级所需数量
				self.assertEqual(int(num.split('/')[1]), int(nextExp), caseList[38])
			else:
				nextExp = TextDic['tsum_exp_max']
				self.assertEqual(num, nextExp, caseList[39])
	def test_A11(self):
		"""测试金币不足时，升级按钮上的升级所需金币数是否显示为红色
		测试金币不足时，点击升级按钮是否弹出金币不足的提示框
		测试金币不足的提示框显示的文案是否与配置一致
		测试金币不足的提示框是否有确定按钮
		测试点击空白处弹窗会不会关闭
		测试点击金币不足提示框的确定按钮，是否关闭提示框
		测试金币充足时点击升级按钮，角色列表里松松是否等级加一
		测试金币充足时点击升级按钮，详情面板里松松是否等级加一
		测试前段的金币数量显示的是否减去了升级花费的金币数
		测试升级后的松松还能升级时分数显示是否为升级后的分数
		测试升级后的松松不能升级时分数的显示是否为升级后的分数
		测试升级后的升级按钮上的金币数量是否为下次升级需要的金币数"""
		global TsumInfo_dic, TsumLevelupInfo_dic
		if not TsumInfo_dic:
			GetTsumInfo(TsumInfo_dic)
		if not TsumLevelupInfo_dic:
			GetTsumLevelupInfo(TsumLevelupInfo_dic)
		# 获取tsum的meta信息
		pocolist = poco('scrollView').child('table').offspring('c2_progress')
		for i in range(len(list(pocolist))):
			#获取松松信息
			levelinfo = poco('scrollView').child('table').offspring('label_tsum_level')[i].get_text()
			tsumlevel = levelinfo.replace('级', '')
			num = poco('scrollView').child('table').offspring('label_tsum_level_info')[i].get_text()
			exp_max = TextDic['tsum_exp_max']
			pocolist1 = poco('scrollView').child('table').offspring('c2_tsum')
			tsumid = pocolist1[i].child().get_name().split('_')[1]
			if num != exp_max:
				if int(num.split('/')[0]) >= int(num.split('/')[1]):
					pocolist[i].click()
					#获取当前的金币数
					headlist = poco('HeaderPart').child("c2_currency").offspring('label_count')
					coin_old = int(headlist[1].get_text())
					tsumstar = TsumInfo_dic[tsumid][1]
					cost = int(TsumLevelupInfo_dic[tsumstar][tsumlevel][1])
					page = 'details_panel'
					#分金币充足和不足两种情况
					if cost <= coin_old:
						#点击升级按钮
						Click('btn_upgrade', page)
						sleep(2.5)
						#检查等级变化
						levelinfo1 = poco('scrollView').child('table').offspring('label_tsum_level')[i].get_text()
						tsumlevel_new = int(levelinfo1.replace('级', ''))
						self.assertEqual(tsumlevel_new, int(tsumlevel)+1, caseList[46])
						level_details = int(poco('label_tsum_level').get_text().replace('级', ''))
						self.assertEqual(level_details, int(tsumlevel)+1, caseList[47])
						#检查金币数
						#coin_new = int(headlist[1].get_text())
						#print coin_new,coin_old
						#self.assertEqual(coin_new, coin_old-cost, caseList[46])
						#检查分数
						num1 = poco('scrollView').child('table').offspring('label_tsum_level_info')[i].get_text()
						#还能升级时的分数显示
						if int(num1.split('/')[0]) >= int(num1.split('/')[1]):
							basescore = int(TsumLevelupInfo_dic[tsumstar][str(int(tsumlevel)+1)][0])
							scorechange = int(TsumLevelupInfo_dic[tsumstar][str(int(tsumlevel)+2)][0]) - basescore
							scoreinfo = poco('label_score_info').get_text()
							score = poco('label_score').get_text()
							info = TextDic['tsum_socre'].encode('utf-8')
							scoreinfo_svn = info % (basescore, '[FFD11AFF]+' + str(scorechange) + '[-]')
							self.assertEqual(scoreinfo + score, scoreinfo_svn, caseList[49])
							# 检查升级按钮上的金币数的变化
							cost_new = int(TsumLevelupInfo_dic[tsumstar][str(int(tsumlevel) + 1)][1])
							numstart = int(poco('btn_upgrade').child().child()[1].get_text().find(']'))
							cost_game = poco('btn_upgrade').child().child()[1].get_text()[numstart + 1:-3]
							self.assertEqual(int(cost_new), int(cost_game), caseList[51])
							sleep(1.0)
							size = poco.get_screen_size()
							G.DEVICE.touch([0.4277778 * size[0], 0.0222222228 * size[1]])
						else:
							basescore = int(TsumLevelupInfo_dic[tsumstar][str(int(tsumlevel)+1)][0])
							scoreinfo = poco('label_score_info').get_text()
							score = poco('label_score').get_text()
							info = TextDic['tsum_socre'].encode('utf-8')
							self.assertEqual(scoreinfo + score, info % (basescore, ''), caseList[50])
							#检查升级按钮变为松松数量不足
							upgrade = poco('label_upgrade_tip').get_text()
							upgrade_svn = TextDic['tsum_num_short'].encode('utf-8')
							self.assertEqual(upgrade, upgrade_svn, caseList[52])
							sleep(1.0)
							size = poco.get_screen_size()
							G.DEVICE.touch([0.4277778 * size[0], 0.0222222228 * size[1]])
						sleep(1.0)
						size = poco.get_screen_size()
						G.DEVICE.touch([0.4277778 * size[0], 0.0222222228 * size[1]])
					#金币不足
					else:
						# 获取金币数量的颜色
						colourstart = int(poco('btn_upgrade').child().child()[1].get_text().find('['))
						colourend = int(poco('btn_upgrade').child().child()[1].get_text().find(']'))
						cost_game = poco('btn_upgrade').child().child()[1].get_text()[colourstart:colourend+1]
						self.assertEqual(cost_game, '[FF0000B2]', caseList[40])
						#点击升级按钮
						Click('btn_upgrade', page)
						#检查金币不足面板
						self.assertTrue(poco('tex_bottom').exists(), caseList[41])
						tips = poco('PromptPopupPanel').offspring('label_info').get_text()
						self.assertEqual(tips, '金币数量不够', caseList[42])
						#检查是否有确定按钮
						self.assertTrue(poco('btn_ok').exists(), caseList[43])
						#点击空白处
						size = poco.get_screen_size()
						G.DEVICE.touch([0.4277778 * size[0], 0.0222222228 * size[1]])
						self.assertTrue(poco('tex_bottom').exists(), caseList[44])
						#点击确定按钮
						page = 'cointips_popup'
						Click('btn_ok', page)
						self.assertFalse(poco('tex_bottom').exists(), caseList[45])
						sleep(1.0)
						size = poco.get_screen_size()
						G.DEVICE.touch([0.4277778 * size[0], 0.0222222228 * size[1]])
	def test_A12(self):
		"""测试角色列表是否有排序按钮"""
		self.assertTrue(poco('label_sort').exists(), caseList[53])
	def test_A13(self):
		"""测试角色列表排序按钮的文案显示是否符合需求"""
		sortinfoList = ['按稀有度降序', '按基础分数降序','按家族降序']
		btninfo = poco('label_sort').get_text()
		self.assertIn(btninfo, sortinfoList, caseList[54])
	def test_A14(self):
		"""测试角色列表的松松是否按照排序按钮的显示来排序"""
		global TsumInfo_dic, TsumLevelupInfo_dic
		if not TsumInfo_dic:
			GetTsumInfo(TsumInfo_dic)
		if not TsumLevelupInfo_dic:
			GetTsumLevelupInfo(TsumLevelupInfo_dic)
		# 获取tsum的meta信息
		star_list = []
		family_list = []
		score_list = []
		page = 'tsumlist'
		Click('label_sort', page)
		pocolist = poco('scrollView').child('table').offspring('c2_progress')
		pocolist1 = poco('scrollView').child('table').offspring('c2_tsum')
		for i in range(len(list(pocolist))):
			# 获取松松信息
			levelinfo = poco('scrollView').child('table').offspring('label_tsum_level')[i].get_text()
			tsumlevel = levelinfo.replace('级', '')
			tsumid = pocolist1[i].child().get_name().split('_')[1]
			star_list.append(TsumInfo_dic[tsumid][1])
			family_list.append(TsumInfo_dic[tsumid][0])
			score_list.append(TsumLevelupInfo_dic[TsumInfo_dic[tsumid][1]][tsumlevel][0])
		sortinfoList = ['按稀有度降序', '按基础分数降序', '按家族降序']
		btninfo = poco('label_sort').get_text()
		#检查按稀有度排序
		if btninfo == sortinfoList[0]:
			for s in range(len(star_list)-1):
				self.assertTrue(int(star_list[s]) >= int(star_list[s+1]), caseList[55])
		#检查按基础分数排序
		elif btninfo == sortinfoList[1]:
			for c in range(len(score_list)-1):
				self.assertTrue(int(score_list[c]) >= int(score_list[c+1]), caseList[55])
		# 检查家族排序
		else:
			for f in range(len(family_list) - 1):
				self.assertTrue(int(family_list[f]) >= int(family_list[f + 1]), caseList[55])
	def test_A15(self):
		"""测试点击排序按钮后的排序显示是否符合规则"""
		global TsumInfo_dic, TsumLevelupInfo_dic
		if not TsumInfo_dic:
			GetTsumInfo(TsumInfo_dic)
		if not TsumLevelupInfo_dic:
			GetTsumLevelupInfo(TsumLevelupInfo_dic)
		# 获取tsum的meta信息
		star_list = []
		family_list = []
		score_list = []
		page = 'tsumlist'
		Click('label_sort', page)
		pocolist = poco('scrollView').child('table').offspring('c2_progress')
		pocolist1 = poco('scrollView').child('table').offspring('c2_tsum')
		for i in range(len(list(pocolist))):
			# 获取松松信息
			levelinfo = poco('scrollView').child('table').offspring('label_tsum_level')[i].get_text()
			tsumlevel = levelinfo.replace('级', '')
			tsumid = pocolist1[i].child().get_name().split('_')[1]
			star_list.append(TsumInfo_dic[tsumid][1])
			family_list.append(TsumInfo_dic[tsumid][0])
			score_list.append(TsumLevelupInfo_dic[TsumInfo_dic[tsumid][1]][tsumlevel][0])
		sortinfoList = ['按稀有度降序', '按基础分数降序', '按家族降序']
		btninfo = poco('label_sort').get_text()
		# 检查按稀有度排序
		if btninfo == sortinfoList[0]:
			for s in range(len(star_list) - 1):
				self.assertTrue(int(star_list[s]) >= int(star_list[s + 1]), caseList[56])
		# 检查按基础分数排序
		elif btninfo == sortinfoList[1]:
			for c in range(len(score_list) - 1):
				self.assertTrue(int(score_list[c]) >= int(score_list[c + 1]), caseList[56])
		# 检查家族排序
		else:
			for f in range(len(family_list) - 1):
				self.assertTrue(int(family_list[f]) >= int(family_list[f + 1]), caseList[56])
	def test_A16(self):
		"""测试再次点击排序按钮后的排序显示是否符合规则"""
		global TsumInfo_dic, TsumLevelupInfo_dic
		if not TsumInfo_dic:
			GetTsumInfo(TsumInfo_dic)
		if not TsumLevelupInfo_dic:
			GetTsumLevelupInfo(TsumLevelupInfo_dic)
		# 获取tsum的meta信息
		star_list = []
		family_list = []
		score_list = []
		page = 'tsumlist'
		Click('label_sort', page)
		pocolist = poco('scrollView').child('table').offspring('c2_progress')
		pocolist1 = poco('scrollView').child('table').offspring('c2_tsum')
		for i in range(len(list(pocolist))):
			# 获取松松信息
			levelinfo = poco('scrollView').child('table').offspring('label_tsum_level')[i].get_text()
			tsumlevel = levelinfo.replace('级', '')
			tsumid = pocolist1[i].child().get_name().split('_')[1]
			star_list.append(TsumInfo_dic[tsumid][1])
			family_list.append(TsumInfo_dic[tsumid][0])
			score_list.append(TsumLevelupInfo_dic[TsumInfo_dic[tsumid][1]][tsumlevel][0])
		sortinfoList = ['按稀有度降序', '按基础分数降序', '按家族降序']
		btninfo = poco('label_sort').get_text()
		# 检查按稀有度排序
		if btninfo == sortinfoList[0]:
			for s in range(len(star_list) - 1):
				self.assertTrue(int(star_list[s]) >= int(star_list[s + 1]), caseList[57])
		# 检查按基础分数排序
		elif btninfo == sortinfoList[1]:
			for c in range(len(score_list) - 1):
				self.assertTrue(int(score_list[c]) >= int(score_list[c + 1]), caseList[57])
		# 检查家族排序
		else:
			for f in range(len(family_list) - 1):
				self.assertTrue(int(family_list[f]) >= int(family_list[f + 1]), caseList[57])
	def test_A17(self):
		"""测试角色列表的排序按钮显示的位置是否符合需求"""
		pos = poco('label_sort').get_position()
		pos1 = float('%.1f' % pos[0])
		pos2 = float('%.1f' % pos[1])
		self.assertTrue(pos1 == 0.9 and pos2 == 0.1, caseList[58])
	def test_A18(self):
		"""测试是否可以上下滑动角色列表"""
		pos1 = poco('scrollView').child('table').offspring('label_info')[0].get_position()
		#向下滑动、向上滑动、再向下滑动
		poco('scrollView').child('table').offspring('label_info')[0].swipe([0, 0.5])
		poco('scrollView').child('table').offspring('label_info')[1].swipe([0, -0.5])
		poco('scrollView').child('table').offspring('label_info')[1].swipe([0, 0.5])
		sleep(1.5)
		pos2 = poco('scrollView').child('table').offspring('label_info')[0].get_position()
		self.assertEqual(pos1, pos2, caseList[59])
	def test_A19(self):
		"""测试角色列表是否有返回按钮"""
		self.assertTrue(poco('btn_return').exists(), caseList[60])
	def test_A20(self):
		"""测试点击返回按钮是否回到城建界面"""
		page = 'tsumlist'
		Click('btn_return', page)
		self.assertTrue(poco('c2_left').exists(), caseList[61])
		sleep(2.0)
	@classmethod
	def tearDownClass(cls):
		for i in range(3):
			if not poco('c2_left').exists():
				if poco('tex_bottom').exists():
					poco('btn_ok').click()
				else:
					poco('btn_return').click()
				i += 1
			else:
				break

if __name__ == '__main__':
	unittest.main()