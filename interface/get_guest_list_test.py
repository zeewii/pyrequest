#coding=utf-8
import unittest
import requests
import os, sys,random
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data
from db_fixture.mysql_db import DB


class GetGuestListTest(unittest.TestCase):
    u''' 查询发布会接口测试'''
    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/get_guest_list/"

    def test_001_get_guest_list_eid_null(self):
        u''' 查询请求的eid为空'''
        params = {'eid':'','phone':'13511001100'}
        r = requests.get(self.base_url, params=params)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertEqual(self.result['message'], 'eid cannot be empty')

    def test_002_get_guest_list_phone_null_success(self):
        u'''eid不为空，但手机号为空,eid存在，查询成功'''
        params = {'eid':1}
        r = requests.get(self.base_url, params=params)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'success')

    def test_003_get_guest_list_eid_noexist_phone_null(self):
        u'''eid不为空，但手机号为空,但eid不存在时，查询失败'''
        params = {'eid': 2}
        datas = test_data.data_event
        r = requests.get(self.base_url, params=params)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], 'query result is empty')


    def test_004_get_guest_list_eid_phone_exist_success(self):
        u'''eid不为空，手机号不为空,eid,手机号都存在，查询成功'''
        params = {'eid': 1, 'phone':'13511001101'}
        r = requests.get(self.base_url, params=params)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'success')

    def test_005_get_guest_list_eid_noexist(self):
        u'''eid不为空，手机号不为空,eid不存在，查询失败'''
        params = {'eid': 2, 'phone':'13511001101'}
        r = requests.get(self.base_url, params=params)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], 'query result is empty')

    def test_006_get_guest_list_phone_noexist(self):
        u'''eid不为空，手机号不为空,手机号不存在，查询失败'''
        params = {'eid': 1, 'phone':'1351101110'}
        r = requests.get(self.base_url, params=params)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], 'query result is empty')

    def test_007_get_guest_list_eid_phone_noexist(self):
        u'''eid不为空，手机号不为空,eid和手机号都不存在，查询失败'''
        params = {'eid': 20, 'phone':'1351101110'}
        r = requests.get(self.base_url, params=params)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], 'query result is empty')


    def tearDown(self):
        print self.result

if __name__ == '__main__':
    # 初始化接口测试数据
    test_data.init_data()
    unittest.main()
