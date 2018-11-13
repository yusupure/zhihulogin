import requests
from scrapy.selector import Selector
import pymysql
conn=pymysql.connect(host='127.0.0.1',port=3339,db='test',user='root',password='root')
cursor=conn.cursor()
class Proxy_ip():
    def get_ip(self):
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        response=requests.get('http://www.xicidaili.com/nn/',headers=headers)
        selector=Selector(text=response.text)
        proxy_ip_list=[]
        all_urls=selector.css('#ip_list tr')
        for url_list in all_urls[1:]:
            ip=url_list.css('td::text').extract()[0]
            port = url_list.css('td::text').extract()[1]
            speed_list = url_list.css('.country div::attr(title)').extract()[0]
            if speed_list:
                speed=float(speed_list.split('秒')[0])
            proxy_ip_list.append((ip,port,speed))
        for datalist in proxy_ip_list:
            insert_sql='''
                insert into proxy_list(ip,port,speed)values('{0}','{1}',{2})
            '''.format(datalist[0],datalist[1],datalist[2])
            try:
                cursor.execute(insert_sql)
                conn.commit()
            except Exception as e:
                pass

    def delete_ip(self,ip):
        delete_sql='''
            delete from proxy_list where ip='{}'
        '''.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def load_ip(self):
        load_sql='''
            select ip,port from proxy_list order by Rand() limit 1
        '''
        cursor.execute(load_sql)
        for ip_list in cursor.fetchall():
            ip=str(ip_list[0])
            port=str(ip_list[1])
            just_ip=self.test_ip(ip,port)
            if just_ip:
                return "http://{0}:{1}".format(ip,port)
            else:
                return self.load_ip()

    def test_ip(self,ip,port):
        httplist='http://{0}:{1}'.format(ip,port)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        try:
            proxy_dict = {'http': httplist}
            response=requests.get('http://www.baidu.com',headers=headers,proxies=proxy_dict,timeout=5)
        except Exception as e:
            print('地址失败1')
            self.delete_ip(ip)
            return False
        else:
            code=response.status_code
            if code>=200 and code<300:
                return True
            else:
                print('访问失败')
                self.delete_ip(ip)
                return False


get_ip=Proxy_ip()
get_ip.load_ip()