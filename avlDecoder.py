import binascii
import datetime
import math
from pprint import pprint

from IO_decoder import IODecoder

io  = IODecoder()
class avlDecoder():
    def __init__(self):
        self.raw_data = ""
        self.initVars()

    def initVars(self):            # initilizing variables
        self.codecid        = 0
        self.no_records_i   = 0
        self.no_records_e   = 0
        self.crc_16         = 0
        self.avl_entries    = []
        self.avl_latest     = ""
        self.d_time_unix    = 0 
        self.d_time_local   = ""
        self.avl_io_raw     = ""
        self.priority       = 0
        self.lon            = 0
        self.lat            = 0
        self.alt            = 0
        self.angle          = 0
        self.satellites     = 0
        self.speed          = 0
        self.decoded_io     = {}

    def decodeAVL(self, data):
        self.raw_data      = data
        self.data_field_l  = int(data[8:16],16)*2                                # Data Field Length – size is calculated starting from Codec ID to Number of Data 2.
        print(f"Data field length: {self.data_field_l}")
        self.total_io_size = self.data_field_l-4-2                               #-4=> subtract codecid and no of data, -2=> no of data at the end.
        self.io_end        = 20+self.total_io_size                               # 20=> start from timestamp
        self.codecid       = int(data[16:18], 16)                                # codecid
        self.no_record_i   = int(data[18:20], 16)                                # first no of total records
        self.no_record_e   = int(data[-10:-8], 16)                               # no of total records before crc-16 check
        self.crc_16        = int(data[-8:],16)                                   # crc-16 check
        self.first_io_start= 20                                                  # first io starting pos
        self.first_io_end  = math.ceil(self.total_io_size/ self.no_record_e)     # end pos for first io entry
        

        if(self.codecid == 8 and (self.no_record_i == self.no_record_e)):
            # record_entries     = data[20:-10]                                    # entry data
            record_entries = data[self.first_io_start: self.io_end ]               # entry data

            print(f"Found {self.no_record_i} records")

            start = 0
            count = 0
            while start < len(record_entries)-1 and count < self.no_record_i:
                print(f"Fetching record no {count +1 }")
                data = {}
                
                data['d_time_unix']  = int(record_entries[start:start+16], 16)
                data['d_time_local'] = self.unixtoLocal(data['d_time_unix'])
                data['priority'] = int(record_entries[start+16:start+18], 16)
                data['lon']          = int(record_entries[start+18:start+26], 16)
                data['lat']          = int(record_entries[start+26:start+34], 16)
                data['alt']          = int(record_entries[start+34:start+38], 16)
                data['angle']        = int(record_entries[start+38:start+42], 16)
                data['satellites']   = int(record_entries[start+42:start+44], 16)
                data['speed']        = int(record_entries[start+44:start+48], 16)
        
                data['io'], io_l   = io.dataDecoder(record_entries[start+48:])

                start = start + io_l+48
                count = count + 1

                pprint(data)
                        
            return self.getAvlData()
        else:
            return -1
 
    def getDateTime(self):                                                         # system time
        return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def unixtoLocal(self, unix_time):                                              # unix to local time
        time = datetime.datetime.fromtimestamp(unix_time/1000)
        return f"{time:%Y-%m-%d %H:%M:%S}"
        
    def getAvlData(self):
        data = {
            "sys_time"   : self.getDateTime(),
            "codecid"    : self.codecid,
            "no_record_i": self.no_record_i,
            "no_record_e": self.no_record_e,
            "crc-16"     : self.crc_16,
            # "avl_entries": self.avl_entries,
            # "avl_latest" : self.avl_latest,
            "d_time_unix" : self.d_time_unix,
            "d_time_local": self.d_time_local,
            "priority"    :self.priority,  
            "lon"         :self.lon,
            "lat"         :self.lat,
            "alt"         :self.alt,       
            "angle"       :self.angle,     
            "satellites"  :self.satellites,
            "speed"       :self.speed,
            "io_data"     :self.decoded_io    
        }
        return data

    def getRawData(self):
        return self.raw_data


if __name__ == "__main__":
    data = b'00000000000004d2081d00000176ccb789480000000000000000000000000000000000060301000200b40002422dea430f150148000000000000000176ccb69ee80000000000000000000000000000000000060301000200b40002422de8430f150148000000000000000176ccb5b4880000000000000000000000000000000000060301000200b40002422de6430f160148000000000000000176ccb4ca280000000000000000000000000000000000060301000200b40002422de6430f130148000000000000000176ccb3dfc80000000000000000000000000000000000060301000200b40002422de6430f160148000000000000000176ccb2f5680000000000000000000000000000000000060301000200b40002422de6430f110148000000000000000176ccb20b080000000000000000000000000000000000060301000200b40002422de4430f110148000000000000000176cc96f1880000000000000000000000000000000000040301000200b400000148000000000000000176cc9607280000000000000000000000000000000000040301000200b400000148000000000000000176cc951cc80000000000000000000000000000000000040301000200b400000148000000000000000176cc9432680000000000000000000000000000000000040301000200b400000148000000000000000176cc9348080000000000000000000000000000000000040301000200b400000148000000000000000176cc925da80000000000000000000000000000000000040301000200b400000148000000000000000176cc9173480000000000000000000000000000000000040301000200b400000148000000000000000176cc900be80000000000000000000000000000000000040301000200b400000148000000000000000176cc8f96b80000000000000000000000000000000000040301000200b400000148000000000000000176cc8eac580000000000000000000000000000000000040301000200b400000148000000000000000176cc8d4cc80200000000000000000000000000000002040301000200b400000148000000000000000176cc8d06780000000000000000000000000000000000040301000200b400000148000000000000000176cc8c1c180000000000000000000000000000000000040301000200b400000148000000000000000176cc8b31b80000000000000000000000000000000000040301000200b400000148000000000000000176cc8a47580000000000000000000000000000000000040301000200b400000148000000000000000176cc895cf80000000000000000000000000000000000040301000200b400000148000000000000000176cc8872980000000000000000000000000000000000040301000200b400000148000000000000000176cc8788380000000000000000000000000000000000040301000200b400000148000000000000000176cc869dd80000000000000000000000000000000000040301000200b400000148000000000000000176cc85b3780000000000000000000000000000000000040301000200b400000148000000000000000176cc84c9180000000000000000000000000000000000040301000200b400000148000000000000000176cc83deb80000000000000000000000000000000000040301000200b40000014800000000001d000027ca'
    # data = b'000000000000003608010000016B40D8EA30010000000000000000000000000000000105021503010101425E0F01F10000601A014E0000000000000000010000C7CF'
    # data = b'000000000000004308020000016B40D57B480100000000000000000000000000000001010101000000000000016B40D5C198010000000000000000000000000000000101010101000000020000252C'
    avl = avlDecoder()
    res = avl.decodeAVL(data)
    print(res)
    # avldata = avl.getAvlData()
    # print(avldata)


