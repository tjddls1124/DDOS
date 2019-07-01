import mySocket
import socket
import struct

if __name__=='__main__':
        # Create Raw Socket
 s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

 tcp = mySocket.TCPPacket()
 tcp.assemble_tcp_feilds()

 s.sendto(tcp.raw, ('127.0.0.1' , 0 ))
