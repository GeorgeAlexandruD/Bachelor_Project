from IncomingMsgFrame import IncomingMsgFrame
from TypesParser import TypesParser
import datetime
from MessageValidator import MessageValidator

class MsgAlarm(IncomingMsgFrame):
    def __init__(self, buff):
        IncomingMsgFrame.__init__(self, buff)

        self.response_code= 0xA003
        if self.error_code == 0:
            try:
                self.load(TypesParser)
            except:
                self.error_code = 1000 + self.cur

    def load(self, typeParser):
        self.cur = 0
        
        self.received_rand_id = typeParser.parse_u16(self.event_data[self.cur: self.cur +2])
        self.cur += 2

        self.alarm_tag = "new" if typeParser.parse_u8(self.event_data[self.cur: self.cur+1]) else "end"
        self.cur += 1

        self.alarm_no = typeParser.parse_u8(self.event_data[self.cur: self.cur+1]) 
        self.cur += 1

        self.alarm_threshold = typeParser.parse_u16(self.event_data[self.cur: self.cur+2])
        self.cur += 2

        self.alarm_value = typeParser.parse_u16(self.event_data[self.cur:self.cur+2])
        self.cur +=2

        self.event_timestamp = typeParser.parse_utc_time(self.event_data[self.cur: self.cur+6],typeParser)
        self.cur += 6
        
        self.alarm_location = typeParser.parse_gps_info(self.event_data[self.cur: self.cur+21], typeParser)

    def to_dict(self):
        res = dict()
        res['packet_type'] = 'alarm'
        res["timestamp"] = datetime.datetime.utcnow().isoformat()
        res["unit_id"] = str(self.unit_id)
        res["gps"] = self.alarm_location 
        res["tag"] = self.alarm_tag
        if self.alarm_no == 13:
            res["power_off"] = True

        return res

    def generate_response(self, typeParser):
        res = bytearray()

        res += typeParser.pack_u16(self.received_rand_id)

        return typeParser.pack(self.unit_id,self.response_code,TypesParser, MessageValidator ,res)