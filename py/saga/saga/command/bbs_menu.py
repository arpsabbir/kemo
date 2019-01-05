# -*- coding: utf-8 -*-
from flask_script import Command
import requests
from logging import getLogger
logger = getLogger(__name__)


class BBSMenu(Command):
    """
    sync BBS Menu
    """

    def run(self):
        logger.info("start")
        self._main()

    def _main(self):
        url = 'https://menu.5ch.net/bbsmenu.html'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding  # shift-jis判定してutf8に変更
        logger.info("url: {}".format(url))
        if not response.ok:
            logger.error("fail return http status is invalid")
            exit(1)
        logger.info("size: {}byte".format(len(response.text)))
        print(response.text)
