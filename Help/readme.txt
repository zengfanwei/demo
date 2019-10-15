config.py修改配置

..Case/Function中的import HTMLTestRunnerCN，pip找不到，手动加..Python27\Lib

如果本机未安装airtest，修改..\Python27\Lib\site-packages\airtest\core\android\constant.py，Windows路径value
DEFAULT_ADB_PATH = {
    	"Windows": "C:\\Users\\Administrator\\AppData\\Local\\Android\\android-sdk\\platform-tools\\adb",
	......


D:\workspace\UITest_TsumTsum\report\OldReport\2018-10-00-20-00-08 OPPO_R11 report.html