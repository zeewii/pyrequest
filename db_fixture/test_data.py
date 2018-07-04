#coding=utf-8

import sys,xlrd
sys.path.append('../db_fixture')
from mysql_db import DB
#PATH = './db_fixture/data.xlsx'
PATH = '/home/zeng/PycharmProjects/pyrequest/db_fixture/data.xlsx'


#发布会数据
def data_sign_event():
    datas = []
    xlsFile = xlrd.open_workbook(PATH)
    table = xlsFile.sheet_by_name('event_conf')
    for i in range(2,8):
        event = {}
        event['id'] = int(table.cell_value(i,0))
        event['name'] = table.cell_value(i,1)
        event['`limit`'] = int(table.cell_value(i,2))
        event['status'] = int(table.cell_value(i,3))
        event['address'] = table.cell_value(i,4)
        event['start_time'] = table.cell_value(i,5)
        event['create_time'] = table.cell_value(i,6)
        datas.append(event)
    return datas

#嘉宾数据
def data_sign_guest():
    datas = []
    xlsFile = xlrd.open_workbook(PATH)
    table = xlsFile.sheet_by_name('guest_conf')
    for i in range(2,5):
        event = {}
        event['id'] = int(table.cell_value(i,0))
        event['realname'] = table.cell_value(i,1)
        event['phone'] = int(table.cell_value(i,2))
        event['email'] = table.cell_value(i,3)
        event['sign'] = int(table.cell_value(i,4))
        event['event_id'] = int(table.cell_value(i,5))
        event['create_time'] = table.cell_value(i,6)
        datas.append(event)
    return datas

data_event = data_sign_event()
data_guest = data_sign_guest()
# 创建测试数据
datas = {
    # 发布会数据
    'sign_event':data_event,
    # 嘉宾表数据
    'sign_guest':data_guest,
}




# 将测试数据插入表
def init_data():
    db = DB()
    for table, data in datas.items():
        db.clear(table)
        for d in data:
            db.insert(table, d)
    db.close()





if __name__ == '__main__':
    init_data()
