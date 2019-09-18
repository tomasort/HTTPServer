#FTPClient.py

from socket import socket, AF_INET, SOCK_STREAM
from ast import literal_eval
import time

def send(socket, msg): 
	print "===>sending: " + msg
	socket.send(msg + "\r\n")
	recv = socket.recv(1024)
	print "<===receive: " + recv
	return recv

def parseHeaders(message):
        lines = message.split('\r\n')
        result = []
        for w in lines:
                temp = w.split(': ')
                if len(temp) == 2:
                        reuslt.append((temp[0], temp[1]))
        return dict(result)	

def download(fileName, clientSocket, dataSocket):
        message = send(clientSocket, "RETR " + fileName)
        message = dataSocket.recv(2048)
        return message

def getList(fileName, clientSocket, dataSocket):
        message = send(clientSocket, "CWD " + fileName)
        message = dataSocket.recv(2048)
        return message


serverName = 'ftp.swfwmd.state.fl.us'
serverPort = 21
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
condition = True
message = clientSocket.recv(2048)
print message
while condition:
	message = clientSocket.recv(2048)
	print message
	condition = message[0:6] != "220---"
message = send(clientSocket,"USER Anonymous")
message = send(clientSocket,"PASS torte007@fiu.edu")
message = send(clientSocket,"TYPE A")
message = send(clientSocket,"PASV")
start = message.find("(")
end  = message.find(")")
tuple = message[start+1:end].split(',')
print tuple
#build the port from the last two numbers
port = int(tuple[4])*256 + int(tuple[5])
print port
dataSocket = socket(AF_INET, SOCK_STREAM)
dataSocket.connect((serverName, port))

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverPort = 10191
while True:
        try:
                print"\n\nReady to serve..."
                connectionSocket, addr = serverSocket.accept()
                message = connectionSocket.recv(4096)
                print "====The message from the client===="
                print message
                filename = ""
                if message.split()[0] == "POST":
                        #then the filename is in the content of the message after "\r\n"
                        content = message.split("\r\n")[1]
                        print content
                        filename = content.split("=")[1]
                        print filename
                #now we have to find if it is a file or a directory
                #it is a file if it contains a "." and a directory if not
                if "." in filename:
                	fileFromServer = download(filename, clientSocket)
			print fileFromServer
			#and we need to find a way of sending this file to the browser 
		else: 
			#it is a directory 
			listFromServer = getList(filename, clientSocket)
			print listFromServer
			#and get the list to the browser 
			
        except KeyboardInterrupt:
                iprint "Keyboard interrupted by CTRL-C"
                break

dataSocket.close()
message = send(clientSocket,"QUIT")
clientSocket.close()
