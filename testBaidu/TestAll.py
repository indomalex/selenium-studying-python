#coding:utf-8

import os
import sys
import unittest
import HTMLTestRunner
from time import strftime, localtime

#在test_cases下的__init__.py里写了from test_cases import TestBaiKe以下*才有效
from test_cases import *



if __name__ =="__main__":
    #这块代码以shell命令行的方式运行test_cases里的所有测试用例
#     testCasesPath = os.path.abspath(".") + "\\test_cases"
#     caseList = os.listdir(testCasesPath)
#     for f in caseList:
#         if f.find(".") != -1:
#             if f.split(".")[1] == "py" and f[:4] == "Test":
#                 os.system("python D:\\eclipse-workspace\\TestBaidu_Taobao\\src\\test_cases\\%s 1>>log.txt 2>&1" %f)
#         

    
    
    
    #这里以正规方式运行test_cases里的所有测试用例,并用htmltestrunner输出
    unit = unittest.TestSuite()
    
    #收集所有待测用例
#     unit.addTest(unittest.makeSuite(TestBaiKe.TestBaiKe))
    #更好的办法：用discover一次性找到test_cases下所有的待测用例
    curPath = os.getcwd() + "\\test_cases"
    discover = unittest.defaultTestLoader.discover(curPath, "Test*.py", top_level_dir=None)
    for suit in discover:
        for case in suit:
            unit.addTest(case)
    
    #用HTMLTestRunner来生成测试报告 
    now = strftime("%Y-%m-%d-%H_%M_%S", localtime())
    reportName = os.path.abspath(".") + "\\" + now + "_report.html"
    try:
        report = open(reportName, 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=report,
            title=u'百度测试报告',
            description=u'用例执行情况：'
            )
        runner.run(unit)
    except IOError as info:
        print("文件读写出现异常：" + info)
    finally:
        report.close()
        
        
