#!/usr/bin/python

""" Simple Web server that can handle cookies """
import random 
import socket
import os
from datetime import datetime 

class Server:
    def __init__(self, port=2024):
        self.serverPort = port
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cookies = {}
        self.colorCookies = ['Blue', 'Red', 'Pink', 'White', 'Yellow', 'Black']

    def parseHeaders(self, message): 
        lines = []
        for w in lines: 
            temp = w.split(': ')
            if len(temp) == 2: 
                result.append((temp[0], temp[1]))
        return dict(result) 

    def getModifiedDate(self, fileName): 
        try: 
            mtime = os.stat(fileName).st_mtime
        except OSError: 
            mtime = 0
        lastModifiedDate = datetime.fromtimestamp(mtime)
        lastModTime = lastModifiedDate.strftime("%a, %d, %b %Y %H: %M: %S %ZGMT")
        return lastModTime

    def checkLanguages(self, langs, fileName): 
        ListOfLangs = langs.split(',') # We only care about the first language present
        res = (False, "")
        for l in ListOfLangs: 
            if len(l) > 3: 
                x = l.split(';')[0]
            else: 
                x = l
            if os.path.isfile(fileName + "." + x): 
                res = (True, x) 
                break 
            else: 
                continue
        return res 

    def sendFile(self, client, fileName, message): 
        modified = True
        response = "" # The HTTP Response 
        last_modified = "Last-Modified: %s\r\n" % getModifiedData(fileName) 
        # Set a random cookie 
        while True: 
            userID = random.randint(1, 100)
            if not(userID in self.cookies): 
                self.cookies.update({userID: (self.colorCookie[random.randint(0, 5)] + str(random.random))})
                break 
        
        headers = pareseHeaders(message)
        listCookies = headers['Cookies'].split(';')
        cookieDict = {}
        for c in listCookies: 
            # we only want the userID and ColorID cookies and we don't care about the rest of the cookies
            if len(c.split('=')) == 2: 
                c = c.strip() # Be careful with spaces 
                name, value = c.split('=')
                cookieDict.update({name: value})
        if 'Accept-Language' in headers: 
            # Now we need to find the file in the language that is specified in headers['Accept-language']
            fileFound, lang = self.checkLanguages(headers['Accept-Language'], fileName)
            if fileFound: 
                fileName = fileName + "." + lang # Assuming that the file ends in the language that it is in 
        httpStatus = "HTTP/1.1 200 OK\r\n"
        file = open(fileName, "rt")
        text = file.read()
        cookie1 = ''
        cookie2 = ''
        # Look for the cookies 
        if 'UserId' in cookieDict and 'colorId' in cookieDict: 
            text = processInput(text, cookieDict['UserId'], cookieDict['colorId'], listCookies)
        else: 
            text = processInput(text, "No ID cookies yet", "No color Cookie yet", "No ohter cookies")
            # If we don't receive any cookies then send some cookies
            cookie1 = "Set-Cookie: UserId=" + str(userID) + "\r\n"
            cookie2 = "Set-Cookie: colorId=" + cookies[UserID] + "\r\n"
        if 'If-Modified-Since' in headers: 
            if headers['If-Modifed-Since'] == self.getModifiedDate(fileName): 
                modified = False
                httpStatus = "HTTP/1.1 304 Not Modified\r\n"
        response = httpStatus + last_modified + cookie1 + cookie2 + "\r\n"
        # The server has to send the file regardless if modified or not
        if True: 
            response = response + text + "\r\n"
        client.send(response)

    def processInput(self, text, userid, colorid, othercookies):
        return text.format(**locals())

    def run(self):
        self.serverSocket.bind(('', self.serverPort))
        self.serverSocket.listen(1)
        print "Interrupt with CTRL-C"
        while True: 
            try: 
                print "\n\nReady to serve..."
                connectionSocket, addr = self.serverSocket.accept()
                message = connectionSocket.recv(4096)
                print "The message from the client is: \n"
                print message
                filename = message.split()[1].partition("/")[2]
                self.sendFile(connectionSocket, filename, message)
                connectionSocket.close()
            except IOError:
                print "Not found %s" % filename
                sendError(connectionSocket, "404", "Not Found")
            except KeyboardInterrupt:
                print "Keyboard interrupted by CTRL-C"
                break 
        self.serverSocket.close()

if __name__ == "__main__":
    server = Server(port=2024)
    server.run()

        
            