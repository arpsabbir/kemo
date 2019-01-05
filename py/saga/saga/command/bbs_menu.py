# -*- coding: utf-8 -*-
from flask_script import Command
from logging import getLogger
from saga.utils import http_get
from saga import constants
import codecs
import yaml
import re
logger = getLogger(getLogger.__str__())


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

        # parse html
        pattern = r'<A HREF=(.+?)>(.+?)</A>'
        matched_list = re.findall(pattern, response.text)
        logger.info("matched_list count:{}".format(len(matched_list)))  # => ('http://medaka.5ch.net/boxing/', 'ボクシング')
        h = {o[1]: o[0] for o in matched_list}
        sites = []
        for site in constants.SITES:
            site.url = h[site.bbs]
            sites.append(site.to_dict())

        # output yaml
        path = "../../data/site.yaml"
        with codecs.open(path, "w", 'utf-8') as f:
            yaml.dump(sites, f, encoding='utf-8', allow_unicode=True, default_flow_style=False)
