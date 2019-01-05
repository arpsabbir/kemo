# -*- coding: utf-8 -*-
from saga.utils import http_get
from logging import getLogger
import re
from saga import constants
logger = getLogger(getLogger.__str__())


ignore_base = [
    '晒',
    '叩',
    'フレンド',
    '協力',
    '交換',
    '終わった',
    '募集',
    '垢',
    '乞食',
    '葬式',
]


class Subject(object):
    dat = None
    title = None
    ct = None

    def __init__(self, dat, title, ct):
        self.dat = int(dat)
        self.title = title
        self.ct = int(ct)

    def execute_matome(self, force=None):
        logger.info("start exec matome: {}({})".format(self.title, str(self.ct)))


class SearchManager(object):
    """
    スレッドを検索する
    """

    def __init__(self, site):
        self.site = site

    def search_and_scraping(self, force=None):
        site = self.site

        # スレッド検索
        url = "{}subject.txt".format(site['url'])
        subjects = self.get_from_url(url)
        method = getattr(self, site['title'])
        subjects_dict = method(subjects, site)

        # スクレイピング
        logger.info("---- start execute_matome")
        for key in subjects_dict:
            sub = subjects_dict[key]
            sub.execute_matome(force=force)

        # 参照を切る
        method = None
        del method
        return subjects_dict

    def get_from_url(self, url):
        """
        urlをrequestsしてパースして返す
        :param url: str
        :return: subjects: list[Subject]
        """
        response = http_get(url)
        if not response.ok:
            exit(1)

        # parse html
        pattern = r'(.+?)\.dat<>(.+?) \t \((.+?)\)'
        matched_list = re.findall(pattern, response.text)  # => ('1543745327', '【ドラガリ】ドラガリアロストPart689', '12')
        logger.info("matched_list count:{}".format(len(matched_list)))
        return [Subject(o[0], o[1], o[2]) for o in matched_list if int(o[2]) > constants.GEN_RES_MIN]

    def sagars(self, subjects, site):
        """
        ロマサガ
        :param subjects: list[Subject]
        :param site: dict{id: Subject}
        """
        keywords = [
            'ロマサガRS',
            'ロマンシングサガ',
            'リ・ユニバース',
        ]
        keywords_ignore = ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def phantom(self, subjects, site):
        """
        ファンキル
        :param subjects: list[Subject]
        :param site: dict{id: Subject}
        """
        keywords = [
            'ファンキル',
            'オブキル',
            'ファントムオブキル',
        ]
        keywords_ignore = ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def fallout4(self, subjects, site):
        """
        ファンキル
        :param subjects: list[Subject]
        :param site: dict{id: Subject}
        """
        keywords = [
            'Fallout4',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def fallout4pc(self, *args, **kwargs):
        return self.fallout4(*args, **kwargs)

    def shironeko(self, subjects, site):
        """
        ファンキル
        :param subjects: list[Subject]
        :param site: dict{id: Subject}
        """
        keywords = [
            '白猫',
        ]
        keywords_ignore = [
            '糞猫',
            'テニス',
            '白テニ',
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def logres(self, subjects, site):
        """
        :param subjects: list[Subject]
        :param site: dict{id: Subject}
        """
        keywords = [
            'ログレス',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def pawaapp(self, subjects, site):
        """
        :param subjects: list[Subject]
        :param site: dict{id: Subject}
        """
        keywords = [
            'パワプロ',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def pd(self, subjects, site):
        """
        :param subjects: list[Subject]
        :param site: dict{id: Subject}
        """
        keywords = [
            'パズドラ',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def mstrike(self, subjects, site):
        """
        :param subjects: list[Subject]
        :param site: dict{id: Subject}
        """
        keywords = [
            'モンスト',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def destiny(self, subjects, site):
        """
        :param subjects: list[Subject]
        :param site: dict{id: Subject}
        """
        keywords = [
            'destiny',
            'Destiny',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def ffbe(self, subjects, site):
        """
        :param subjects: list[Subject]
        :param site: dict{id: Subject}
        """
        keywords = [
            'FFBE',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def tos(self, subjects, site):
        keywords = [
            'Savior',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def dq10(self, subjects, site):
        keywords = [
            'DQ10',
            'DQX',
            'ドラゴンクエストX',
            'ドラゴンクエスト10',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def fgo(self, subjects, site):
        keywords = [
            'Grand Order',
            'FateGO',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def splatoon(self, subjects, site):
        keywords = [
            'Splatoon',
            'スプラトゥーン',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def star(self, subjects, site):
        keywords = [
            '星の',
            'スプラトゥーン',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def ffrk(self, subjects, site):
        keywords = [
            'FFRK',
        ]
        keywords_ignore = [
            '動画配信',
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def sekaiju(self, subjects, site):
        keywords = [
            '世界樹',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def lol(self, subjects, site):
        keywords = [
            'LoL',
            'League of Legends',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def alchemy(self, subjects, site):
        keywords = [
            'タガタメ',
            '誰ガ為',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def darksouls3(self, subjects, site):
        keywords = [
            'ダークソウル3',
            'ダークソウル３',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def dqmj3(self, subjects, site):
        keywords = [
            'DQMJ3',
            'ドラゴンクエストモンスターズ ジョーカー3',
            'ドラゴンクエストモンスターズ ジョーカー３',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def clashroyal(self, subjects, site):
        """
        :param subjects:
        :param site:
        :return:
        """
        keywords = [
            'クラッシュ・ロワイヤル',
            'クラッシュ ロワイヤル',
            'クラッシュロワイヤル',
            'クラロワ',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def division(self, subjects, site):
        """
        :param subjects:
        :param site:
        :return:
        """
        keywords = [
            'The Division',
            'ディビジョン',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def seven(self, subjects, site):
        """
        :param subjects:
        :param site:
        :return:
        """
        keywords = [
            'セブンナイツ',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def overwatch(self, subjects, site):
        """
        :param subjects:
        :param site:
        :return:
        """
        keywords = [
            'Overwatch',
            'オーバーウォッチ',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def dp(self, subjects, site):
        """
        :param subjects:
        :param site:
        :return:
        """
        keywords = [
            'ドラプロ',
            'ドラゴンプロジェクト',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def hstone(self, subjects, site):
        """
        :param subjects:
        :param site:
        :return:
        """
        keywords = [
            'シャドバ',
            'シャドウバース',
            'Shadowverse',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)

    def poke(self, subjects, site):
        """
        :param subjects:
        :param site:
        :return:
        """
        keywords = [
            'ポケモンGO',
        ]
        keywords_ignore = [
        ]
        keywords_ignore += ignore_base
        return _base_search(subjects, site, keywords, keywords_ignore)


def _base_search(subjects, site, keywords, keywords_ignore):
    """
    :param subjects: list[Subject]
    :param site: Site
    :param keywords: list[str]
    :param keywords_ignore: list[str]
    :return: dict{id: Subject}
    """
    # 名前でフィルタ
    subjects_dict = {}
    for key in keywords:
        for subject in subjects:
            if key in subject.title:
                subjects_dict[subject.dat] = subject

    # 禁止名でフィルタ
    ignore_keys = []
    for key_subject in subjects_dict:
        _subject = subjects_dict[key_subject]
        _title = _subject.title
        for key_ignore in keywords_ignore:
            if key_ignore in _title:
                ignore_keys.append(key_subject)

    # 禁止名でフィルタの削除部分
    for key in ignore_keys:
        if key in subjects_dict:
            del subjects_dict[key]

    # 結果出力
    logger.info("---- search results")
    for key_subject in subjects_dict:
        logger.info(subjects_dict[key_subject].title)

    return subjects_dict
