
class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_BINDS  = {
        'school': 'mysql://root:1@192.168.11.11/school',
        'user': 'mysql://root:sangfor@192.200.41.233/user'
    }