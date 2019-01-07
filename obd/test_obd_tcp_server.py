import unittest
from obd_tcp_server import Host
import socket, time
import os
import threading
from MsgHandler import MsgHandler
import collections
from obd_tcp_server import Client, Host
from mock import Mock
import socket
import asyncore

        
class TestObdtcpRead(unittest.TestCase):
    def setUp(self):
        self.valid_buff = bytearray.fromhex("404039003247512d313630313030383803201000010f0000002d0703110f1b390703110f1b030c549e3d0c2aec200200000000000034080d0a")
        self.invalid_buff = bytearray.fromhex("404036")
        self.msgHandler = MsgHandler()
        self.valid_unit_id = "unknown"
        self.valid_box = collections.deque()
        
        host = Mock()
        socket = Mock()
        addr = Mock()   
        self.client = Client(host,socket, addr)

    def tearDown(self):
        self.client =None

    def test_reading_output(self):
        self.client.reading(self.valid_buff,self.valid_unit_id,self.msgHandler,self.valid_box)
        self.assertGreater(len(self.valid_box),0)


    def test_reading_invalid_buff(self):
        self.client.reading(self.invalid_buff,self.valid_unit_id,self.msgHandler,self.valid_box)
        self.assertEqual(len(self.valid_box),0)
        
       

    

if __name__ == '__main__':
    unittest.main()