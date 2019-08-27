import socket
import sys

#  https://github.com/remzmike/python-kports-portscanner/blob/master/kports.py 참고할것
# https://github.com/phillips321/python-portscanner/blob/master/nmap.py
'''
PORT      STATE    SERVICE
80/udp    closed   http
443/udp   open     https
997/udp   filtered maitrd
998/udp   filtered puparp
999/udp   filtered applix
2002/udp  filtered globe
33459/udp closed   unknown
'''

def checkUdp(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        s.sendto("test".encode(), (ip, port))
        recv, svr= s.recvfrom(255)
    except socket.timeout:
        try:
            print('0')
        except ValueError:
            print ("UDP Port {}: Open".format(port))
        else:
            print ("UDP Port {}: Close".format(port))

    s.close()

    # if result == 0:
    #     print("UDP Port {}: Open".format(port))
    return 0

def checkTcp(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = s.connect_ex((ip, port))
    except socket.gaierror:
        s.close()
        return 1

    s.close()

    if result == 0 :
        print ("TCP Port {}: Open".format(port))

    return result


if __name__ == "__main__":
    for i in range(1, 1024):
        checkUdp('192.168.0.1', i)
