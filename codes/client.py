import socket
import sys
IP = '47.98.42.12'
port = 10002
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    client.connect((IP,port))
except Exception as e:
    print('server not find')
    sys.exit()
while True:
    message = input('send:')
    client.send(message.encode())
client.close()
