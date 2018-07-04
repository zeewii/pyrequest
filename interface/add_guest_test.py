#coding=utf-8
import unittest
import requests
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data
from db_fixture.mysql_db import DB


class AddGuestTest(unittest.TestCase):
    u''' 添加嘉宾接口测试 '''
    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/add_guest/"

    def test_001_add_guest_all_null(self):
        u''' 所有参数为空 '''
        payload = {'eid':'','realname':'','phone':'','email':""}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertEqual(self.result['message'], 'parameter error')

    def test_002_add_guest_one_param_null(self):
        u''' eid，realname,phone中有一个为空 '''
        payload = {'eid':'','realname':'zeng','phone':'13410048448','email':""}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertEqual(self.result['message'], 'parameter error')

    def test_003_add_guest_eid_exist(self):
        u''' 发布会的eid不存在 '''
        payload = {'eid':20,'realname':'zeng','phone':'13410048448','email':"zeng@mail.com"}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], 'event id null')

    def test_004_add_guest_event_False(self):
        u''' 发布会的状态为False '''
        payload = {'eid':3,'realname':'zeng','phone':'13410048448','email':"zeng@mail.com"}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10023)
        self.assertEqual(self.result['message'], 'event status is not available')

    def test_005_add_guest_event_number_full(self):
        u''' 嘉宾人数大于发布会的嘉宾限制人数 '''
        payload = {'eid':6,'realname':'zeng','phone':'13410048448','email':"zeng@mail.com"}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10024)
        self.assertEqual(self.result['message'], 'event number is full')

    def test_006_add_guest_event_startime(self):
        u''' 发布会开始时间大于当前时间，不能添加嘉宾 '''
        payload = {'eid':5,'realname':'zeng','phone':'13410048448','email':"zeng@mail.com"}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10025)
        self.assertEqual(self.result['message'], 'event has started')

    # def test_007_add_event_eid_exist(self):
    #     u''' 嘉宾手机号码重复，不能添加嘉宾 '''
    #     payload = {'eid':1,'realname':'zeng','phone':'13511001101','email':"zeng@mail.com"}
    #     r = requests.post(self.base_url, data=payload)
    #     self.result = r.json()
    #     self.assertEqual(self.result['status'], 10026)
    #     self.assertEqual(self.result['message'], 'the event guest phone number repeat')

    def test_008_add_guest_success(self):
        u''' 添加成功 '''
        payload = {'eid':2,'realname':'zeng1','phone':'13511001188','email':"zeng1@mail.com"}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'add guest success')



    def tearDown(self):
        print self.result

if __name__ == '__main__':
    unittest.main()
