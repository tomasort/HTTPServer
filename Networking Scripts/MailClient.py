#!/usr/bin/python  

import cgi, cgitb, socket, time, ssl, base64
#For some reason the cgi script does not work and gives a server error but as a python script it works fine
#As a python script it sends email

def send_recv(socket, msg, code):
    if msg != None:
        print "Sending==> ", msg 
        socket.send(msg + '\r\n')

    recv = socket.recv(1024)
    print "<==Received:\n", recv
    if recv[:3]!=code:
        print '%s reply not received from server.' % code
    return recv

def send(socket, msg):
    print "Sending ==> ", msg 
    socket.send(msg + '\r\n') 

#get the info from the form 
#form = cgi.FieldStorage()

destination = raw_input("To: ")
source = raw_input("From: ") 
subject = raw_input("Enter the subject: ")
message = raw_input("Enter a message: ")

serverName = 'smtp.gmail.com'
serverPort = 587 

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
recv = send_recv(clientSocket, None, '220')

clientName = 'Tomas'
userName, userServer  = source.split('@')
toName, toServer = destination.split('@')

#Send HELO command and print server response.
heloCommand='EHLO %s' % clientName
recvFrom = send_recv(clientSocket, heloCommand, '220')

#Send STARTTLS command and print server response. 
starttlscomand = 'STARTTLS'
recvFrom = send_recv(clientSocket, starttlscomand, '220')
scc = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)

#Ask for the username and password

username = raw_input("Username: ")
password = raw_input("Password: ")

authcomand = 'AUTH LOGIN'
recvFrom = send_recv(scc, authcomand, '334')
user = base64.b64encode(username)
recvFrom = send_recv(scc, user, '334')
passw = base64.b64encode(password)
recvFrom = send_recv(scc, passw, '334')

#Send HELO command and print server response.
heloCommand='EHLO %s' % clientName
recvFrom = send_recv(scc, heloCommand, '250')

#Send MAIL FROM command and print server response.
fromCommand='MAIL FROM: <%s@%s>' % (userName, userServer)
recvFrom = send_recv(scc, fromCommand, '250')

#Send RCPT TO command and print server response.
rcptCommand='RCPT TO: <%s@%s>' % (toName, toServer)
recvRcpt = send_recv(scc, rcptCommand, '250')

#Send DATA command and print server response.
dataCommand='DATA'
dataRcpt = send_recv(scc, dataCommand, '354')
#Send message data.
send(scc, "Date: %s" % time.strftime("%a, %d %b %Y %H:%M:%S -0400", time.localtime()));
send(scc, "From: %s <%s@%s>" % (clientName, userName, userServer));
send(scc, "Subject: %s" % subject);
send(scc, "To: %s@%s" % (toName, toServer));
send(scc, ""); #End of headers
send(scc, message);
#Message ends with a single period.
send_recv(scc, ".", '250');
#Send QUIT command and get server response.
quitCommand='QUIT'
quitRcpt = send_recv(scc, quitCommand, '221')
