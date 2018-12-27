# -*- coding: utf-8 -*-
from flask import Flask, request, current_app


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    return app
