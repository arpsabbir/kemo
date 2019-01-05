# -*- coding: utf-8 -*-
from flask_script import Manager, Server
import saga
import config
from saga.command.bbs_menu import BBSMenu
from saga.command.site_gen import SiteGen

manager = Manager(saga.create_app(config))

# manage.py option
# manager.add_option('-c', '--config', dest='config', required=False)

######################
# コマンド追加
######################
manager.add_command('sync-menu', BBSMenu)
manager.add_command('gen', SiteGen)

# runserver
manager.add_command('runserver', Server(use_reloader=True))


if __name__ == "__main__":
    manager.run()