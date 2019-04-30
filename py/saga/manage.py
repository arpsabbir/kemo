# -*- coding: utf-8 -*-
from flask_script import Manager, Server
import saga
import config
from saga.command.bbs_menu import BBSMenu
from saga.command.site_gen import SiteGen
from saga.command.pb2 import Pb2

manager = Manager(saga.create_app(config))

# manage.py option
# manager.add_option('-c', '--config', dest='config', required=False)

######################
# コマンド追加
######################
manager.add_command('sync-menu', BBSMenu)
manager.add_command('gen', SiteGen)
manager.add_command('proto', Pb2)

# runserver
manager.add_command('runserver', Server(use_reloader=True))


if __name__ == "__main__":
    manager.run()
