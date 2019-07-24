import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import re


def get_page_source():
    page_url = 'https://www.toutiao.com/c/user/4472462177744952/#mid=1634147228048398'

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(page_url)
    time.sleep(5)
    tab_xpath = '//div[@id="wrapper"]/div[2]/div[1]/ul/li[3]'
    elem = browser.find_element_by_xpath(xpath=tab_xpath)
    print(elem)
    elem.click()
    time.sleep(5)
    webdriver.ActionChains(browser).key_down(Keys.END).perform()
    time.sleep(5)

    html = browser.page_source
    browser.quit()
    print(html)


def pic_page_save():

    page_url = 'https://www.toutiao.com/i6714794529771225613/'
    page_url = 'https://www.toutiao.com/i6695606649538740747/'
    page_url = 'https://www.toutiao.com/i6660306403061662211/'
    # page_url = 'https://www.toutiao.com/a1639903073346564'

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(page_url)
    time.sleep(1)
    webdriver.ActionChains(self.__web_driver).key_down(Keys.END).perform()
    time.sleep(1)
    html_text = browser.page_source
    browser.quit()

    # html_text1 = html_text.replace('\u002F', '')
    print(html_text)
    # print(html_text.find('\u002F'))

    p = re.compile('(http://p.+?pstatp.com/large/pgc-image/.+?)&quot', re.S)
    p = re.compile('(http://p.+?pstatp.com/large/pgc-image/.+?)"', re.S)
    p = re.compile(
        'url_list....{."url.":."http:\\\\.+?(p.+?pstatp.com)\\\\.+?origin\\\\.+?pgc-image\\\\.......(.+?)"', re.S)
    result = re.findall(p, html_text)
    pic_urls = []
    for (p, id) in result:
        url = 'http://%s/origin/pgc-image/%s' % (p, id)
        pic_urls.append(url)

    print(result)
    print(len(result))

    url = pic_urls[0]
    pic_url = url.replace('\\', '')
    print(pic_url)
    res = requests.get(pic_url, timeout=60)
    sz = open('a.jpg', 'wb').write(res.content)


def main():
    # pic_page_save()
    get_page_source()


if __name__ == '__main__':
    main()
