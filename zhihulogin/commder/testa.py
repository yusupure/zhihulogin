
from selenium import webdriver
import requests
import base64
import re
from time import sleep
from PIL import Image
import json
def get_zhuhu():
    brow=webdriver.Chrome()
    session=requests.session()
    session.headers.clear()
    brow.get('https://www.zhihu.com')
    brow.find_element_by_xpath('').click()#登录
    brow.find_element_by_xpath('').send_keys('1356014027')
    brow.find_element_by_xpath('').send_keys('abc.12345')
    try:
        img=''
    except:
        img=brow.find_element_by_xpath('').get_attribute('src')
        sleep(10)
        basenum=re.findall(r'base64(.*)',img,re.S)
        if basenum!='null':
            with open('yzm.jpg','wb') as fb:
                fb.write(base64.b64decode(basenum))
                fb.close()
            try:
                im=Image.open('yzm.jpg','r')
                im.show()
                im.close()
            except:
                pass
    else:
        pass
    brow.find_element_by_xpath('').click()
    sleep(5)
    codenum=input('输入验证码')
    brow.find_element_by_xpath('').send_keys(codenum)
    cookies=brow.get_cookies()
    sleep(10)
    brow.quit()
    with open('json1.txt','w') as f:
        json.dump(cookies,f)
