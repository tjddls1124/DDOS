# Import socket module
import socket

ip = '127.0.0.1'
# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 12345

# connect to the server on local computer
s.connect((ip, port))

# receive data from the server
print( s.recv(1024))
# close the connection
s.send('123'.encode())

s.close()
