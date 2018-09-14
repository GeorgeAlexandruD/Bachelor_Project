import unittest
from obd_tcp_server import Host
import socket, time
import os
import threading

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
    def test_host(self):
        TCP_IP = str(os.getenv('VCAP_APP_HOST', '127.0.0.1'))
        TCP_PORT = int(os.getenv('VCAP_APP_PORT', '7777'))
        host = Host((TCP_IP,TCP_PORT))
        server_thread = threading.Thread(target=host.handle_accept)
        server_thread.start()
        time.sleep(0.01)
        fake_client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fake_client.connect((TCP_IP,TCP_PORT))
        
class TestObdtcp(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
        

if __name__ == '__main__':
    unittest.main()