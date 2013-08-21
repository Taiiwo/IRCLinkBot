#Taiiwo's LinkBot v2.1.5
#Features:
##Doesn't post titles to the same link twice, so you can't DOS it.
##Pongs all ping requests so should run indefinitely
##
#GPL v2
#Note: You need to install BeautifulSoup. sudo apt-get install python-BeautifulSoup
import socket, sys, re, urllib2, time, os, random
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
def html_decode(s):
	htmlCodes = (("'", '&#39;'),('"', '&quot;'),('>', '&gt;'),('<', '&lt;'),('&', '&amp;'))
	for code in htmlCodes:
		s = s.replace(code[1], code[0])
	return s
def randomnum(low,high):
	random.randint(low,high)
def textbetween(str1,str2,text):
	posstr1 = re.search(r"[^a-zA-Z](" + str1 + ")[^a-zA-Z]", text).start(1)
	posstr2 = re.search(r"[^a-zA-Z](" + str2 + ")[^a-zA-Z]", text).start(1)
	between = text[posstr1 + len(str1):posstr2]
	return between
def command(command): #finds the argument for a command.
	if command + " " in recv:
		match = re.search(r"[^a-zA-Z](" + command + ")[^a-zA-Z]", recv)
		num = match.start(1)
		message = recv[num + len(command):]
		if message == '':
			return 'no word'
		else:
			return str(message[1:])
	else:
		message = "None"
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
	time.sleep(0.05)#space out the loop so as not to run too fast
	print recv #prints everything received from freenode. Remove this to clean up the debugging
	#check for ping
	pong(recv)
	#check for links
	error = 0
	message = command("!love")
	if str(message) != 'None':
		s.send('privmsg ' + channel + ' :I love ' + str(message) + '\r\n')
	message = command("!say")
	if str(message) != 'None':
		s.send('privmsg ' + channel + ' :' + str(message) + '\r\n')
	message = command("!rfl")
	if str(message) != 'None':
		s.send('privmsg ' + channel + ' :I really fucking love ' + str(message) + '\r\n')
	message = command("!fact")
	if str(message) != 'None':
		s.send('privmsg ' + channel + ' :' + textbetween("<strong>","</strong>", urllib2.urlopen("http://randomfunfacts.com").read())[3:-4] + '\r\n')
	message = command("!joke")
	if str(message) != 'None':
		s.send('privmsg ' + channel + ' :' + textbetween('<td style="color: #000000">','<td align="right width="95px">', urllib2.urlopen('http://www.sickipedia.org/joke/view/' + str(randomnum(61,1300))).read()[:-5]) + '\r\n')
	message = ""
	if "!wyr1" in recv:
		file = open("WYR.txt","r")
		text = file.read()
		lines = text.splitlines()
		s.send('privmsg ' + channel + ' :' + lines[int(random.randint(0,62))] + '\r\n')
	message = ""
	if "!wyr" in recv and "!wyr1" not in recv:
		error = 1
		while error == 1:
			try:
				s.send('PRIVMSG '+ channel +' :' + gettitle('http://www.rrrather.com/view/' + str(random.randint(0,40000)))+ '\r\n') 
				error = 0
			except:
				print '[Server Error (Not my fault)]'
				error = 1
	message = command('!roll')
        if str(message) != 'None':
		try:
			int(message)
			error = 0
		except:
			error = 1
		if error != 1 and len(message) <= 6:
			s.send('PRIVMSG '+ channel +' :' + str(random.randint(1,int(message))) + '\r\n')
	urlsfound = True
	try:
		link2 = link
		link = geturl(recv)
		print link
	except:
		print "[-]No URLS found"
		error = 1
		urlsfound = False
	#check for title
	if link2 != link:
		try:
			nlink = link[0]
			if nlink[-4:] == '.cgi' or nlink[-4:] == '.CGI':
				title = 'Get fucked'
			else:
				title = gettitle(nlink)
				title = title.splitlines()
				title = title[0]
			if len(title) >= 150:
				title = title[:150]
			title = html_decode(title)
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
	
