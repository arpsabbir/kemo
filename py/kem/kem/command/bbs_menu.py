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
        logger.error("start")
        self._main()

    def _main(self):
        url = 'https://menu.5ch.net/bbsmenu.html'
        response = requests.get(url)
        if response.ok:
            logger.info("hoge")
        else:
            logger.info("hoge2")

        logger.info("hoge3")