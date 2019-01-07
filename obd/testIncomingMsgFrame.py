from IncomingMsgFrame import IncomingMsgFrame
import unittest
from mock import Mock
from TypesParser import TypesParser
from MessageValidator import MessageValidator

class TestPreload(unittest.TestCase):
    def setUp(self):
        
        self.goodMsg =   bytearray.fromhex("404039003247512d313630313030383803201000010f0000002d0703110f1b390703110f1b030c549e3d0c2aec2002000000000000 3408 0d0a")
        self.wrongCRC =  bytearray.fromhex("404039003247512d313630313030383803201000010f0000002d0703110f1b390703110f1b030c549e3d0c2aec2002000000000000 0000 0d0a")
        self.wrongHead = bytearray.fromhex("000039003247512d313630313030383803201000010f0000002d0703110f1b390703110f1b030c549e3d0c2aec2002000000000000 1f1a 0d0a")
        self.wrongTail = bytearray.fromhex("404039003247512d313630313030383803201000010f0000002d0703110f1b390703110f1b030c549e3d0c2aec2002000000000000 3408 0000")
        self.wrongLen =  bytearray.fromhex("404039003247512d313630313030383803201000010f0000002d0703110f1b390703110f1b030c549e3d0c2aec200200000000000034080d0a0000")
        
        self.tp = TypesParser
        self.mv = MessageValidator
        
    def tearDown(self):
        pass
        

    def test_preload_goodMsg(self):
        self.msgFrame = IncomingMsgFrame(self.goodMsg)
        result = self.msgFrame.preload(self.tp,self.mv,self.msgFrame.get_event_type)
        self.assertEqual(result,0)

    def test_preload_wrong_CRC(self):
        self.msgFrame = IncomingMsgFrame(self.wrongCRC)
        result = self.msgFrame.preload(self.tp,self.mv,self.msgFrame.get_event_type)
        self.assertEqual(result,4)

    def test_preload_wrong_head(self):
        self.msgFrame = IncomingMsgFrame(self.wrongHead)
        result = self.msgFrame.preload(self.tp,self.mv,self.msgFrame.get_event_type)
        self.assertEqual(result,3)

    def test_preload_wrong_tail(self):
        self.msgFrame = IncomingMsgFrame(self.wrongTail)
        result = self.msgFrame.preload(self.tp,self.mv,self.msgFrame.get_event_type)
        self.assertEqual(result,1)

    def test_preload_wrong_len(self):
        self.msgFrame = IncomingMsgFrame(self.wrongLen)
        result = self.msgFrame.preload(self.tp,self.mv,self.msgFrame.get_event_type)
        self.assertEqual(result,2)

if __name__ == '__main__':
    unittest.main()