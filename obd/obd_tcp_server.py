import asyncore, socket
import os
from MsgHandler import MsgHandler
import collections
import time

import json


TCP_IP = str(os.getenv('VCAP_APP_HOST', '127.0.0.1'))
TCP_PORT = int(os.getenv('VCAP_APP_PORT', '3333'))
host = None


class Client(asyncore.dispatcher):
    def __init__(self, host,socket,addr):
        asyncore.dispatcher.__init__(self, socket)
        self.host = host
        self.unit_id = "unknown"
        
        self.outbox = collections.deque()
        self.last_write = time.time()
        self.msgHandler= MsgHandler()

    def handle_read(self):
        try:
            buff = bytearray(self.recv(1024))
        except:
            pass
        self.reading(buff, self.unit_id, self.msgHandler, self.outbox)

    def reading(self, buff, unit_id, msgHandler,  outbox):
        packets = msgHandler.lock_packet(buff)
        for (start, end) in packets:
            if start>=0 and end >0:
                if unit_id is "unknown":
                    unit_id = msgHandler.get_unit_id(buff[start:end])

                # todo: publish or not
 
                res = msgHandler.process(unit_id,buff[start:end])

                if res is not None:
                    outbox.append(res)
        

    def handle_write(self):

        message = self.writing(self.outbox, self.last_write)
        if message is not None:
            self.send(message)

    def writing(self, outbox, last_write):
        if not outbox or bool(time.time() - last_write < 1.0):
            time.sleep(0.2) 
            return None

        message = outbox.popleft()
        if len(message) > 1024:
            raise ValueError('Message too long')
        last_write = time.time()
        return message

class Host(asyncore.dispatcher):
    def __init__(self, address=('127.0.0.1', 3333)):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        self.listen(1)
        self.clients=[]

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            socket, addr = pair
            self.add_client(socket,addr, self, self.clients)

    def add_client(self, socket, addr,host, clients):
        clients.append(Client(host,socket,addr))



if __name__ == '__main__':
    host = Host((TCP_IP, TCP_PORT))
    try:
        asyncore.loop()
    except:
        asyncore.close_all()
    



    