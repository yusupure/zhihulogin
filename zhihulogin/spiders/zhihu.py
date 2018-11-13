# -*- coding: utf-8 -*-
import scrapy
import json
from PIL import Image
from scrapy.loader import ItemLoader
from selenium import webdriver
import requests
from time import sleep
import re
import base64

from zhihulogin.items import ZhihuloginItem

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    url='https://www.zhihu.com/api/v3/feed/topstory/recommend?session_token=49ecf380ded1f3f798ad93e71abfc9b8&desktop=true&limit=7&action=down&after_id=5'
    def get_zhihucookies(self):
        brower=webdriver.Chrome()
        session=requests.session()
        session.headers.clear()
        brower.get(self.start_urls[0])
        brower.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[2]/span').click()
        brower.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[1]/div[2]/div[1]/input').send_keys("13560414027")
        brower.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[2]/div/div[1]/input').send_keys("abc.12345")
        sleep(5)
        try:
            img=brower.find_element_by_css_selector('.Captcha-chineseContainer img')
            sleep(5)
        except:
            img=brower.find_element_by_css_selector('.Captcha-englishContainer img').get_attribute("src")
            sleep(5)
            data=re.findall(r'base64,(.*)',img,re.S)[0]

            if data!='null':
                with open('yzm.jpg','wb')as f:
                    f.write(base64.b64decode(data))
                    f.close()
                try:
                    im=Image.open('/zhihulogin/zhihulogin/yzm.jpg','r')
                    im.show()
                    im.close()
                except:
                    pass
                yzm=input('输入验证码')
                sleep(10)
                brower.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[3]/div/div/div[1]/input').send_keys(yzm)
        else:
            pass
        brower.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/button').click()
        sleep(10)
        #等待加载COOKIES
        cookies=brower.get_cookies()
        cookieslist={}
        brower.quit()
        with open('zhihucookies.txt','w') as fb:
            json.dump(cookies,fb)
            fb.close()
        for cookiesnew in cookies:
            name=cookiesnew['name']
            value=cookiesnew['value']
            cookieslist.setdefault(name,value)
        #print(cookieslist)
        return cookieslist

    def cookies_file(self):
        cookieslist = {}
        with open('/zhihulogin/zhihulogin/zhihucookies.txt','r') as f:
            coookies=json.load(f)
            f.close()
        for cookiesnew in coookies:
            name=cookiesnew['name']
            value=cookiesnew['value']
            cookieslist.setdefault(name,value)
        return (cookieslist)



    def start_requests(self):
        yield scrapy.Request(url=self.url,cookies=self.cookies_file(),callback=self.parse)
        #self.get_zhihucookies()
        #self.cookies_file()
    def parse(self, response):
        html=response.text
        url_id=json.loads(html)
        if 'data' in url_id.keys():
            for url_id_list in url_id['data']:
                try:
                    id=url_id_list['target']['question']['id']
                    url='https://www.zhihu.com/question/{}'.format(id)
                    yield scrapy.Request(url=url,cookies=self.cookies_file(),meta={'id':id,'url':url},callback=self.parse_delte)
                except:
                    pass
        # if 'paging' in url_id.keys() and url_id['paging']['is_end']==False:
        #     next=url_id['paging']['next']
        #     yield scrapy.Request(url=next,headers=self.headers,cookies=self.cookies_file(),callback=self.parse)

    def parse_delte(self,response):
        id=response.meta.get('id')
        url=response.meta.get('url')
        itemloader=ItemLoader(item=ZhihuloginItem(),response=response)
        itemloader.add_css('title','.QuestionHeader-main  h1::text')
        itemloader.add_value('id',id)
        itemloader.add_value('url',url)
        itemloader.add_css('pl','.QuestionHeader-Comment button::text')
        itemloader.add_css('hds','.List-headerText span::text')
        item=itemloader.load_item()
        yield item