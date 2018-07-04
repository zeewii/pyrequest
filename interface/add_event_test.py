#coding=utf-8
import unittest
import requests
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data
from db_fixture.mysql_db import DB


class AddEventTest(unittest.TestCase):
    u''' 添加发布会接口测试 '''
    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/add_event/"

    def test_001_add_event_all_null(self):
        u''' 所有参数为空 '''
        payload = {'eid':'','name':'','limit':'','address':"",'start_time':''}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertEqual(self.result['message'], 'parameter error')

    def test_002_add_event_one_param_null(self):
        u''' 某一个参数为空 '''
        payload = {'eid':20,'name':"iphone12",'limit':"",'address':"shenzhen",'start_time':'2017-10-09 12:00:00'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertEqual(self.result['message'], 'parameter error')

    def test_003_add_event_eid_exist(self):
        u''' id已经存在 '''
        payload = {'eid':1,'name':"iphone10",'limit':2000,'address':'shenzhen','start_time':'2017-10-09 12:00:00'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], 'event id already exists')

    def test_004_add_event_name_exist(self):
        u''' 名称已经存在 '''
        payload = {'eid':11,'name':"iphone1",'limit':2000,'address':"shenzhen",'start_time':'2017-10-09 12:00:00'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10023)
        self.assertEqual(self.result['message'], 'event name already exists')

    def test_005_add_event_data_type_error(self):
        u''' 日期格式错误 '''
        payload = {'eid':15,'name':"iphone8",'limit':2000,'address':"shenzhen",'start_time':'2017'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10024)
        self.assertIn('start_time format error.', self.result['message'])

    def test_006_add_event_success(self):
        u''' 添加成功 '''
        payload = {'eid':12,'name':"iphone12",'limit':2000,'address':"shenzhen",'start_time':'2017-10-09 12:00:00'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()

        #删除新添加的数据，以便后面的测试
        database = DB()
        database.clear_condition('sign_event','id=12')

        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'add event success')


    def tearDown(self):
        print self.result

if __name__ == '__main__':
    unittest.main()
