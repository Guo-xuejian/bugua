import pymysql

pymysql.install_as_MySQLdb()  # 用pymysql替代MySQLdb
pymysql.version_info = (1, 4, 13, "final", 0)
