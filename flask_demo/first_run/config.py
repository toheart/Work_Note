
class Config(object):
    pass

class ProdConfig(object):
    pass

class DevConfig(object):
    DEBUG = True
    # sqlalchemy的配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1@192.168.11.11:3306/flask'
    # 打印输出SQL语句
    SQLALCHEMY_ECHO = True
    