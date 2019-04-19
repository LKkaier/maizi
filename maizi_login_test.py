# encoding=utf-8
from selenium import webdriver
import configparser
import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import time

def get_ele_wait(browser, times, func):
    return WebDriverWait(browser,times).until(func)

def openUrl(browser,url):
    browser.get(url)
    browser.maximize_window()

def findElement(browser,arg):

    if 'text_id' in arg:
        ele_login = get_ele_wait(browser,10,lambda browser: browser.find_element_by_link_text(arg['text_id']))
        try:
            ele_login.click()
        except Exception as e:
            print(e)
            time.sleep(1)
            ele_login.click()
    userEle = browser.find_element_by_id(arg['userid'])
    pswEle = browser.find_element_by_id(arg['pswid'])
    loginEle = browser.find_element_by_id(arg['loginid'])
    print(userEle,pswEle,loginEle)
    return userEle,pswEle,loginEle

def sendVals(eletuple,arg):
    listkey = ['uname','psw']
    i = 0
    for key in listkey:
        # eletuple[i].send_keys('')
        try:
            eletuple[i].clear()
        except Exception as e:
            print(e)
            time.sleep(1)

        eletuple[i].send_keys(arg[key])
        i+=1
    eletuple[-1].click()

def checkResult(browser,text):
    try:
        browser.find_element_by_partial_link_text(text)
        print('Account login fail')
    except:
        print('Account login well')

def login_test(ele_dict,userlist):
    browser = webdriver.Chrome()
    browser.implicitly_wait(5)
    openUrl(browser,ele_dict['url'])

    for userinfo in userlist:
        ele_tuple = findElement(browser,ele_dict)
        sendVals(ele_tuple,userinfo)
        checkResult(browser,"失败")
        ele = browser.find_element_by_partial_link_text(ele_dict['logoutText'])
        ele.click()


if __name__ == '__main__':
    # ele_dict = {'url':url,'text_id': login_text, 'userid': 'id_account_l', 'pswid': 'id_password_l', 'loginid': 'login_btn'}
    # account_dict = {'uname': account, 'psw': psw}
    # login_test(ele_dict)
    config = configparser.ConfigParser()
    config.read("config.ini", encoding='utf-8')
    # config.read()
    # print(config.sections())

    userlist=[]
    for sec in config.sections():
        if "user." in sec:
            userlist.append({"uname": config[sec]['uname'],'psw': config[sec]['psw']})
    print(userlist)

    ele_dict = {'url': config['webinfo']['url'], 'text_id': config['webinfo']['text_id'],'userid': config['webinfo']['userid'], 'pswid': config['webinfo']['pswid'],
                'loginid': config['webinfo']['loginid'],'logoutText': config['webinfo']['logoutText']}
    print(ele_dict)
    login_test(ele_dict,userlist)
