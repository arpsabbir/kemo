# -*- coding: utf-8 -*-
from logging import getLogger
import requests
logger = getLogger(getLogger.__str__())


def http_get(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding  # shift-jis判定してutf8に変更
    logger.info("url: {}".format(url))
    logger.info("size: {}byte".format(len(response.text)))
    logger.info("status: {}".format(response.status_code))
    return response
