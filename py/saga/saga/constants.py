# -*- coding: utf-8 -*-
import codecs
import yaml


class Site(object):
    name = None
    short_name = None
    title = None
    url = None
    bbs = None

    def __init__(self, o):
        self.bbs = o['bbs']  # e.g. スマホゲーム
        self.name = o['name']  # e.g. gamesm
        self.short_name = o['short_name']  # e.g. ロマサガRS
        self.title = o['title']  # e.g. sagars
        self.base_url = o['base_url']  # e.g. http://krsw.5ch.net

    @property
    def url(self):
        return self.base_url + "/" + self.name

    @property
    def subject_url(self):
        return self.url + "/subject.txt"

    # https://egg.5ch.net/test/read.cgi/game/1555935306/
    def dat_url(self, dat):
        return self.base_url + "/test/read.cgi/" + self.name + "/" + str(dat) + "/"


GEN_RES_MIN = 600

SITE_YAML = "../../data/site.yaml"
with codecs.open(SITE_YAML, "r", 'utf-8') as f:
    sites = yaml.load(f)
SITES = [Site(yaml_site) for yaml_site in sites]
