from TypesParser import TypesParser
from MessageValidator import MessageValidator


class IncomingMsgFrame:
    def __init__(self, message):
        self.msg = message
        
        self.unit_id= ""
        self.event_code=0x0000
        self.event_data=""
        self.event_response_code= 0x0000

        self.error_code = self.preload(TypesParser, MessageValidator, IncomingMsgFrame.get_event_code)


    @staticmethod
    def lock_packet(buff, typeParser):
        buff = bytes(buff)
        offset = 0
        packets = list()

        while True:
            start = buff.find('\x40\x40', offset)  # Identify start of packet
            if start == -1:
                return packets
            pack_l = typeParser.parse_u16(buff[start + 2: start + 4])

            if pack_l > len(buff):
                return packets

            end = buff.find('\x0d\x0a', offset + pack_l - 2)

            if start != -1 and end != -1:
                packets.append((start, end + 2))
                offset += (end + 2)
            else:
                packets.append((0, 0))
                offset += (start + 2)

    @staticmethod
    def get_unit_id(buff):
        return str(buff[4: 16])

    @staticmethod
    def get_event_type(buff, typeParser):
        return typeParser.parse_u16(buff[16:18])
    
    @staticmethod
    def get_event_code(buff, typeParser):
        return typeParser.parse_u16(buff[16:18])
    

    def preload(self, typeParser, mv, get_event_code):
        
        package_length = typeParser.parse_u16(self.msg[2: 4])

        crc_sum = typeParser.parse_u16(self.msg[package_length - 4: package_length - 2])
 
        if mv.msg_crc_is_good(self.msg[0: package_length - 4], crc_sum, mv.crc_calculate):
        
            if mv.msg_head_is_good(self.msg[0: 2]):
            
                if mv.msg_len_is_good(len(self.msg), package_length):

                    self.unit_id = self.msg[4: 16]
                    self.event_code = get_event_code(self.msg, typeParser)
                    self.event_data= self.msg[18: package_length - 4]

                    if not mv.msg_tail_is_good(self.msg[package_length-2: package_length]):
                        return 1
                else:
                    return 2
            else:
                return 3
        else:
            return 4
        return 0

