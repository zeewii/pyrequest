#coding=utf-8
#描述：测试带Auth的认证安全机制的查询发布会接口
#requtests库的get(),post()方法均提供有auth参数，用于设置用户签名
import unittest
import requests
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data
from db_fixture.mysql_db import DB

data_event = test_data.data_sign_event()


class SecAuthGetEventListTest(unittest.TestCase):
    u''' 查询发布会信息(带auth用户认证的安全机制的接口) '''
    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/sec_auth_get_event_list/"

    def test_001_get_event_list_auth_null(self):
        u''' auth为空 '''
        r = requests.get(self.base_url,params={'eid':1})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10011)
        self.assertEqual(self.result['message'], 'user auth null')

    def test_002_get_event_list_auth_error(self):
        u''' auth错误 '''
        auth_user = ('abc', '123')
        r = requests.get(self.base_url,auth=auth_user,params={'eid':1})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10012)
        self.assertEqual(self.result['message'], 'user auth fail')

    def test_003_get_event_list_eid_null(self):
        u''' eid参数为空 '''
        auth_user = ('admin', 'admin123456')
        r = requests.get(self.base_url,auth=auth_user,params={'eid':''})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertEqual(self.result['message'], 'parameter error')

    def test_004_get_event_list_eid_success(self):
        u''' 根据eid查询结果成功 '''
        auth_user = ('admin', 'admin123456')
        r = requests.get(self.base_url,auth=auth_user,params={'eid':data_event[0]['id']})
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'success')
        self.assertEqual(self.result['data']['name'],data_event[0]['name'])
        self.assertEqual(self.result['data']['address'],data_event[0]['address'])

    def tearDown(self):
        print self.result

if __name__ == '__main__':
    # 初始化接口测试数据
    test_data.init_data()
    unittest.main()
