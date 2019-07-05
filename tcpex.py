import socket
import struct

class TCPPacket:
    def __init__(self, dport = 80, sport = 65535, dst = '127.0.0.1', src = '192.168.1.101', data = 'Nothing'):
        self.dport = dport
        self.sport = sport
        self.dst_ip = dst
        self.src_ip = src
        self.data = data
        self.raw = None
        self.create_tcp_feilds()

    def create_tcp_feilds(self):
        self.tcp_src = self.sport
        self.tcp_dst = self.dport
        self.tcp_seq = 0
        self.tcp_ack_seq = 0
        self.tcp_hdr_len = 80

        tcp_flags_rsv = (0 << 9)
        tcp_flags_noc = (0 << 8)
        tcp_flags_cwr = (0 << 7)
        tcp_flags_ecn = (0 << 6)
        tcp_flags_urg = (0 << 5)
        tcp_flags_ack = (0 << 4)
        tcp_flags_psh = (0 << 3)
        tcp_flags_rst = (0 << 2)
        tcp_flags_syn = (1 << 1)
        tcp_flags_fin = (0)

        self.tcp_flags = tcp_flags_rsv + tcp_flags_noc + tcp_flags_cwr + tcp_flags_ecn + tcp_flags_urg + tcp_flags_ack + tcp_flags_psh + tcp_flags_rst + tcp_flags_syn + tcp_flags_fin

        self.tcp_wdw = socket.htons(5840)

        self.tcp_chksum = 0

        self.tcp_urg_ptr = 0

        return


    def assemble_tcp_feilds(self):
        self.raw = struct.pack('!HHLLBBHHH',
            self.tcp_src,
            self.tcp_dst,
            self.tcp_seq,
            self.tcp_ack_seq,
            self.tcp_hdr_len,
            self.tcp_flags,
            self.tcp_wdw,
            self.tcp_chksum,
            self.tcp_urg_ptr
        )

        self.calculate_chksum()
        return

    def calculate_chksum(self):
        src_addr = socket.inet_aton(self.src_ip)
        dest_addr = socket.inet_aton(self.dst_ip)
        placeholder = 0
        protocol = socket.IPPROTO_TCP
        tcp_len = len(self.raw) + len(self.data)

        psh = struct.pack('!4s4sBBH',
            src_addr,
            dest_addr,
            placeholder,
            protocol,
            tcp_len
        )

        psh = str(psh) + str(self.raw) + self.data

        self.tcp_chksum = self.chksum(psh)

        self.reassemble_tcp_feilds()

        return

    def chksum(self, msg):
        s = 0

        for i in range(0, len(msg), 2):
            a = ord(msg[i])
            b = ord(msg[i+1])
            s = s + (a + (b << 8))

        s = s + (s >> 16)
        s = ~s & 0xffff
        return s

    def reassemble_tcp_feilds(self):
        self.raw = struct.pack('!HHLLBBH',
            self.tcp_src,
            self.tcp_dst,
            self.tcp_seq,
            self.tcp_ack_seq,
            self.tcp_hdr_len,
            self.tcp_flags,
            self.tcp_wdw
        ) + struct.pack("H", self.tcp_chksum) + struct.pack('!H', self.tcp_urg_ptr)

        return

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

    tcp = TCPPacket()
    tcp.assemble_tcp_feilds()

    s.sendto(tcp.raw, ('127.0.0.1' , 0 ))
