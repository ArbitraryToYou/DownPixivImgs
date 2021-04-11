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
            input('Press any key to quit.')
            exit(1)
        if self._cur.execute('SELECT * FROM information_schema.SCHEMATA where SCHEMA_NAME="p_acg"'):
            self._cur.execute('USE p_acg')
        else:
            self._cur.execute('CREATE DATABASE p_acg')#存在的话就会报错
            self._cur.execute('USE p_acg')
            print('Tip:成功创建数据库"p_acg"!')
        if not self._cur.execute('SELECT * FROM information_schema.TABLES where TABLE_NAME="tb_imgs"'):
            self._cur.execute('CREATE TABLE tb_imgs(id BIGINT(7) NOT NULL AUTO_INCREMENT, title VARCHAR(150) NOT NULL, type VARCHAR(50) NOT NULL, date DATE NOT NULL, links VARCHAR(5000), names VARCHAR(5000), PRIMARY KEY (id))')
            print('Tip:成功创建表tb_imgs!')

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

    def insert(self, title, type, date, bf_links, bf_names):
        links = '|'.join(bf_links)
        names = '|'.join(bf_names)
        sql = "INSERT INTO tb_imgs (title, type, date, links, names) VALUES ('%s', '%s', str_to_date('%s', '%%Y-%%m-%%d'), '%s', '%s')" % (title, type, date, links, names)
        self._cur.execute(sql)
        self._conn.commit()

    def isRepeat(self, title, date):
        sql_title = 'SELECT * from tb_imgs where title = "%s" and date = "%s"' % (title, date)
        return self._cur.execute(sql_title)

    def close(self):
        if self._flag:
            self._cur.close()
            self._conn.close()
            self._flag = False

    def myRollback(self):
        self._conn.rollback()

    def __del__(self):
        if self._flag:
            self._cur.close()
            self._conn.close()

global_mysql = Mysql()