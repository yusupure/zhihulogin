# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json

from scrapy.loader import ItemLoader

from zhihudata.items import ZhihudataItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com:']
    start_urls = ['http://www.zhihu.com/']


    # url_token=''
    # user_url=''
    # url_parer=''
    #
    # folwees_url=''
    # folowees_parer=''
    #
    # folwers_url=''
    # folowers_parer=''
    #
    # def start_requests(self):
    #     yield  Request(self.url,callback=self.url_nr)
    #     yield Request(self.folwees_url, callback=self.folwees_nr)
    #     yield Request(self.folwers_url, callback=self.folwers_nr)
    #
    # def url_nr(self,response):
    #     data=response.text
    #     userdata=json.loads(data)
    #     url=userdata['data']
    #     id=userdata['id']
    #     items=ItemLoader(item=ZhihudataItem(),response=response)
    #     items.add_value('url',url)
    #     items.add_value('id',id)
    #     item=items.load_item()
    #     yield item
    #     yield Request()
    # def folwees_nr(self,response):
    #     data = response.text
    #     userdata = json.loads(data)
    #     if 'data' in userdata.keys():
    #         url_token=''
    #         yield Request(self.url(),callback=self.url_nr)
    #     if 'paging' in userdata.keys and userdata.get('paging').get('is_end')==False:
    #         next_page=userdata['paging']['next']
    #         yield Request(self.folwees_url(),callback=self.folwees_nr)
    #
    # def folwers_nr(self,response):
    #     pass
    def parse(self, response):

