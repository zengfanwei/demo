# coding=utf-8

import requests, json
from urllib import urlencode


def updateData(uid, logic, data, param=''):
	headers = {'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Accept': 'text/plain'}
	newData = {}
	newData['json'] = data
	newData['param'] = param
	newData['logic'] = logic

	dataDic = json.loads(data)
	if dataDic['uid'] != int(uid):
		print "修改数据中的uid与要修改的uid不一致，请修改！"
		return False

	err = 0
	url = 'http://popcornbox.happyelements.net:8850/data.do?method=update&uid=%s&env=tsumtsum_qa&pf=apple&check=false' % uid
	r = requests.post(url, data=urlencode(newData), headers=headers)
	#r.auth = ('service_auth', 'qwer1234!')

	if 200 != r.status_code:
		err += 1

	if err == 0:
		return True
	else:
		print "输入的参数有问题，请检查数据格式是否正确！"
		return False

def queryData(uid, logic, item, param=''):
	headers = {'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Accept': 'text/plain'}
	url = 'http://popcornbox.happyelements.net:8850/data.do?method=query&param=%s&logic=%s&uid=%s&env=tsumtsum_qa&pf=apple&check=false' % (param, logic, uid)
	r = requests.post(url, headers=headers)
	urlData = json.loads(r.text)
	if item not in urlData.keys():
		print '您输入的参数有问题，请重新来过！'
		return False
	else:
		if not urlData[item]:
			return 0
		else:
			return urlData[item]

if __name__ == '__main__':
	d = '''{
  "uid": 12011,
  "coin": 6000,
  "energy": 72,
  "cash": 26,
  "level": 1,
  "updateTime": 1560236730647,
  "tsumId": 0,
  "material": 46,
  "createTime": 1559673353079,
  "lastLoginTime": 1560236730647,
  "continueLoginDays": 2,
  "activeDays": 4,
  "coinLimit": 0,
  "qualifyingPoint": 2000,
  "newbie": false
}'''
	i = '12011'
	l = 'User'
	#updateData(i, l, d)
	queryData(i, 'User', 'coin')