import socket, os, ssl
from datetime import datetime
#use with urls like: 
#https://users.cs.fiu.edu/~downeyt/cnt4713/scripts/MailClientGoogle.py

def parseHeaders(message):
	lines = message.split('\r\n')
	result = []
	for w in lines: 
		temp = w.split(': ')
		if len(temp) == 2: 
			result.append((temp[0], temp[1]))
	return dict(result)
	
def createPath(path):
	result = []
	for p in folders: 
		if '~' in p: p = p.replace("~", "")
		if '.' in p: continue
		if len(p) > 0: 
			result.append(p + "/")
        pathToDir = []
        for dir in result:
		pathToDir.append(dir)
                if not os.path.exists(dir):
                        #make the directory
                        os.makedirs(dir)
                else: 
                        print "The directory ", dir, " Already exists"
                os.chdir(dir)

def checkFile(fileName): 
	if os.path.isfile(fileName):
		#then get the modified date
		return (getModfiedDate(fileName), True)
	else: 
		return ("", False)
	
def getContent(message): 
	return message.split("\r\n\r\n")[1]

def getServerName(url): 
	name = url.split('//')[1].partition('/')[0]
	return name

def getHostName(serverName):
	host = serverName.split("www.")[0]
	return host

def getModfiedDate(fileName): 
	try: 
		mtime = os.stat(fileName).st_mtime
	except OSError: 
		mtime = 0
	lastModifiedDate = datetime.fromtimestamp(mtime)
	lastModTime = lastModifiedDate.strftime("%a, %d %b %Y %H:%M:%S %ZGMT")
	return lastModTime

def getPath(message):
	x = message.split('//')[1]
	hostName = x.split('/')[0]
	path = x.split(hostName)[1]
	return path	

def getStatus(message): 
	status = message.split('\r\n')[0]
	return status.split()[1]

def sendFile(client, fileName):
	response = ""
	lastModified = "Last-Modified: %s\r\n" %getModfiedDate(fileName)
	httpStatus = "HTTP/1.1 200 OK\r\n"
	file = open(fileName, "rt")
	text = file.read()
	response = httpStatus + lastModified + "\r\n" + text + "\r\n"
	client.send(response)
	

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverPort1 = 10191
serverName = ""
serverPort2 = 80

serverSocket.bind(('', serverPort1))
serverSocket.listen(1)
print "Interrupt with CTRL-C"
while True: 
	try: 
		print "\n\nReady to serve..."
		connectionSocket, addr = serverSocket.accept()
		print "Connetcion from %s port %s" % addr
		message = connectionSocket.recv(2048)
		print "Original message from the client is: \n", message
		headers = parseHeaders(message)
		serverName = getServerName(message)	
		hostName = getHostName(serverName)
		if ('youtube' in message) or ('bing' in message): 
			print "Can't access youtube or bing sorry"
			connectionSocket.send("Sorry but you can't access youtube or bing")
			connectionSocket.close()
			continue
		httpMessage = "GET %s HTTP/1.1\r\nHost: %s\r\n" %(message, hostName)
		#now try to connect to the server that is specified in the url
		clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#if it is https we need to wrap it using ssl 
		#clientSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_TLSv1)
		#if it is not then we can connect using regular sockets 
		clientSocket.connect((serverName, serverPort2))
		path = getPath(message)
		folders = path.split('/')
		fileName = ""
		if '.' in (folders[len(folders) - 1]):
			fileName = folders[len(folders) - 1]
		#we must check if we have the file in memory
		createPath(path)
		#after createPath, the current directory is the path of the file 
		mdate, fileExists = checkFile(fileName)
		if fileExists: 
			ifModifiedSince = "If-modified-since: %s\r\n" %mdate
			httpMessage = httpMessage + ifModifiedSince + "\r\n"
		else: 
			httpMessage = httpMessage + "\r\n"
		clientSocket.send(httpMessage)
		total_data = []
		while True: 
			data = clientSocket.recv(8192)
			if len(data) < 8192:
				total_data.append(data) 
				break 
			total_data.append(data)
		messageFromOrigin = ''.join(total_data)	
		print messageFromOrigin
		clientSocket.close()
		headersFromOrigin = parseHeaders(messageFromOrigin)
		status = getStatus(messageFromOrigin)
		if status == "200": 
			#first save the file and then send the message
			#saveFile
			file = open(fileName, "w+")
        		file.write(getContent(messageFromOrigin))
			connectionSocket.send(messageFromOrigin)
		elif status == "304":
			#send the cached version 
			sendFile(connectionSocket, fileName)	
		os.chdir("/a/buffalo.cs.fiu.edu./disk/jccl-002/homes/torte007/CNT4713")
		connectionSocket.close()
	except KeyboardInterrupt: 
		print "\n===========Interrupted by CRTL-C===========\n"
		break
serverSocket.close()
