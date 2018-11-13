from selenium import webdriver
import requests
from time import sleep
import re
import base64
from PIL import Image
import json
def tiqucookies():
    brown=webdriver.Chrome()
    session=requests.session()
    session.headers.clear()
    brown.get('https://www.zhihu.com/signup?next=%2F')
    brown.find_element_by_css_selector('.SignContainer-switch span').click()
    brown.find_element_by_css_selector('.SignFlow-accountInput input').send_keys('13560414027')
    brown.find_element_by_css_selector('.SignFlow-password .SignFlowInput .Input-wrapper input').send_keys('abc.12345')
    try:
        img=''
    except:
        img=brown.find_element_by_css_selector('.Captcha-englishContainer img').get_attribute('src')
        sleep(5)
        yzmimage=re.findall(r'base64,(.*)',img,re.S)
        if yzmimage!='null':
            image=base64.decode(yzmimage)
            with open('yzm.jpg','wb') as f:
                f.write(image)
                f.close()
            try:
                im=Image.open()
                im.show('yzm.jpg')
                im.close()
                sleep(10)
                yzmlogin = input()
                brown.find_element_by_css_selector('.SignFlowInput .Input-wrapper input').send_keys(yzmlogin)
            except:
                pass
    else:
        pass
    brown.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/button').click()
    sleep(5)
    cookies=brown.get_cookies()
    sleep(10)
    brown.quit()
    with open('json.txt','w') as f:
        json.dump(cookies,f)

def get_cookies():
    cookiesdata={}
    with open('\zhihudata\zhihudata\commer\json.txt','r') as d:
        cookies=json.load(d)
    for cookiess in cookies:
        name=cookiess['name']
        value=cookiess['value']
        cookiesdata.setdefault(name,value)
    print(cookiesdata)

import hashlib
def md5_import():
    url='http://www.zhihu.com'
    if isinstance(url,str):
        url=url.encode('utf-8')
        m=hashlib.md5()
        m.update(url)
        print(m.hexdigest())
md5_import()