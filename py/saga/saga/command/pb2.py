# -*- coding: utf-8 -*-
from flask_script import Command
from logging import getLogger
logger = getLogger(getLogger.__str__())


class Pb2(Command):
    """
    protobuf test
    """

    def run(self):
        logger.info("start")
        person = self._main()
        print(type(person))
        print(person)

    def _main(self):
        from saga.auto_generated_python import news_pb2
        person = news_pb2.News()
        person.id = 1234
        person.name = "John Doe"
        person.email = "jdoe@example.com"
        phone = person.phones.add()
        phone.number = "555-4321"
        phone.type = news_pb2.News.HOME
        return person
