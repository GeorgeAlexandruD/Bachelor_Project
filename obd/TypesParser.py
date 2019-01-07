import struct
import datetime
import Logging as log


class TypesParser:

    @staticmethod
    def parse_u16(barray):
        try:
            return struct.unpack('<H', barray)[0] 
        except Exception as e:
            log.warn_logger(e)
            return None

            
    @staticmethod
    def parse_u8(barray): 
        try:
            return struct.unpack('B', barray)[0]
        except Exception as e:
            log.warn_logger(e)
            return None
            
    @staticmethod
    def parse_u32(barray):
        try:
            return struct.unpack('<I', barray)[0]
        except Exception as e:
            log.warn_logger(e)
            return None
        

    @staticmethod
    def parse_s16(barray):
        try:
            return struct.unpack('<h', barray)[0]
        except Exception as e:
            log.warn_logger(e)
            return None
        

    @staticmethod
    def parse_utc_time(barray, typeParser):
        try:
           return datetime.datetime(2000 + typeParser.parse_u8(bytearray([barray[2]])),  # Year
                          typeParser.parse_u8(bytearray([barray[1]])),  # Month
                          typeParser.parse_u8(bytearray([barray[0]])),  # Day
                          typeParser.parse_u8(bytearray([barray[3]])),  # Hour
                          typeParser.parse_u8(bytearray([barray[4]])),  # Minute
                          typeParser.parse_u8(bytearray([barray[5]])),  # Second
                          0,  # Milisecs
                          None)    
        except Exception as e:
            log.warn_logger(e)
            return None
        
    
    @staticmethod
    def parse_gps_info(barray, typeParser):

        gps_data = dict()
        try:
            # UTC timestamp
            gps_data['utc_time'] = typeParser.parse_utc_time(barray[0:6], typeParser).isoformat()  # Parse utc_time in ISO format

            # Process status bitfields
            # LSB implementation
            gps_data['fix'] = ((barray[6] & 0x03) != 0)  # Get fix - 00 - not fixed 01/11 fixed
            gps_data['lat_dir'] = 'N' if(((barray[6] >> 2) & 0x01) == 1) else 'S'  # Latitude direction
            gps_data['lng_dir'] = 'E' if(((barray[6] >> 3) & 0x01) == 1) else 'W'  # Longitude direction

            # Latitude
            gps_data['lat'] = float(typeParser.parse_u32(barray[7:11])) / 3600000.0
            gps_data['lat'] = gps_data['lat'] if(gps_data['lat_dir'] == 'N') else (- gps_data['lat'])

            # Longitude
            gps_data['lng'] = float(typeParser.parse_u32(barray[11:15])) / 3600000.0
            gps_data['lng'] = gps_data['lng'] if (gps_data['lng_dir'] == 'E') else (- gps_data['lng'])

            # Speed
            gps_data['speed'] = float(typeParser.parse_u16(barray[15:17])) / 100.0    # Speed in m/s

            # Course
            gps_data['course'] = float(typeParser.parse_u16(barray[17:19])) / 10.0  # Heading in degrees 0 - 359.9

            # Altitude
            gps_data['altitude'] = float(typeParser.parse_s16(barray[19:21])) / 10.0  # Altitude in meters

            return gps_data
        
        except Exception as e:
            log.warn_logger(e)
            return None
        

    @staticmethod
    def pack_u16(val):
        try:
            return struct.pack('<H', val)
        except Exception as e:
            log.warn_logger(e)
            return None
        

    @staticmethod
    def pack( unit_id, event_code, typeParser, mv, event_data= ''):
        try:
            packet = ''
            packet += '\x40\x40'
            
            packet += typeParser.pack_u16(22 + len(event_data))

            packet += unit_id.ljust(12,'\x00')

            packet += typeParser.pack_u16(event_code)

            packet += event_data

            packet += typeParser.pack_u16(mv.crc_calculate(packet))

            packet += '\x0d\x0a'

            return packet 
        except Exception as e:
            log.warn_logger(e)
            return None
        
