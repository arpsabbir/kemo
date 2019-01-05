# -*- coding: utf-8 -*-
from flask_script import Command
from logging import getLogger
from saga.utils import http_get
logger = getLogger(__name__)


class BBSMenu(Command):
    """
    sync BBS Menu
    """

    def run(self):
        logger.info("start")
        self._main()

    def _main(self):
        # http get
        url = 'https://menu.5ch.net/bbsmenu.html'
        response = http_get(url)
        if not response.ok:
            exit(1)
        # print(response.text)

        # parse html
