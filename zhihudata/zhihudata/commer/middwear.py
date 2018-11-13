from fake_useragent import UserAgent


class randomuseragentmiddewear(object):
    def __init__(self,crawler):
        super(randomuseragentmiddewear, self).__init__()
        self.ua=UserAgent()
        self.ua_type=crawler.settings.get('RANDOM_AGENT_TYPE','random')
    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua,self.ua_type)
        request.headers.setdefault(self.ua,get_ua())
