#coding:utf-8
'''
Created on 2017年12月6日

@author: Administrator
'''
import unittest
import os
import time
from public import LoginOut, FileOpenClose
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver


class TestBaiKe(unittest.TestCase):


    def setUp(self):
        LoginOut.setUp(self)        

    def tearDown(self):
        LoginOut.setDown(self)

    @unittest.skip("暂时不测testBaikeSearch")
    def testBaikeSearch(self):
        pathForRead = os.path.dirname(os.path.dirname(__file__)) + "\\inputInfo\\wordsForSearch"
        sourceFile = FileOpenClose.openMyFile(pathForRead)
        values = FileOpenClose.readLinesFromMyFile(sourceFile)
    
        pathForWrite = os.path.dirname(os.path.dirname(__file__)) + "\\outputInfo\\resultInfo"
        resultFile = FileOpenClose.openMyFile(pathForWrite, "a+")
    
        browser = self.driver
    
        for v in values:
            browser.find_element_by_id("query").send_keys(v)
            browser.find_element_by_id("search").click()
            time.sleep(3)
#                 elements = browser.find_elements_by_xpath("/html/body/div[4]/div[2]/div/div[2]/div[5]/div[1]//*")
#                 div = browser.find_element_by_xpath("/html/body/div[4]/div[2]/div/div[2]/div[5]/div[1]")
            div = browser.find_element_by_xpath("//div[@class='para'][1]")
            
            txt = div.get_attribute("textContent")
#                 for ele in elements:
#                     txt = txt + ele.get_attribute('textContent')
            txt = txt.replace(u"\xa0", u" ") + "\n\n\n"
            FileOpenClose.writeToMyFile(resultFile, txt)
            txt = ""
            browser.find_element_by_id("query").clear()
        
        FileOpenClose.closeMyFile(sourceFile)
        FileOpenClose.closeMyFile(resultFile)
    
    @unittest.skip("暂时不测testBaikeLogins")    
    def testBaikeLogins(self):
        #检查一批账号是否登录成功
        csvPath = os.path.dirname(os.path.dirname(__file__)) + "\\inputInfo\\accounts.csv"
        csvFile = FileOpenClose.openMyFile(csvPath)
        accounts = FileOpenClose.readLinesFromMyCSVFile(csvFile)
        for acc in accounts:
            tip = LoginOut.Login(self, acc)
            b = True if "请输入验证码" == str(tip) or "" == str(tip) else False
            self.assertTrue(b) #如果成功登录或者显示“请输入验证码”都算通过
            
            time.sleep(2)
            if str(tip) == "":
                LoginOut.LogOut(self)
        
        FileOpenClose.closeMyFile(csvFile)
        
        
    def testBaikeMenuAndPageJumping(self):
        u'百度百科里点击弹出菜单实现页面两连跳'
        #打开百科，鼠标悬停在搜索栏下方的菜单栏，显示出级联菜单，点击分类其中的科学，
        #页面跳转，在其中点击一个词条，再跳转，在页面中取出词条第一自然段的解释存至
        #resultInfo中，关闭所有页面。
        
        #打开firefox并打开百科
        #此步已经交给setup
        
        time.sleep(3)
        #鼠标悬停在菜单上，点击分类下的科学
        a = self.driver.find_element_by_class_name("technology")
        a.click()
#         navBar = self.driver.find_element_by_class_name("navbar-bg-top")
#         ActionChains(self.driver).move_to_element(navBar)
#         time.sleep(1)
#         ActionChains(self.driver).move_to_element(a).click()
        
        #跳转的页面
        time.sleep(3) #一定要等一会，否则还没打开
        self._JumpToPage()
        #定位
        div = self.driver.find_element_by_class_name("hotLemma-container")
        #注意xpath定位。若前边加了/表明是从整个文档的开头，//表明是搜索下边任何位置
        a = div.find_element_by_xpath("div[1]/a[1]") #这里说明，可以基于已经找到的元素再定位，再定位时前边不要加“/”
#         a = self.driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div[1]/a[1]")
        a.click()
        
        #在再跳转的页面中取出词条第一段。
        time.sleep(3)
        self._JumpToPage()
        div = self.driver.find_element_by_xpath("//div[@class='para'][1]")
        txt = div.get_attribute("textContent")
        txt = txt.replace(u"\xa0", u" ") + "\n\n\n"
        
        #打开resultinfo并存入其中
            #这样写容易出现问题。abspath不是当前文件所在绝对路径，而是运行时那个文件的绝对路径
#         pathForWrite = os.path.abspath("..") + "\\outputInfo\\resultInfo"
        #os.getcwd()和abspath一样，是返回运行时那个文件的路径，不是当前文件路径
        
        #dirname(__file__)返回当前文件的路径，要返回上一级，则dirname(当前文件路径)
        
        #在路径间移动：推荐用os.path.join(当前路径, "../..")，但用了之后它只是附加在路径后边../..，要用abspath才能执行上跳目录路径
        
        pathForWrite = os.path.dirname(os.path.dirname(__file__)) + "\\outputInfo\\resultInfo"
        resultFile = FileOpenClose.openMyFile(pathForWrite, "a+")
        FileOpenClose.writeToMyFile(resultFile, txt)
        FileOpenClose.closeMyFile(resultFile)
        
        #关闭所有页面
        #交给setDown去做了
        # self.driver.close() 可以只关闭当前标签页
        
    
    
    def _JumpToPage(self, num=-1):
        #如果num为-1表示新打开一个窗口，将新句柄加入列表，切换到新窗口，返回新窗口在列表中的位置
        #如果num不为-1表示打开一个已经打开的窗口，切换到该旧窗口，返回该窗口在列表里的位置
        allHandles = self.driver.window_handles
        if num == -1:
            for hd in allHandles:
                if hd not in self.handles:
                    self.handles.append(hd)
                    self.driver.switch_to_window(hd)
                    return self.handles.index(hd)
        else:
            self.driver.switch_to_window(self.handles[num])
            return num
    
    

if __name__ == "__main__":
    #第一种调用方式
#     unittest.main()

    #第二种
#     suit = unittest.TestSuite()
#     suit.addTest(TestBaiKe("testBaikeSearch"))
#     suit.addTest(TestBaiKe("testBaikeLogins"))
#     suit.addTest(TestBaiKe("testBaikeMenuAndPageJumping"))
#     runner = unittest.TextTestRunner()
#     runner.run(suit)
    
    #第三种
    suit = unittest.makeSuite(TestBaiKe, "test") #找到以test为前缀的待测方法
    runner = unittest.TextTestRunner()
    runner.run(suit)
