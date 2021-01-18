import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # 不编码中文
    JSON_AS_ASCII = False

    # 用户信息
    USERNAME = os.environ.get('USERNAME') or 'wangtieshan'
    PASSWORD = os.environ.get('PASSWORD') or '000000'

    # 服务器密钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 文件上传
    #UPLOAD_FOLDER = '/var/www/html/images'
    UPLOAD_FOLDER = os.path.join(basedir, 'files')
    ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg', 'gif' }
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
