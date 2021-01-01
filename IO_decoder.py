from avlMatcher import avlController
avl = avlController()
class IODecoder():
    def __init__(self, data):
        self.IO_data = data
        self.Ns_data = self.dataDecoder(self.IO_data)

    def ioDecoderN1(self, N1s, N1s_size):
        # print('n1s', N1s)
        temp       = {}
        for i in range(0,  N1s_size, 4):
            id  = int(N1s[i:i+2], 16)
            val = int(N1s[i+2:i+4], 16)
            temp[int(id)] = val
        return temp

    def ioDecoderN2(self, N2s, N2_size):
        # print("n2s", N2s)
        temp = {}
        for i in range(0, N2_size, 6):
            id  = int(N2s[i:i+2], 16)
            val = int(N2s[i+2: i+2+4], 16)
            temp[int(id)] = val
        return temp

    def ioDecoderN4(self, N4s, N4_size):
        temp = {}
        for i in range (0, N4_size, 10):
            id  = int(N4s[i:i+2], 16)
            val = int(N4s[i+2: i+10], 16)
            temp[int(id)] = val
        print("temp", temp)
        return temp

    def dataDecoder(self, n_data):
        Ns_data    = {}
        eventIO_ID = int(n_data[0:2], 16)
        N_Tot_io   = int(n_data[2:4], 16)

        n_N1       = int(n_data[4:6], 16)                   # number of n1's
        N1s_size   = n_N1 * (2 + 2)                         # n1 size
        N1s        = n_data[6:6+N1s_size]                   # n1 raw data
        N1_data    = self.ioDecoderN1(N1s, N1s_size)
        Ns_data['n1'] = N1_data                             # final N1 converted

        if(n_N1 == N_Tot_io):                               # N1 Break check
            print("breaking @ N1")
            return Ns_data

        N2_start   = 6+N1s_size                             # n2 start location
        n_N2       = int(n_data[N2_start:N2_start+2], 16)   # number of n2's
        N2s_size   = n_N2 * (2 + 4)                         # n2 size
        N2_end     = N2_start+2+N2s_size                    # n2 end location
        N2s        = n_data[N2_start+2: N2_end]             # n2 raw data
        N2_data    = self.ioDecoderN2(N2s, N2s_size)
        Ns_data['n2'] = N2_data                             # final N2 converted

        if(n_N1 + n_N2 == N_Tot_io):                        # N2 Break check
            print("breaking @ N2")
            return Ns_data

        N4_start   = N2_end                                 # n4 start location
        n_N4       = int(n_data[N4_start:N4_start+2], 16)   # number of n4's
        N4s_size   = n_N4 * (2 + 8)                         # n4 size
        N4_end     = N4_start + 2 + N4s_size                # n4 end location
        N4s        = n_data[N4_start+2: N4_end]             # n4 raw data
        N4_data    = self.ioDecoderN4(N4s, N4s_size)
        Ns_data['n4'] = N4_data                             # final N4 converted

        if(n_N1 + n_N2 + n_N4 == N_Tot_io):                 # N4 Break check
            print("breaking @ N4")
            return Ns_data
        

        print(Ns_data)


        

    def getNSData(self):
        return self.Ns_data



if __name__ == '__main__':
    n_data = "0009080100020103000400b301b401320033000148011d0000"
    n_data = "0105021503010101425E0F01F10000601A014E0000000000000000"
    # data = dataDecoder(n_data)
    # print(data)

    d = IODecoder(n_data)
    print(d.getNSData())