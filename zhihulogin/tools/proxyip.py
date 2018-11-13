import requests
from scrapy.selector import Selector
import pymysql
conn=pymysql.connect(host='',port='',db='',user='',password='')
cursor=conn.cursor()
class Proxy_ip():
    #提取代理ip
    def get_ip(self):
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        user_agent_list=[]
        for i in range(1000):
            response=requests.get('https://www.kuaidaili.com/free/inha/{}/'.format(i),headers=headers)
            selector=Selector(text=response.text)
            all_useragent=selector.css('.table-bordered tbody tr')
            for all_agent_list in all_useragent:
                ip=all_agent_list.css('td::text').extract()[0]
                port = all_agent_list.css('td::text').extract()[1]
                niming= all_agent_list.css('td::text').extract()[2]
                htp = all_agent_list.css('td::text').extract()[3]
                speed_list = all_agent_list.css('td::text').extract()[5]
                if speed_list:
                    speed=float(speed_list.replace('秒',''))
                user_agent_list.append((ip,port,niming,htp,speed))
            for list_agent in user_agent_list:
                insert_sql='''
                        insert into proxyiplist(ip,port,niming,htp,speed)values(%s,%s,%s,%s,%s)
                '''
                parmer=(list_agent[0],list_agent[1],list_agent[2],list_agent[3],list_agent[4])
                try:
                    cursor.execute(insert_sql,parmer)
                    conn.commit()
                except:
                    pass

    def delete_ip(self,ip):
        delete_ip='''
            delete from proxyiplist where ip='{}'
        '''.format(ip)
        cursor.execute(delete_ip)
        conn.commit()
        return True

    def test_ip(self,ip,port):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        url='http://www.baidu.com'
        iplist="http://{0}:{1}".format(ip,port)
        try:
            proxy_dict = {"http": iplist, }
            reponse = requests.get(url, headers=headers,proxies=proxy_dict,timeout=3)
        except Exception as e:
            print('无法使用1')
            self.delete_ip(ip)
            return False
        else:
            code=reponse.status_code
            if code>=200 and code<300:
                return True
            else:
                print('无法使用2')
                self.delete_ip(ip)
                return False

    def load_ip(self):
        select_sql='''
            select ip,port from proxyiplist order by rand() limit 1
        '''
        cursor.execute(select_sql)
        for ipdata in cursor.fetchall():
            ip=str(ipdata[0])
            port=str(ipdata[1])
            just_ip=self.test_ip(ip,port)
            if just_ip:
                return "http://{0}:{1}".format(ip,port)
            else:
                return self.load_ip()


if __name__=='__main__':
    get_op=Proxy_ip()
    #get_op.get_ip()
    get_op.load_ip()