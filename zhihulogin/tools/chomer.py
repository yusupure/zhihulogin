from selenium import webdriver
#不加载图片
chrome_opt=webdriver.ChromeOptions()
prefs={"profile.managed_default_content_settings.images":2}
chrome_opt.add_experimental_option("prefs",prefs)
brow=webdriver.Chrome(chrome_options=chrome_opt)
brow.get('http://www.taobao.com')
print(brow.page_source)