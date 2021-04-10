import pymysql
from libs.config import global_config

class Mysql(object):
    def __init__(self, cfg = global_config):
        params = cfg.items('mysql')
        try:
            self._conn = pymysql.connect(host=params[0][1], user=params[2][1], passwd=params[3][1], port=int(params[1][1]))
            self._cur = self._conn.cursor()
            self._flag = True
        except Exception as e:
            print(e)
            self._flag = False
            exit(1)
        if self._cur.execute('SELECT * FROM information_schema.SCHEMATA where SCHEMA_NAME="p_acg"'):
            self._cur.execute('USE p_acg')
        else:
            print('ERROR1:目标数据库不存在!')
        if not self._cur.execute('SELECT * FROM information_schema.TABLES where TABLE_NAME="tb_imgs"'):
            print('ERROR2:目标数据表不存在！')

    def search(self, fact):
        self._cur.execute(fact)
        return self._cur.fetchall()

    def takeall(self, tail = ''):
        self._cur.execute('SELECT title FROM tb_imgs ' + tail)
        titles = self._cur.fetchall()
        self._cur.execute('SELECT links FROM tb_imgs ' + tail)
        links = self._cur.fetchall()
        self._cur.execute('SELECT names FROM tb_imgs ' + tail)
        names = self._cur.fetchall()
        return (titles, links, names)

    def close(self):
        if self._flag:
            self._cur.close()
            self._conn.close()
            self._flag = False
        print('与数据库主机%s连接已成功断开。' % global_config.items('mysql')[0][1])

    def __del__(self):
        if self._flag:
            self._cur.close()
            self._conn.close()

global_mysql = Mysql()