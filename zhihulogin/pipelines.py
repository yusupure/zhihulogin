# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymysql.cursors
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi
import json
from PIL import Image
import codecs
import os
import requests
from zhihulogin import items


class ZhihuloginPipeline(object):
    def process_item(self, item, spider):
        return item

class twmysqlinsertPipline(object):
    def __init__(self,dbpool):
        self.dbpool=dbpool
    @classmethod
    def from_settings(cls,settings):
        dbpool=adbapi.ConnectionPool(
        "pymysql",
        host=settings['MYSQL_HOST'],
        port=settings['MYSQL_PORT'],
        db=settings['MYSQL_DBNAME'],
        user=settings['MYSQL_USER'],
        password=settings['MYSQL_PASSWORD'],
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
        )
        return cls(dbpool)

    def process_item(self, item, spider):
        query=self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item)
    def handle_error(self,failure,item):
        print(failure)
    def do_insert(self,cursor,item):
        insert_to,parmes=item.get_insert_sql()
        cursor.execute(insert_to,parmes)

class NewjsondownloadPipline(object):
    def __init__(self):
        self.file=codecs.open('json.txt','w',encoding='utf-8')

    def process_item(self, item, spider):
        jsonlist=json.dumps(dict(item),ensure_ascii=False)
        self.file.write(jsonlist)
        return item
    def close_json(self):
        self.file.close()

class NkjsondownloadPipline(object):
    def __init__(self):
        self.file=open('json2.text','wb')
        self.jsonload=JsonItemExporter(self.file,ensure_ascii=False,encoding='utf-8')
        self.jsonload.start_exporting()
    def close_json(self):
        self.jsonload.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.jsonload.export_item(item)
        return item


class NkimagedwomPipline(object):
    def process_item(self, item, spider):
        filelist='{}\{}.{}'.format(os.getcwd(),item['url'],'jpg')
        file=open(filelist,'wb')
        response=requests.get(item['url'])
        file.write(response.content)
        file.close()


class NewimagePipline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok,value in results:
            image_path=value['path']
            item['xxx']=image_path
        return item