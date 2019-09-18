#UDP client 
import socket
import time

serverName = 'localhost'
serverPort = 12900
#we create a socket object with SOCK_DGRAM because it is UDP
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#We don't want to wait too long so we set a timeout
clientSocket.settimeout(1)
message = raw_input('Inout lowercase sentence: ')
try:
  #record the time when we send the message to the server 
	startTime = time.time()
	clientSocket.sendto(message, (serverName, serverPort))
	modifiedMessage, serverAddr = clientSocket.recvfrom(2048)
  #now record the time when we receive the message
	finalTime = time.time()
except timeout:
	print "Connection timeout"

print modifiedMessage, serverAddr, 
#the round trip time is finalTime - startTime
rtt = finalTime - startTime
print "RTT = %f" % rtt
clientSocket.close()
