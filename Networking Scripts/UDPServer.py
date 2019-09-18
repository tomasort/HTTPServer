#this UDP server is used for assignment 2
import socket
import random

serverPort = 12900
serverName = ''

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((serverName, serverPort))
while True: 
	print "Waiting for connections"
	randomNum = random.randint(0, 10)
	message, addr = serverSocket.recvfrom(2048)
	print message, addr
	message = message.upper()
	if randomNum > 6:
		serverSocket.sendto(message, addr)
	#else we don't respond 
serverSocket.close()

