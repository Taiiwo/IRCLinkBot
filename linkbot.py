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
import socket, sys, re, urllib2, urllib, time
import os, random, subprocess, plugins, util
import thread, json
from plugins import *
from BeautifulSoup import BeautifulSoup

#Settings:
channels = ["##426699k", "#33012013"]
server = "irc.freenode.net"
port = 6667 #6667 is the default irc port
nick = "TaiiwoBot"
user = "Taiiwo"
admins = ['taiiwo','trollstrich', 'surtri']
channelops = [
		{
			"channel":"#33012013",
			"user":"Taiiwo"
		},
		{
			"channel":"##426699k",
			"user":"Taiiwo"
		},
		{
			"channel":"#33012013",
			"user":"Surtri"
		},
		{
			"channel":"##426699k",
			"user":"Surtri"
		}

	]
loginmessage = "-- LinkBot v3.0 ONLINE --" #Leave blank for no message
recvbits = 512 #How many bits to wait for. This affects the max length of links.
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
print "[-]Joining channels..."
for channel in channels:
	s.send('join ' + channel + '\r\n')
	#Sending login message
	s.send('privmsg ' + channel + ' :' + loginmessage + "\n\r")
time.sleep(1)
#setting variables
recv = ""
loop = 0
plugclass = plugins('')
#input("Logged in yet?")
def runplugins():# This is for threading
	for plugin in plugins.__dict__.values():
		message = None
        	try:
        	        message = plugin(plugclass, data)
        	except Exception , err:
        	        errormsg = sys.exc_info()[1]
			if errormsg != None:
				print errormsg
        	print message
        	if message != '' and message != None:
        	        for msg in message.split('\n'):
				s.send(str(msg))
				time.sleep(0.1)

#### Begin loop ####
while loop >= 0:
	loop = loop + 1
	print loop #print the number of times the script has looped
	time.sleep(0.05)#space out the loop so as not to run too fast
	print recv #prints everything received from freenode. Remove this to clean up the debugging
	#iterate through plugins executing all functions
	data = {'admins' : admins,
		's': s ,'recv': recv ,
		'nick':nick,
		'loop': loop ,'numr' : numr ,
		'channel' : channel,
		'channelops':channelops,
		'plugclass' : plugclass}# format data to send to plugins
	thread.start_new_thread(runplugins,())
	if '!update' in recv and util.argv('!update',recv)['user'] in data['admins']:
        	status = 'Successful'
                try:
                	execfile('./plugins.py')
                        from plugins import *
                       	execfile('./util.py')
                except Exception, err:
                        print sys.exc_info()[1]
                        status = 'Failed'
                args = argv('!update', data['recv'])
                s.send(util.say(args['channel'],'Dynamic update: ' + status))
	#get recv last. I thought this would be a good idea. I can't remember why, but there was a reason.
	recv = s.recv(recvbits)	
