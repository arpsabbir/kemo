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
        person = self.gen_sample_pb2()
        print(type(person))
        print(person)
        print("----------")

        # binaryに変更
        b = person.SerializeToString()
        print(b)
        print(type(b))
        print("----------")

        # binary to instance
        person2 = deserialize(b, 'saga.auto_generated_python.news_pb2.News')
        print(type(person2))
        print(person2)

    def gen_sample_pb2(self):
        person = news_pb2.News()
        person.id = 1234
        person.name = "John Doe"
        person.email = "jdoe@example.com"
        phone = person.phones.add()
        phone.number = "555-4321"
        phone.type = news_pb2.News.HOME
        return person


def deserialize(byte_message, proto_type):
    module_, class_ = proto_type.rsplit('.', 1)
    class_ = getattr(import_module(module_), class_)
    rv = class_()
    rv.ParseFromString(byte_message)
    return rv
