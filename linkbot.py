#Taiiwo's LinkBot v3.0
#=======================
#Features:
#---------
##Doesn't post titles to the same link twice, so you can't DOS it.
##Pongs all ping requests so should run indefinitely
##Plugin system added for easy expansion
#
#---------------------------------------
#
#GPL v2
#------
#Note: You need to install BeautifulSoup. sudo apt-get install python-BeautifulSoup
#
#Importing Libraries
import socket, sys, re, urllib2, time, os, random
from util import *
from plugins import *
from BeautifulSoup import BeautifulSoup

#Settings:
channel = "#426699t"
server = "irc.freenode.net"
port = 6667 #6667 is the default irc port
nick = "TaiiwoBot"
user = "Taiiwo"
loginmessage = "-- LinkBot v3.0 ONLINE --" #Leave blank for no message
recvbits = 315 #How many bits to wait for. This affects the max length of links.
numr = 27 #Number of recvs to ignore on startup. This can be determined by running the script and checking when the
	#last title was send to the chat by the number printed in square brackets.
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
	#iterate through plugins executing the all
	data = {'s': s , 'recv': recv , 'loop': loop}
	for plugin in plugins.__dict__.values():
		try:
			plugin(data)
		except TypeError:
			pass
	#get recv last. I thought this would be a good idea. I can't remember why, but there was a reason.
	recv = s.recv(recvbits)	
