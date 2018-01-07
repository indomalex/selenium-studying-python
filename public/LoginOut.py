#coding:utf-8
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains

def setUp(self):
    self.driver = webdriver.Firefox()
    self.driver.implicitly_wait(15)
    self.base_url = "http://baike.baidu.com/"
    self.driver.get(self.base_url)
    self.verificationErrors = []
    self.handles = [self.driver.current_window_handle] #用于记录多个窗口情况下每个窗口的句柄

    
    
def setDown(self):
    self.driver.quit()
    self.assertEqual([], self.verificationErrors, "出错了！")
   
    
def Login(self, account):
    #由于验证码的问题无法实现自动化登录，仅以是否弹出了验证码错误提示来判断是否走完了登录流程
    a = self.driver.find_element_by_xpath("//a[@data-action='login'][1]")
#     a = self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/ul/li[2]/a")
    a.click()
    self.driver.find_element_by_id("TANGRAM__PSP_10__userName").send_keys(account[0])
    self.driver.find_element_by_id("TANGRAM__PSP_10__password").send_keys(account[1])
    self.driver.find_element_by_id("TANGRAM__PSP_10__submit").click()
#     loginBtn = self.driver.find_element_by_id("TANGRAM__PSP_10__submit")
#     ActionChains(self.driver).click(loginBtn).perform()
    time.sleep(2)
    try:
        tip = self.driver.find_element_by_id("TANGRAM__PSP_10__error").get_attribute("textContent")
    except:tip = "" #如果成功登录则登录框会消失，此元素将不存在；如果未输入验证码则会出现提示。
    return tip
    
    

def LogOut(self):
    #仅把用户名和登录框置空，和点击了关闭弹框窗口作为退出流程
    self.driver.find_element_by_id("TANGRAM__PSP_10__userName").clear()
    self.driver.find_element_by_id("TANGRAM__PSP_10__password").clear()
    self.driver.find_element_by_id("TANGRAM__PSP_4__closeBtn").click()
    
    