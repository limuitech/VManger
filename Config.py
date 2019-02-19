class Config(object):
    USERNAME = 'admin'
    PASSWORD = 'admin'

    DIALECT = 'mysql'  # 要用的什么数据库
    DRIVER = 'mysqlconnector'  # 连接数据库驱动
    DBUSERNAME = 'root'  # 用户名
    DBPASSWORD = 'root'  # 密码
    HOST = 'localhost'  # 服务器
    PORT = '3306'  # 端口
    DATABASE = 'vmanager'  # 数据库名

    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, DBUSERNAME, DBPASSWORD, HOST,
                                                                           PORT, DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    AWVS_URL = "https://192.168.137.160:3443/"
    AWVS_USERNAME = "918936661@qq.com"
    AWVS_PASSWORD = "a40b344dfecdb70b9690076b0f1c40176887cc6a8f269cce10ff55fbf78205e9" #sha256加密后的密码，通过burp抓包可获取,也可以使用(http://tool.oschina.net/encrypt?type=2)把密码进行加密之后填入，请区分大小写、中英文字符。

    NESSUS_URL = ""
    NESSUS_USERNAME = ""
    NESSUS_PASSWORD = ""





