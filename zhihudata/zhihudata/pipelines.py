# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import requests
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi
class ZhihudataPipeline(object):
    def process_item(self, item, spider):
        return item

class NewjsondownPipeline(object):
    def __init__(self):
        self.file=codecs.open('json1.txt','w',encoding='utf-8')

    def process_item(self, item, spider):
        jsonlist=json.dumps(dict(item),ensure_ascii=False)
        self.file.write(jsonlist)
        return item
    def json_close(self):
        self.file.close()


class NkJsondownPipeline(object):
    def __init__(self):
        self.file=open('json2.txt','wb')
        self.exp=JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        self.exp.start_exporting()
    def closejson(self):
        self.exp.finish_exporting()
        self.file.close()
    def process_item(self, item, spider):
        self.exp.export_item(item)
        return item

class NewimagedownPipeling(object):
    def process_item(self, item, spider):
        image_html=requests.get(item['url'])
        image_file='{}\{}.{}'.format(item['url'],item['id'],'jpg')
        with open(image_file,'wb') as fb:
            fb.write(image_html.content)
            fb.close()
        return item

class NkimagedownPipleing(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok,value in results:
            images_path=value['path']
            item['image_path']=images_path
            return item

class NkmysqldowmPipleing(object):
    def __init__(self,dbpool):
        self.dbpool=dbpool
    @classmethod
    def from_setting(cls,settings):
        dbpool=adbapi.ConnectionPool(
            "pymysql",
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            )
        return cls(dbpool)

    def process_item(self, item, spider):
        query=self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item)
    def handle_error(self,failure,item):
        print(failure)
    def do_insert(self,cursor,item):
        insert_sql='''
            insert into xxx(id,url)values (%s,%s)
        '''
        parmer=(item['id'],item['url'])
        cursor.execute(insert_sql,parmer)


class NewmysqlinsertPipline(object):
    def __init__(self):
        self.db=pymysql.connect(host='',port='',db='',user='',password='')
        self.cur=self.db.cursor(pymysql.cursors.DictCursor)

    def process_item(self, item, spider):
        insert_sql = '''
                    insert into xxx(id,url)values (%s,%s)
                '''
        parmer = (item['id'], item['url'])
        try:
            self.cur.execute(insert_sql,parmer)
            self.db.commit()
        except:
            self.db.rollback()