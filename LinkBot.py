#Taiiwo's LinkBot v2.1.5
#Features:
##Doesn't post titles to the same link twice, so you can't DOS it.
##Pongs all ping requests so should run indefinitely
##
#GPL v3
#Note: You need to install BeautifulSoup. sudo apt-get install python-BeautifulSoup
import socket, sys, re, urllib2, time
from BeautifulSoup import BeautifulSoup

#Settings:
channel = "#426699k"
server = "irc.freenode.net"
port = 6667 #6667 is the default irc port
nick = "TaiiwoBot"
user = "Taiiwo"
loginmessage = "-- LinkBot v2.1.5 ONLINE --" #Leave blank for no message
recvbits = 315 #How many bits to wait for. This affects the max length of links.
numr = 27 #Number of recvs to ignore on startup. This can be determined by running the script and checking when the
	#last title was send to the chat by the number printed in square brackets.

def gettitle(url):#get the page title of an URL
        soup = BeautifulSoup(urllib2.urlopen(url))
        return soup.title.string
def pong(recv):#respond to ping req in a string --Not perfect, but works
	if "ping" or "PING" in recv:
		url = str(geturl(str(recv)))
		if url != "":
			s.send("PONG " + url + "\n\r")
def geturl(recv):#parse an URL from a string
	return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', recv)
def maketiny(url):
	html = urllib2.urlopen("http://tinyurl.com/api-create.php?url=" + url)
	tiny = str(html.read())
	return tiny
#### Preparing for loop ####
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #making socket
print "[-]Connecting to server..."
try:
	s.connect((server,port)) #connect to server
except:
	print "[E]Could not connect to url. Please check and try again."
print "[-]Logging in..."
s.send('nick ' + nick + '\r\n')
time.sleep(1)
s.send('user 8 * ' + user + ' my name\r\n')
time.sleep(1)
print "[-]Joining channel..."
s.send('join ' + channel + '\r\n')
time.sleep(1)
print "Sending login message..."
s.send('privmsg ' + channel + ' :' + loginmessage + "\n\r")
time.sleep(1)
#setting variables
recv = ""
link = ""
link2 = ""
loop = 0
error = 0
nlink = ""
input("Logged in yet?")
#### Begin loop ####
while loop >= 0:
	loop = loop + 1
	print loop #print the number of times the script has looped
	time.sleep(0.2)#space out the loop so as not to run too fast
	print recv #prints everything received from freenode. Remove this to clean up the debugging
	#check for ping
	pong(recv)
	#check for links
	error = 0
	urlsfound = True
	try:
		link2 = link
		link = geturl(recv)
		print link
	except:
		print "[-]No URLS found"
		error = 1
		urlsfound = False
	#chack for title
	if link2 != link:
		try:
			nlink = link[0]
			title = gettitle(link[0])
			print title
		except:
			print "[E]No valid title"
			error = 2
		#post title to irc
		if error == 0  and loop >= numr:
			if len(nlink) >= 40:
				s.send('privmsg ' + channel + ' : ^ ' + str(title) + " " + maketiny(link[0]) + ' ^\n\r')
			else:
				s.send('privmsg ' + channel + ' : ^ ' + str(title) + " ^\r\n")
		if error == 2 and urlsfound == True and nlink != "" and loop >= numr and len(nlink) >= 40:
			s.send('privmsg ' + channel + ' : ^ ' + maketiny(nlink) + ' ^\r\n')
	#get recv last. I thought this would be a good idea. I can't remember why, but there was a reason.
	recv = s.recv(recvbits)
	nlink = ""
	
