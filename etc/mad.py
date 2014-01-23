import time, re, socket
threshold = 30 
nick = 'TaiiwoTracker'
srv = "irc.freenode.net"
port = 6667
chan = "#33012014"
logging = 1
print '----------------'
print '-Python IRC Bot-'
print '------v0.1------'
print '----------------'
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((srv,port))	#Connect to IRC Server
s.send('NICK %s\r\n'%(nick))
s.send('USER 8 * ' + nick + ' my name\r\n')
s.send('JOIN %s\r\n'%(chan))	#Join IRC Server
f = open("logg.txt","a")
while 1: #While Connection is Active
    data = s.recv(1024)
    print data
    f.write(data)
    if 'PING' in data:
        s.send('PONG ' + data.split(' ')[1] + '\r\n')
    if 'any news' in data:
	s.send('PRIVMSG %s :Read the wiki for news !uc recent\r\n'%chan)
