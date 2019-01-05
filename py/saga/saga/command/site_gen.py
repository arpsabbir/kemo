# -*- coding: utf-8 -*-
from flask_script import Command
from logging import getLogger
from saga.utils import http_get
from saga import constants
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
        site = sites[0] # TODO 暫定
        url = "{}subject.txt".format(site["url"])
        response = http_get(url)
        if not response.ok:
            exit(1)
        

