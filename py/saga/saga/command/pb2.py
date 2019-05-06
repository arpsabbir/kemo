# -*- coding: utf-8 -*-
from flask_script import Command
from logging import getLogger
from saga.auto_generated_python import news_pb2
from importlib import import_module
logger = getLogger(getLogger.__str__())


class Pb2(Command):
    """
    protobuf test
    """

    def run(self):
        logger.info("start")
        news = self.gen_sample_pb2()
        print(type(news))
        print(news)
        print(news.keywords[0])
        print(news.keywords[1])
        print(news.keywords[2])
        print("----------")

        # binaryに変更
        b = news.SerializeToString()
        print(b)
        print(type(b))
        print("----------")

        # binary to instance
        news2 = deserialize(b, 'saga.auto_generated_python.news_pb2.News')
        print(type(news2))
        print(news2)
        print(news2.keywords[0])
        print(news2.posts[0].text)

    def gen_sample_pb2(self):
        news = news_pb2.News()
        news.keywords.extend(["アアア", "いいい", "漢字"])
        post = news.posts.add()
        post.rank = 10
        post.text = "テスト投稿10"
        post.post_at = 1557137832
        post2 = news.posts.add()
        post2.rank = 20
        post2.text = "テスト投稿20"
        post2.post_at = 1557137852
        return news


def deserialize(byte_message, proto_type):
    module_, class_ = proto_type.rsplit('.', 1)
    class_ = getattr(import_module(module_), class_)
    rv = class_()
    rv.ParseFromString(byte_message)
    return rv
