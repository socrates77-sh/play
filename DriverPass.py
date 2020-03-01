import re
from mitmproxy import ctx
import logging


log_file = r'f:\download\log\chrome.log'

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
fh = logging.FileHandler(log_file, mode='w')
fh.setLevel(logging.WARNING)
# formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
# fh.setFormatter(formatter)
logger.addHandler(fh)


def response(flow):
    # print(flow.request.url)
    # if 'dist/captcha' in flow.request.url:
    #     for webdriver_key in ['webdriver', '__driver_evaluate', '__webdriver_evaluate', '__selenium_evaluate',
    #                           '__fxdriver_evaluate', '__driver_unwrapped', '__webdriver_unwrapped', '__selenium_unwrapped',
    #                           '__fxdriver_unwrapped', '_Selenium_IDE_Recorder', '_selenium', 'calledSelenium',
    #                           '_WEBDRIVER_ELEM_CACHE', 'ChromeDriverw', 'driver-evaluate', 'webdriver-evaluate',
    #                           'selenium-evaluate', 'webdriverCommand', 'webdriver-evaluate-response', '__webdriverFunc',
    #                           '__webdriver_script_fn', '__$webdriverAsyncExecutor', '__lastWatirAlert',
    #                           '__lastWatirConfirm', '__lastWatirPrompt', '$chrome_asyncScriptInfo',
    #                           '$cdc_asdjflasutopfhvcZLmcfl_']:
    #         ctx.log.info('Remove "{}" from {}.'.format(
    #             webdriver_key, flow.request.url))
    #     # flow.response.text = flow.response.text.replace(
    #     #     '"{}"'.format(webdriver_key), '"NO-SUCH-ATTR"')
    #     print(flow.response.text)

    # flow.response.text = flow.response.text.replace('t.webdriver', 'false')
    # flow.response.text = flow.response.text.replace('navigator.webdriver', 'false')
    # flow.response.text = flow.response.text.replace('ChromeDriver', '')

    # if '/user/96454134877' in flow.request.url:
    #     print(flow.request.url)
        # flow.response.text = flow.response.text.replace('success', 'error')

    # toutiao_pc-pc-fe_switch
    #     # print(flow.request.url)
    #     logger.warning(flow.request.url)
    global fh
    # url_like ='www.toutiao.com/api/pc/feed/'
    if ('www.toutiao.com/api/pc/feed/' in flow.request.url) or ('www.toutiao.com/c/user/article' in flow.request.url):
        # logger.warning(flow.request.url)
        logger.warning(flow.response.text)
        # logger.warning('='*70)
        # logger.warning('url')
        # logger.warning(flow.request.url)
        # logger.warning('-'*70)
        # logger.warning('request')
        # logger.warning(flow.request.text)
        # logger.warning('-'*70)
        # logger.warning('response')
        # logger.warning(flow.response.text)

    # logger.warning(flow.request.url)


# https://www.toutiao.com/c/user/96454134877/#mid=1596815857982478
# chrome --proxy-server=127.0.0.1:8080 --ignore-certificate-errors
