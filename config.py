from datetime import timedelta
import os

#数据库基本配置
class BaseConfig:
  SECRET_KEY = "your secret key"
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  PERMANENT_SESSION_LIFETIME = timedelta(days=7)

  UPLOAD_IMAGE_PATH = os.path.join(os.path.dirname(__file__),"media")

  PER_PAGE_COUNT = 10

#开发环境
class DevelopmentConfig(BaseConfig):
  # 数据库配置
  HOSTNAME = '127.0.0.1'
  PORT = '3306'
  DATABASE = 'happy_bb'
  USERNAME = 'root'
  PASSWORD = '123456'
  DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
  SQLALCHEMY_DATABASE_URI = DB_URI

  # 缓存配置
  CACHE_TYPE = "RedisCache"
  CACHE_REDIS_HOST = "127.0.0.1"
  CACHE_REDIS_PORT = 6379

  # Celery配置
  # 格式：redis://:password@hostname:port/db_number
  CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
  CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"

  AVATARS_SAVE_PATH = os.path.join(BaseConfig.UPLOAD_IMAGE_PATH,"avatars")

  # 邮箱配置
  # dyqqdrlduggojjhb
  MAIL_SERVER = "smtp.qq.com"
  MAIL_USE_SSL = True
  MAIL_PORT = 465
  MAIL_USERNAME = "1091909200@qq.com"
  MAIL_PASSWORD = "dyqqdrlduggojjhb"
  MAIL_DEFAULT_SENDER = "1091909200@qq.com"

  # 随机头像
  AVATARS_SAVE_PATH = os.path.join(BaseConfig.UPLOAD_IMAGE_PATH, "avatars")

#测试环境
class TestingConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI = "mysql+pymysql://[测试服务器MySQL用户名]:[测试服务器MySQL密码]@[测试服务器MySQL域名]:[测试服务器MySQL端口号]/pythonbbs?charset=utf8mb4"

#线上环境
class ProductionConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI = "mysql+pymysql://[生产环境服务器MySQL用户名]:[生产环境服务器MySQL密码]@[生产环境服务器MySQL域名]:[生产环境服务器MySQL端口号]/pythonbbs?charset=utf8mb4"
