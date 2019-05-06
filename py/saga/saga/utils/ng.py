# -*- coding: utf-8 -*-
import re
from saga import constants_inspection_word as ng


class InspectionWord(object):
    # クラスオブジェクトにキャッシュ
    _INSPECTION_PATTERN = None

    @classmethod
    def get_re_compile(cls):
        """
        禁止文字にマッチさせるための正規表現文字列
        :rtype : _sre.SRE_Pattern
        """
        if cls._INSPECTION_PATTERN:
            return cls._INSPECTION_PATTERN
        body = '|'.join([word for word in ng.NG_WORDS])
        r = re.compile("({})".format(body))
        cls._INSPECTION_PATTERN = r
        return r

    @classmethod
    def inspection(cls, word):
        """
        ワードが禁止文字列を含んでいるとTrue
        :param word: unicode
        :rtype : bool
        """
        if len(word.strip()) == 0:  # 空白のみで構成されている
            return False
        r = cls.get_re_compile()
        m = r.search(word)
        if bool(m):
            return True

        # アフィチェック
        return inspection_affiliate(word)


def inspection_affiliate(word):
    """
    ワードが禁止文字列を含んでいるとTrue
    :param word: unicode
    :rtype : bool
    """
    if len(word.strip()) == 0:  # 空白のみで構成されている
        return False
    r = re.compile("あふぃ|アフィ|ア.*フィ|ア.*ふぃ|あ.*ふぃ|あ.*フィ|あ.*フ.*ィ|クリック|くりっく|広告")
    m = r.search(word)
    return bool(m)
