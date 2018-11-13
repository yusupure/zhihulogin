import requests
from scrapy.selector import Selector
import pymysql
conn=pymysql.connect(host='127.0.0.1',port=3339,db='test',user='root',password='root')
cursor=conn.cursor()
# class crawl_ips():
#     iplist=[]
#     headers={
#         'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
#     }
#     for i in range(1500):
#         re=requests.get('http://www.xicidaili.com/nn/{}'.format(i),headers=headers)
#         selector=Selector(text=re.text)
#         all_trs=selector.css("#ip_list tr")
#         for tr in all_trs[1:]:
#             speed_str=tr.css(".bar::attr(title)").extract()[0]
#             if speed_str:
#                 speed = float(speed_str.split("秒")[0])
#
#             all_texts=tr.css('td::text').extract()
#             ip=all_texts[0]
#             port=all_texts[1]
#             proxy_type=all_texts[4]
#             iplist.append((ip,port,speed,proxy_type))
#
#         for insert_sql in iplist:
#             #print(insert_sql[0])
#             insert_sqla=('''insert proxy_ip(id,port,speed,proxy_type) values(%s,%s,%s,%s)''')
#             parmer=(insert_sql[0],insert_sql[1],insert_sql[2],insert_sql[3])
#             cursor.execute(insert_sqla,parmer)
#             conn.commit()


class Get_ip(object):
    def delete_ip(self,ip):
        delete_slq='''
            delete from proxy_ip where ip='{0}'
        '''.format(ip)
        cursor.execute(delete_slq)
        conn.commit()
        return True

    def judge_ip(self,ip,port):
        #判断IP是否可用
        http_url='https://www.baidu.com'
        proxy_url="http://{0}:{1}".format(ip,port)
        try:
            proxy_dict={"http":proxy_url,"https":proxy_url}
            response=requests.get(http_url,proxies=proxy_dict)
        except Exception as e:
            print('异常')
            self.delete_ip(ip)
            return False
        else:
            code=response.status_code
            print(proxy_url)
            if code>=200 and code<300:
                print('ok')
                return True
            else:
                print('cuowu')
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        #冲数据中获取一个IP
        sql="select ip,port from proxy_ip order by RAND() limit 1"
        result=cursor.execute(sql)
        for ip_info in cursor.fetchall():
            ip=str(ip_info[0])
            port=str(ip_info[1])
            judge_re=self.judge_ip(ip,port)
            if judge_re:
                return "http://{0}:{1}".format(ip,port)
            else:
                return self.get_random_ip()
if __name__=="__main__":
    get_ip=Get_ip()
    get_ip.get_random_ip()