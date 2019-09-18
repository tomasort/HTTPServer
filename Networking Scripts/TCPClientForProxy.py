#TCPClient.py
#to test the proxy server 

from socket import socket, AF_INET, SOCK_STREAM
serverName = 'localhost'
serverPort = 2024
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
message = raw_input('Input a URL: ')
clientSocket.send(message)
a = []
while True:
        m = clientSocket.recv(2048)
        a.append(m)
        if not m: break
messageFromServer = ''.join(a)
print 'From Server: ', messageFromServer
clientSocket.close()
