from selenium import webdriver
from lxml import etree
from pyquery import PyQuery as pq
import time
from selenium.webdriver.chrome.options import Options
import re
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome()
# driver.maximize_window()
driver.get('https://www.toutiao.com/c/user/107952533857/#mid=1628218742667278')
time.sleep(3)
# driver.implicitly_wait(10)
# print(driver.find_element_by_link_text('科技').text)
# driver.find_element_by_link_text('科技').click()
# driver.implicitly_wait(10)

for i in range(100): #这里循环次数尽量大，保证加载到底
    webdriver.ActionChains(driver).key_down(Keys.END).perform()
    # ActionChains(driver).key_down(Keys.DOWN).perform() #相当于一直按着DOWN键
    print(f'已完成{i}次')
    time.sleep(3)

# webdriver.ActionChains(driver).key_down(Keys.END).perform()
# time.sleep(3)

# for x in range(6):
#     js="var q=document.documentElement.scrollTop="+str(x*10000)
#     driver.execute_script(js)
#     print(x)
#     time.sleep(5)

# time.sleep(5)
page = driver.page_source
print(page)

p = re.compile(
    r'<a class=\"link title\" target=\"_blank\" href=\"/item/(.*?)/\">(.*?)</a>.*?<span class=\"lbtn\">.*?(\d{4}.*?)</span>', re.M)

result = re.findall(p, page)

# print(result)
for r in result:
    # print(r[0], r[1])
    print(r)

print(len(result))

# doc = pq(page)
# doc = etree.HTML(str(doc))
# contents = doc.xpath('//div[@class="wcommonFeed"]/ul/li')
# print(contents)
# for x in contents:
#     /html/body/div/div[4]/div[2]/div[2]/div/div/div/ul/li[1]/div/div[1]/div/div[1]/a
#     title = x.xpath('div/div[1]/div/div[1]/a/text()')
#     if title:
#         title = title[0]
#         with open('toutiao.txt','a+',encoding='utf8')as f:
#             f.write(title+'\n')
#         print(title)
#     else:
#         pass