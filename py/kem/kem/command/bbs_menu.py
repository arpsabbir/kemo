# -*- coding: utf-8 -*-
from flask_script import Command, Option
import base64
import io
import os

PROJECT_ID = 'dena-auto-taxifms-dev-gcp'
project_id = PROJECT_ID
LOCATION_ID = 'global'
KEY_RING_ID = 'pantry'
CRYPTO_KEY_ID = 'config'


class BBSMenu(Command):
    """
    sync BBS Menu
    """
    def run(self):
        print("start")


