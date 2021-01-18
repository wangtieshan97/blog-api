from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config

# 数据库实例
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化
    db.init_app(app)

    # 注册蓝图
    from main.api import api
    app.register_blueprint(api, url_prefix = '/api')

    return app
