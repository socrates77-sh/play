import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

WAIT_RESPONSE = 3

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome()

driver.get('https://www.toutiao.com/c/user/107952533857/#mid=1628218742667278')
time.sleep(WAIT_RESPONSE)
# print(driver.find_element_by_id("wrapper"))
print(driver.title)

# driver.save_screenshot("a.png")

# data = driver.find_element_by_id("wrapper")
# print(data)

# content = driver.find_element_by_xpath('"//ul/li/div[@ga_event=article_item_click]"')
# print(content.text)

html_text = driver.page_source
# print(html_text)

element = driver.find_element_by_tag_name('body')


p = re.compile(
    '<a class=\"link title\" target=\"_blank\" href=\"/item/(.*?)/\">(.*?)</a>.*?<span class=\"lbtn\">.*?(\d{4}.*?)</span>', re.M)
result = re.findall(p, html_text)

# print(result)
for r in result:
    # print(r[0], r[1])
    print(r)

print(len(result))

# i = 1
# js = 'var q=document.documentElement.scrollTop=' + str(500 * i)
# for i in range(1, 6):
#     js = 'window.scrollTo(0, document.body.scrollHeight)'
#     js = 'js = "var q=document.body.scrollTop=10000"'
#     driver.execute_script(js)
#     print('=====================================')
#     time.sleep(3)

print('key down')
element.send_keys(Keys.END)
time.sleep(10)
print("====================")


html_text = driver.page_source
# print(html_text)

result = re.findall(p, html_text)

# print(result)
for r in result:
    # print(r[0], r[1])
    print(r)

print(len(result))

#
# # 逐渐滚动浏览器窗口，令ajax逐渐加载
# for i in range(1, 10):
#     js = "var q=document.body.scrollTop=" + str(500 * i)  # PhantomJS
#     js = "var q=document.documentElement.scrollTop=" + \
#         str(500 * i)  # 谷歌 和 火狐

#     driver.execute_script(js)
#     print('=====================================')
#     time.sleep(3)

#     # 拿到页面源码
#     html = etree.HTML(driver.page_source)
#     all_img_list = []

#     # 得到所有图片
#     img_group_list = html.xpath("//img[contains(@id,'J_pic')]")
#     # img_group_list = html.xpath("//img[starts-with(@id,'J_pic')]")
#     # 正则表达式匹配
#     # img_group_list = html.xpath(r'//img[re:match(@id, "J_pic*")]',namespaces={"re": "http://exslt.org/regular-expressions"})

#     # 收集所有图片链接到列表
#     for img_group in img_group_list:
#         img_of_group = img_group.xpath(
#             ".//@data-original | .//@data-img-back | .//@data-img-side")
#         print(img_of_group)
#         all_img_list.append('\n'.join(img_of_group) + '\n')

#     # 将收集到的数据写入文件
#     with open('vip.txt', 'w', encoding='utf-8') as f:
#         f.write('\n'.join(all_img_list))

#     # 退出浏览器
driver.close()
