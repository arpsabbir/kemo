# -*- coding: utf-8 -*-
from saga.utils import http_get
from logging import getLogger
import re
from bs4 import BeautifulSoup
from saga import constants
from saga.utils import InspectionWord
import nltk

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


class SubjectRaw(object):
    def __init__(self, rank, refer, raws):
        """
        :param rank: string
        :param refer: list[string]
        :param raws: list[string] split text by line code
        """
        assert isinstance(rank, int)
        if len(refer) > 0:
            assert isinstance(refer[0], int)
        if len(raws) > 0:
            assert isinstance(raws[0], str)
        self.rank = rank
        self.refer = refer
        self.raws = raws


class Subject(object):
    dat = None
    title = None
    ct = None

    def __init__(self, site, dat, title, ct):
        self.site = site
        self.dat = int(dat)
        self.title = title
        self.ct = int(ct)

    def execute_matome(self, force=None):
        logger.info("start exec matome: {}({})".format(self.title, str(self.ct)))
        logger.info("url: {}, site: {}".format(self.url, self.site))

        # TODO: まとめ実装

        # url 生成
        response = http_get(self.url)
        if not response.ok:
            exit(1)
        # logger.info(response.text)

        # 正規表現で投稿ごとにパースする
        pattern = r'<div(.+?)data-userid(.+?)>(.+?)<\/span><\/div><\/div><br>'
        matched_list = re.findall(pattern, response.text)  # => ('1543745327', '【ドラガリ】ドラガリアロストPart689', '12')
        logger.info("res count:{}".format(len(matched_list)))

        # 投稿をSubjectRawにと投入する
        posts = []
        for r in matched_list:
            soup = BeautifulSoup(r[2], 'lxml')

            # [[1,2,3],[4,5,6], [7], [8,9]] をsumで畳み込んで Rubyのflattenを実現している[1,2,3,4,5,6,7,8,9]
            refer = sum([_normalizationa(a.text) for a in soup.find_all("a", attrs={"class": "reply_link"})], [])
            rank = int(soup.find("span", attrs={"class": "number"}).text)
            raws = soup.find("div", attrs={"class": "message"}).text.split()

            # NGワードを含んでいる場合は登録スキップ
            include_ng_word = False
            for line in raws:
                if InspectionWord.inspection(line):
                    include_ng_word = True
                    break

            if not include_ng_word:
                posts.append(SubjectRaw(rank, refer, raws))

        # 全体を俯瞰してキーワード抽出する
        logger.info("--")
        keywords = select_keyword(sum([post.raws for post in posts], []))
        for word in keywords:
            logger.info(word)
        logger.info("--")

        raise

        return

    @property
    def url(self):
        return self.site.dat_url(self.dat)


class SearchManager(object):
    """
    スレッドを検索する
    """

    def __init__(self, site):
        self.site = site

    def search_and_scraping(self, force=None):
        site = self.site

        # スレッド検索
        url = site.subject_url
        subjects = self.get_from_url(url)
        method = getattr(self, site.title)
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
        return [Subject(self.site, o[0], o[1], o[2]) for o in matched_list if int(o[2]) > constants.GEN_RES_MIN]

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


def _normalizationa(text):
    """
    レスを正規化してlist(int)にする
    e.g. >>1
    e.g. >>1-3
    :return: list(int)
    """
    s = text.strip('>>')
    if '-' not in text:
        return [int(s)]
    return [int(_s) for _s in s.split('-')]


def select_keyword(texts):
    """
    キーワードを抽出する
    :param texts: list(str)
    :return: list(str) キーワード一覧
    """
    # 標準化 記号や日本語以外を排除(実装したけど使ってないから残しておいた)
    # texts = select_japanese(texts)

    # 標準化 1行が短い文を排除
    texts = [_r for _r in texts if len(_r) > 2]

    # 抽出 カタカナ 3文字以上
    select_keywords = []
    r = re.compile(r'[ァ-ヴー・]+')
    for text in texts:
        for t in r.findall(text):
            if len(t) > 2:
                select_keywords.append(t)

    # 抽出 漢字 3文字以上
    r = re.compile(r'[一-龥]+')
    for text in texts:
        for t in r.findall(text):
            if len(t) > 2:
                select_keywords.append(t)

    # カウントする
    from collections import defaultdict
    d = defaultdict(int)
    for keyword in select_keywords:
        d[keyword] += 1

    # 5以上ならキーワード認定
    # 1スレッドあたり10-20が最高
    results = []
    for key in d:
        if InspectionWord.inspection(key):  # NGワードチェック
            continue

        if InspectionWord.inspection_keyword(key):  # NGワードチェック
            continue

        if d[key] > 4:
            results.append(key)
    return results


def select_japanese(texts):
    """
    :param texts: list[str]
    :rtype : list[str]
    """
    if len(texts) == 0:
        return []
    assert isinstance(texts[0], str), "type: {}, message: {}".format(type(texts[0]), texts[0])

    # アルファベットと半角英数と記号と改行とタブを排除
    r1 = re.compile(r'[a-zA-Z¥"¥.¥,¥@]+')
    r2 = re.compile(r'[!"“#$%&()\*\+\-\.,\/:;<=>?@\[\\\]^_`{|}~]')
    r3 = re.compile(r'[\n|\r|\t]')

    # 日本語以外の文字を排除(韓国語とか中国語とかヘブライ語とか)
    jp_chartype_tokenizer = nltk.RegexpTokenizer(u'([ぁ-んー]+|[ァ-ンー]+|[\u4e00-\u9FFF]+|[ぁ-んァ-ンー\u4e00-\u9FFF]+)')

    results = []
    for t in texts:
        text = r1.sub('', t)
        text = r2.sub('', text)
        text = r3.sub('', text)
        results.append("".join(jp_chartype_tokenizer.tokenize(text)))
    return results
