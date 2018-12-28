class Config(object):
    USERNAME = 'admin'
    PASSWORD = 'admin'


class ProductionConfig(Config):
    DB = '127.0.0.1'
    PORT = 65521
    DBUSERNAME = 'scan'
    DBPASSWORD = 'scanlol66'
    DBNAME = 'xunfeng'


class Vulnerability():
    sql={{'title':'sql盲注',
         'rank': '高',
         'repair': '全局数据过滤，避免用户输入的危害数据传输到数据库后台。'
         },
         }
    xss={'title':'sql注入',
         'rank': '高',
         'repair': '全局数据过滤，避免用户输入的危害数据传输到数据库后台。'
         }