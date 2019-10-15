# coding=utf-8

from poco.drivers.unity3d import UnityPoco
poco = UnityPoco()

def accessControlInfo(start, spring, text=True):
	accessInfos = []

	with poco.freeze() as frozen_poco:
		for item in frozen_poco(start).offspring(spring):
			if text:
				accessInfos.append(item.get_text())
			else:
				accessInfos.append(item)
	return accessInfos
