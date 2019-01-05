# -*- coding: utf-8 -*-
from logging import getLogger, StreamHandler, DEBUG

# logを標準出力するためのおまじない
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
