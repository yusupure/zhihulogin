import hashlib
url='http://www.zhihu.com'

def md5_dd(url):
    if isinstance(url,str):
        url=url.encode('utf8')
        im=hashlib.md5()
        im.update(url)
        print(im.hexdigest())

md5_dd(url)