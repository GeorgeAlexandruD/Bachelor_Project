from IncomingMsgFrame import IncomingMsgFrame
from MsgAlarm import MsgAlarm
import json
from RabbitMQBinding import RabbitMQBinding


class MsgHandler:

    def __init__(self):
        self.unit_id= ""
        self.IncomingMsgFrame = IncomingMsgFrame
        self.rb_mq = RabbitMQBinding()

    def lock_packet(self,buff):
        return self.IncomingMsgFrame.lock_packet(buff)


    def publish(self, unit_id, data):
        self.rb_mq.publish(unit_id + '.' + data['packet_type'], json.dumps(data))
    
    def get_unit_id(self, buff):
        return self.IncomingMsgFrame.get_unit_id(buff)

    def process(self,unit_id, buff):
        message_type = IncomingMsgFrame.get_event_type(buff)
        
        if len(self.unit_id) == 0:
            self.unit_id= unit_id
        elif self.unit_id != unit_id:
             raise Exception('Not the correct device handler. Expected: ' + self.unit_id + ' Incoming: ' + unit_id)

        if message_type== 0x2003:
            msg = MsgAlarm(buff)
            if msg.error_code != 0:
                raise Exception('error code'+ msg.error_code)
                #todo log
            else:
                res = msg.to_dict()
                self.publish(self.unit_id, res)
                return msg.generate_response()
