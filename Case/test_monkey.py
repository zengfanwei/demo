# coding=utf-8

from airtest.core.helper import G
from airtest.core.api import *
from poco.drivers.unity3d import UnityPoco
import random
import time
import unittest


class Monkey(unittest.TestCase):
	def test1(self):
		resolution = G.DEVICE.get_current_resolution()
		old = time.time()
		while True:
			pos1 = random.uniform(0, resolution[0])
			pos2 = random.uniform(0, resolution[1])
			G.DEVICE.touch((pos1, pos2))
			new = time.time()
			if (new - old) > 60.0:
				break

	def test2(self):
		stop_app('com.tencent.TsumTsumAndroid')
		sleep(3.0)
		start_app('com.tencent.TsumTsumAndroid')
		wait(Template(r"D:\\workspace\\UITest_TsumTsum\\Case\\photo\\tpl1568629745795.png", record_pos=(-0.01, 0.91), resolution=(720, 1496)))
		poco = UnityPoco()
		sleep(1.0)
		poco("btn_start_level").click()
		sleep(2.0)
		poco(
			absoluteName="UI Root/ChapterPopupPanel/ChapterContainer/list_chapter/scrollView/table/0002/btn_content/chapter_1/tex_chapter").click()
		sleep(1.0)
		poco("level_2").click()
		sleep(1.0)
		poco("btn_start").click()
		resolution = G.DEVICE.get_current_resolution()
		old = time.time()
		while True:
			pos1 = random.uniform(0, resolution[0])
			pos2 = random.uniform(400, resolution[1] - 400)
			pos3 = random.uniform(0, resolution[0])
			pos4 = random.uniform(400, resolution[1] - 400)
			G.DEVICE.swipe((pos1, pos2), (pos3, pos4))
			new = time.time()
			if (new - old) > 65.0:
				break

if __name__ == "__main__":
	unittest.main()