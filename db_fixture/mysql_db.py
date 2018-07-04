#coding=utf-8
from pymysql import connect, cursors
from pymysql.err import OperationalError
import os
import configparser as cparser


# ======== 读取db_config.ini文件设置 ===========
base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_config.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

host = cf.get("mysqlconf", "host")
port = cf.get("mysqlconf", "port")
db   = cf.get("mysqlconf", "db_name")
user = cf.get("mysqlconf", "user")
password = cf.get("mysqlconf", "password")


# ======== 封装MySql基本操作 ===================
class DB:

    def __init__(self):
        try:
            # 连接数据库
            self.conn = connect(host=host,
                                user=user,
                                password=password,
                                db=db,
                                charset='utf8mb4',
                                cursorclass=cursors.DictCursor)
        except OperationalError as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    # 清除表中所有数据
    def clear(self, table_name):
        # real_sql = "truncate table " + table_name + ";"
        real_sql = "delete from " + table_name + ";"
        with self.conn.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(real_sql)
        self.conn.commit()
        print "delete table:%s success!"%table_name

    # 根据条件，清除表中数据
    def clear_condition(self, table_name, condition):
        # real_sql = "truncate table " + table_name + ";"
        real_sql = "delete from " + table_name + " where " + condition + ";"
        print real_sql
        with self.conn.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(real_sql)
        self.conn.commit()
        print "delete table:%s where %s success!"%(table_name,condition)

    # 插入表数据
    def insert(self, table_name, table_data):
        for key in table_data:
            table_data[key] = "'"+str(table_data[key])+"'"
        key   = ','.join(table_data.keys())
        value = ','.join(table_data.values())
        real_sql = "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ");"
        #print(real_sql)
        with self.conn.cursor() as cursor:
            cursor.execute(real_sql)
        self.conn.commit()
        print "insert table:%s values:%s"%(table_name,table_data)

    # 关闭数据库连接
    def close(self):
        self.conn.close()

if __name__ == '__main__':

    db = DB()
    table_name = "sign_event"
    data = {'id':1,'name':'iphone X','`limit`':2000,'status':1,'address':'shenzhen','start_time':'2017-12-25 12:00:00','create_time':'2017-10-9 15:15:00'}

    db.clear(table_name)
    db.insert(table_name, data)
    db.clear_condition(table_name, "id=2")
    db.close()

    # table_name = "sign_guest"
    # data = {'id':1,'realname':'alen','phone':13511001100,'email':'alen@mail.com','sign':0,'event_id':1,'create_time':'2017-10-9 15:15:00'}
    # db.clear(table_name)
    # db.insert(table_name, data)
    # db.close()
    #




    # table_name = "sign_guest"
    # db.clear(table_name)
    # for i in range(1,3001):
    #     id = i
    #     realname = 'zeng'+ str(i)
    #     phone = 13811000000+i
    #     email = 'zeng0' + str(i) + "@mail.com"
    #     data = {'id':id,'realname':realname,'phone':phone,'email':email,'sign':0,'event_id':1,'create_time':'2017-12-25 15:00:00'}
    #
    #
    #
    #     db.insert(table_name, data)
    # db.close()















