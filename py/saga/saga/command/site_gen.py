# -*- coding: utf-8 -*-
from flask_script import Command
from logging import getLogger
from saga import constants
from saga.module.scraping.search import SearchManager
import codecs
import yaml
import re
logger = getLogger(getLogger.__str__())


class SiteGen(Command):
    """
    generate site
    """

    def run(self):
        logger.info("start")
        self._main()

    def _main(self):
        # subjects.txtとる
        sm = SearchManager(constants.SITES[0])
        sm.search_and_scraping()
