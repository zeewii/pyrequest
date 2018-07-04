#coding=utf-8
import unittest
import requests
import os, sys,random
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data
from db_fixture.mysql_db import DB


class GetEventListTest(unittest.TestCase):
    u''' 查询发布会接口测试'''
    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/get_event_list/"

    def test_001_get_event_list_eid_name_null(self):
        u''' 查询请求的eid和发布会名称name都为空'''
        params = {'eid':'','name':''}
        r = requests.get(self.base_url, params=params)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertEqual(self.result['message'], 'parameter error')

    def test_002_get_event_list_eid_error(self):
        u'''发布会id不存在'''
        params = {'eid':190}
        r = requests.get(self.base_url, params=params)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], 'query result is empty')
    #
    # def test_003_get_event_list_eid_success(self):
    #     u'''发布会id存在,查询成功'''
    #     #在data.xlsx的发布会列表的行数中去随机数
    #     i = random.randint(0,5)
    #     print "random data is %s"%i
    #     datas = test_data.data_event
    #     eid = datas[i]['id']
    #     print "eid is %s"%eid
    #     params = {'eid': eid}
    #     print params
    #     #遍查datas，得到id为i的发布会
    #     for data in datas:
    #         if data['id'] == eid:
    #             #取出id为1的发布会所在datas的索引号
    #             index = datas.index(data)
    #             print "the index of event id equal 1 is %s"%index
    #             print data
    #
    #     r = requests.get(self.base_url, params=params)
    #     self.result = r.json()
    #     self.assertEqual(self.result['status'], 200)
    #     self.assertEqual(self.result['message'], 'success')
    #     self.assertEqual(self.result['data']['name'], datas[index]['name'])
    #     self.assertEqual(self.result['data']['status'], datas[index]['status'])
    #     self.assertEqual(self.result['data']['address'], datas[index]['address'])
    #     self.assertEqual(self.result['data']['limit'], datas[index]['`limit`'])

    def test_003_get_event_list_eid_success(self):
        u'''发布会id存在,查询成功'''
        params = {'eid': 1}
        r = requests.get(self.base_url, params=params)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'success')
        self.assertEqual(self.result['data']['name'], 'iphone1')
        self.assertEqual(self.result['data']['status'], True)
        self.assertEqual(self.result['data']['address'], 'shenzhen')
        self.assertEqual(self.result['data']['limit'], 2000)

    def test_004_get_event_list_name_error(self):
        u'''发布会name不存在'''
        params = {'name':'xiaomi'}
        r = requests.get(self.base_url, params=params)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], 'query result is empty')

    # def test_005_get_event_list_name_success(self):
    #     u'''发布会name存在,查询成功'''
    #      #在data.xlsx的发布会列表的行数中去随机数
    #     i = random.randint(0,5)
    #     print "random data is %s"%i
    #     datas = test_data.data_event
    #     name = datas[i]['name']
    #     print "name is %s"%name
    #     params = {'name': name}
    #     print params
    #     #遍查datas，得到id为i的发布会
    #     for data in datas:
    #         if data['name'] == name:
    #             #取出id为1的发布会所在datas的索引号
    #             index = datas.index(data)
    #             print "the index of event name equal %s is %s"%(name,index)
    #             print data
    #     r = requests.get(self.base_url, params=params)
    #     self.result = r.json()
    #     self.assertEqual(self.result['status'], 200)
    #     self.assertEqual(self.result['message'], 'success')
    #     self.assertEqual(self.result['data'][0]['limit'], datas[index]['`limit`'])
    #     self.assertEqual(self.result['data'][0]['status'], datas[index]['status'])
    #     self.assertEqual(self.result['data'][0]['address'], datas[index]['address'])

    def test_005_get_event_list_name_success(self):
        u'''发布会name存在,查询成功'''
        datas = test_data.data_event
        params = {'name': 'iphone2'}
        r = requests.get(self.base_url, params=params)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'success')
        self.assertEqual(self.result['data'][0]['limit'], 2000)
        self.assertEqual(self.result['data'][0]['status'], True)
        self.assertEqual(self.result['data'][0]['address'], 'shenzhen')

    def tearDown(self):
        print self.result

if __name__ == '__main__':
    # 初始化接口测试数据
    test_data.init_data()
    unittest.main()
