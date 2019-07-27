# coding: utf-8
# 1.初始化数据库
# 2.数据表迁移

from flask_script import Manager 
from flask_migrate import Migrate, MigrateCommand
from tomato.app import app
from .model import db

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()