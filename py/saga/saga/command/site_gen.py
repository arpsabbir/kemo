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
        # load yaml
        with codecs.open(constants.SITE_YAML, "r", 'utf-8') as f:
            sites = yaml.load(f)

        # subjects.txtとる
        sm = SearchManager(sites[0])
        sm.search_and_scraping()
