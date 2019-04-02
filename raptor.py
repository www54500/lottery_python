#Taiwan Lottery
import time
import os
from datetime import datetime
from datetime import timedelta
from selenium import webdriver

def tryclick(driver, selector, count=0): ##保護機制，以防無法定位還沒渲染出來的元素
    try:
        elem = driver.find_element_by_css_selector(selector)
        # elem = driver.find_element_by_xpath(Xpath)  # 如果你想透過Xpath定位元素
        elem.click() # 點擊定位到的元素
    except:
        time.sleep(2)
        count+=1
        if(count < 128):
            tryclick(driver, selector,count)
        else:
            print("cannot locate element:" + selector)
            
def tryclickbasketball(driver, count=0): ##保護機制，以防無法定位還沒渲染出來的元素
    try:
        games = driver.find_elements_by_class_name("wn-Classification ")
        for g in games:
            if (g.text == "Basketball"):
                elem = g
                break
        # elem = driver.find_element_by_xpath(Xpath)  # 如果你想透過Xpath定位元素
        elem.click() # 點擊定位到的元素
    except:
        time.sleep(2)
        count+=1
        if(count < 128):
            tryclickbasketball(driver, count)
        else:
            print("cannot locate [Basketball]")

def tryclickusdate(driver, count=0): ##保護機制，以防無法定位還沒渲染出來的元素
    try:
        uset = (datetime.today() + timedelta(hours = -12)).strftime("%d") # us eastern dst time
        datelist = driver.find_elements_by_css_selector("#scoreboard-date-navigation > div.os-sly.nba > div.frame.undefined > ul > li")
        for d in datelist:
            if (uset in d.text):
                elem = d
                break
        # elem = driver.find_element_by_xpath(Xpath)  # 如果你想透過Xpath定位元素
        elem.click() # 點擊定位到的元素
    except:
        time.sleep(2)
        count+=1
        if(count < 128):
            tryclickbasketball(driver, count)
        else:
            print("cannot locate " + (datetime.today() + timedelta(hours = -12)).strftime("%a %d"))
            
def tryget(driver, selector, count=0): ##保護機制，以防無法定位還沒渲染出來的元素
    try:
        elem = driver.find_element_by_css_selector(selector)
        # elem = driver.find_element_by_xpath(Xpath)  # 如果你想透過Xpath定位元素
        return elem;
    except:
        time.sleep(2)
        count+=1
        if(count < 128):
            tryclick(driver, selector,count)
        else:
            print("cannot locate element:" + selector)
            
browser = webdriver.Chrome()
browser.get('http://www.sportslottery.com.tw/zh/web/guest/sports-betting')       
tryclick(browser, "#s-442 > div.accordion-heading.normal.sports > a")
tryclick(browser, "#tour_t-4102 > span.event.ellipsis")
browser.refresh()
date_e = tryget(browser, "#tournamentContainer > div > div > div > div > div > div > span")
date = date_e.text[9:11] + date_e.text[14:16] + str((int(date_e.text[3:6]) + 1911) % 100)
folder = "./" + date  
if not os.path.exists(folder):
    os.makedirs(folder)
datet = time.strftime("%Y%m%d%H%M", time.localtime())
path = folder + "/" + datet + "_twlottery.txt"
file = open(path, 'w', encoding='utf8')
time.sleep(2)
element = tryget(browser, "div.dataBox:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)")
file.write(element.text)
file.close()
#=========================================================================================================================================================================================================================================================================================================================================================
#Bet365
browser.get('https://www.bet365.com/en/')
browser.get('https://www.bet365.com/')
tryclickbasketball(browser)
tryclick(browser, "body > div:nth-child(1) > div > div.wc-PageView > div.wc-PageView_Main > div > div.wc-CommonElementStyle_PrematchCenter.wc-SplashPage_CenterColumn > div.sm-SplashModule > div.sm-SplashContainer > div:nth-child(2) > div.sm-MarketGroup_Open > div:nth-child(1) > div.sm-MarketContainer.sm-MarketContainer_NumColumns2.sm-Market_Open > div:nth-child(1) > div.sm-CouponLink_Label")
path = folder + "/" + datet + "_bet365.txt"
file = open(path, 'w', encoding='utf8')
element = tryget(browser, "body > div:nth-child(1) > div > div.wc-PageView > div.wc-PageView_Main > div > div.wc-CommonElementStyle_PrematchCenter > div.cm-CouponModule > div > div.gl-MarketGroup.cm-CouponMarketGroup.cm-CouponMarketGroup_Open > div.gl-MarketGroup_Wrapper.cm-MarketGroupContainerForHeader")
element = browser.find_element_by_css_selector("body > div:nth-child(1) > div > div.wc-PageView > div.wc-PageView_Main > div > div.wc-CommonElementStyle_PrematchCenter > div.cm-CouponModule > div > div.gl-MarketGroup.cm-CouponMarketGroup.cm-CouponMarketGroup_Open > div.gl-MarketGroup_Wrapper.cm-MarketGroupContainerForHeader")
file.write(element.text)
file.close()
#=========================================================================================================================================================================================================================================================================================================================================================
#Oddsshark
browser.get('https://www.oddsshark.com/nba/scores')
path = folder + "/" + datet + "_oddsshark.txt"
file = open(path, 'w', encoding='utf8')
tryclickusdate(browser)
time.sleep(2)
element = tryget(browser, "#oslive-scoreboard > div")
file.write(element.text)
file.close()
browser.close()
print("finished, the filename is " + datet)