from IncomingMsgFrame import IncomingMsgFrame
from TypesParser import TypesParser as type_parser
import datetime

class MsgAlarm(IncomingMsgFrame):
    def __init__(self, buff):
        IncomingMsgFrame.__init__(self, buff)

        self.response_code= 0xA003
        if self.error_code == 0:
            try:
                self.load()
            except:
                self.error_code = 1000 + self.cur

    def load(self):
        self.cur = 0
        
        self.received_rand_id = type_parser.parse_u16(self.event_data[self.cur: self.cur +2])
        self.cur += 2

        self.alarm_tag = "new" if type_parser.parse_u8(self.event_data[self.cur: self.cur+1]) else "end"
        self.cur += 1

        self.alarm_no = type_parser.parse_u8(self.event_data[self.cur: self.cur+1]) 
        self.cur += 1

        self.alarm_threshold = type_parser.parse_u16(self.event_data[self.cur: self.cur+2])
        self.cur += 2

        self.alarm_value = type_parser.parse_u16(self.event_data[self.cur:self.cur+2])
        self.cur +=2

        self.event_timestamp = type_parser.parse_utc_time(self.event_data[self.cur: self.cur+6])
        self.cur += 6
        
        self.alarm_location = type_parser.parse_gps_info(self.event_data[self.cur: self.cur+21])

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

    def generate_response(self):
        res = bytearray()

        res += type_parser.pack_u16(self.received_rand_id)

        return type_parser.pack(self.unit_id,self.response_code, res)