# -*- coding: utf-8 -*-


class Site(object):
    name = None
    short_name = None
    title = None
    url = None
    bbs = None

    def __init__(self, name, short_name, title, bbs):
        self.name = name
        self.short_name = short_name
        self.title = title
        self.bbs = bbs

    def to_dict(self):
        return {
            "name": self.name,
            "short_name": self.short_name,
            "title": self.title,
            "url": self.url,
            "bbs": self.bbs,
        }


SITE_YAML = "../../data/site.yaml"
SITES = [
    Site("ロマサガRS", "sagars", "ロマサガRS", "スマホゲーム")
]
