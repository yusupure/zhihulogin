# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuloginItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    id=scrapy.Field()
    url=scrapy.Field()
    pl=scrapy.Field()
    hds=scrapy.Field()

    def get_insert_sql(self):
        insert_to='''
            insert into zhihulogin(id,title,url,pl,hds)VALUES(%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE pl=values(pl),hds=values(hds)
            
        '''
        id=self['id'][0]
        title=''.join(self['title'][0])
        url=self['url'][0]
        pl=self['pl'][0]
        hds=self['hds'][0]

        parmes=(id,title,url,pl,hds)
        return insert_to,parmes