# -*- coding: utf-8 -*-
from flask_script import Manager, Server
import kem
import config
from kem.command.bbs_menu import BBSMenu

manager = Manager(kem.create_app(config))

# manage.py option
# manager.add_option('-c', '--config', dest='config', required=False)

######################
# コマンド追加
######################
manager.add_command('encrypt', BBSMenu)

# runserver
manager.add_command('runserver', Server(use_reloader=True))


if __name__ == "__main__":
    manager.run()