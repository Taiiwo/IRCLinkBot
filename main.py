import socket, urllib2, sys, json, os, thread, re, random, time
from util import *
class botApi:
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	loop = 0
	sending = 0
	def __init__(self):
		self.importConfig()
	def importConfig(self, submissive = False):
		while 1:
			try:
				configFile = open ('./linkbot.conf','rw')#	Import settings file
				self.config = json.loads( configFile.read() )#	Parse config file
				configFile.close()
				return self.config
				break
			except:
				if fails < 5:
					print "[E] Failed to read config, trying again..."
					fails += 1
				else:
					error = "[E] Failed to read config 5 times. Check file exists, named linkbot.conf, and syntax is correct."
					if submissive:
						print error
						return self.config
					else:
						raise Exception(error)
						break

	def connect(self):
		print "[-]Connecting to server..."
		while 1:
			try:
				self.s.connect(( self.config['settings']['host'] , int(self.config['settings']['port']))) #connect to server
				break
			except:
				print "[E]Could not connect to server, trying again..."
				time.sleep(5)
		time.sleep(0.2)
		# set nick
		self.s.send('nick ' + self.config['settings']['botNick'] + '\r\n')
		time.sleep(0.2)
		# set user
		self.s.send('user ' + self.config['settings']['botIdent'] + ' * ' + self.config['settings']['botUser'] + ' ' + self.config['settings']['botName'] + '\r\n')
		# authenticate
		if self.config['settings']['authenticate'] == 'True':
			try:
				passFile = open('pass','r')
				password = passFile.read()
				self.say('nickserv','identify ' + password)
			except:
				print "[E] Password not found. Continuing without authentication."
		while 1:
			recvData = self.recv()
			if self.config['settings']['printRecv'] == 'True':
				print recvData
			if ":You are now identified for" in recvData or self.config['settings']['authenticate'] != 'True':
				break
		for channel in self.config['settings']['joinChannels']:#	Join all the channels
			self.s.send('join ' + channel + '\r\n')
			time.sleep(0.5)
			self.say(channel, self.config['settings']['joinMessage'])
			
	def do(self):
		self.importConfig(submissive = True)#	Refresh the config file
		recvData = bot.recv()
		bot.runPlugins()
		bot.handlePing()
		
	def recv(self):
		bot.loop += 1
		recvLen = int(self.config['settings']['recvLen'])
		self.recvData = self.s.recv(recvLen)
		if self.config['settings']['printRecv'] == 'True':
			print self.recvData
		return self.recvData
		
	def say(self, target, message):
		# send multiple messages by splitting with \n
		# It is this way to help stop IRC injection
		retme = ""
		for msg in message.split('\n'):
			if msg and msg != '':
				if len(msg) > 430:
					# split into a group of messages 430 chars long
					msgs = [msg[i:i+430] for i in range(0, len(msg), 430)]
					for msg in msgs:
						retme += 'PRIVMSG ' + target + ' :' + msg + '\r\n'
				else:
					retme += ("PRIVMSG " + target + " :" + msg + "\r\n")
		self.s.send(retme)
		# I don't know why you'd want this, but better to return something than nothing.
		return retme

	def runPlugins(self):# run all plugins in threads
		self.indexPlugins()
		data = {'recv' : self.recvData,#	Format data to send to the plugins.	
			'config' : self.config,#	json object of config file
			'loop' : self.loop,#		number of messages received
			'api' : self }#		The bot object used to interface with IRC
		for pluginFolder in self.pluginList:
			thread.start_new_thread(self.pluginThread, (pluginFolder['nameList'], pluginFolder['path'], data))

	def indexPlugins(self):
		self.pluginList = []
		path = './plugins/'
		rootPlugins = os.listdir('./plugins/')# 	Get plugin filenames only from the plugins directory
							#	This runs the plugins no matter what.
		self.pluginList.append({"nameList" : rootPlugins, "path": path})#	Run the root plugins in a new thread

		# Check if the recv is a privmsg from a channel
		if not re.match('^:[^!]*![^@]*@[^\s]\s(PRIVMSG|privmsg)\s#[^:]*:.*', self.recvData) == None:
			#Run plugins from ./plugins/privmsg/*
			for root, subFolders, files in os.walk('./plugins/privmsg/',followlinks=True):#		Fetch plugins recurisively. This means
				self.pluginList.append({"nameList" : files, "path": root})#	you can organize plugins in subfolders however you'd like. eg. Have a folder
											#	full of entertainment plugins that you can easily disable by prepending '.' to the folder name.
		# If recv is a private message to the bot
		elif not re.match('^:[^!]*![^@]*@[^\s]\s(PRIVMSG|privmsg)\s' + self.config['settings']['botNick'] + ':.*', self.recvData) == None:
			# Run plugins from ./plugins/privmsgbot/*
			for root, subFolders, files in os.walk('./plugins/privmsgbot/',followlinks=True):
				self.pluginList.append({"nameList" : files, "path": root})
		
		# run plugins from the directory named 'root'
		for root, subFolders, files in os.walk('./plugins/root/',followlinks=True):
			self.pluginList.append({"nameList" : files, "path": root})

	def pluginThread(self, plugins, path, data):#	This function is for threading
		for plugin in plugins:
			self.runPlugin(plugin, path, data)

	def runPlugin(self, plugin, path, data):# runs a single plugin
		if plugin[-3:] == '.py' and plugin[0:2] != 'lib':
			pluginFile = open (path + '/' + plugin,'r')
			exec(pluginFile)
			pluginFile.close()
			args = argv(':', data['recv'])
			toSend = main(data)
			if args['channel'] in self.config['settings']['pluginIgnoreChannels']:
				if plugin in self.config['settings']['pluginIgnoreChannels'][args['channel']]:
					toSend = None
			if toSend and toSend != '' and toSend != None:
				while 1:
					# this is so the bot can only send 2 messages at a time
					# (Since we're threading), so as not to get us kicked for
					# excess flood
					if self.sending <= 2:
						self.sending += 1
						for send in toSend.split('\n'):
							try:
								self.s.send(send + '\n')
								time.sleep(float(self.config['settings']['messageTimeSpacing']))
							except Exception , err:
								self.sending -= 1
								errormsg = sys.exc_info()[1]
								if errormsg != None:
									print plugin + ' : ' + str(errormsg)
						self.sending -= 1
						break
					else:
						continue
				if self.config['settings']['printSend'] == 'True':
					print toSend

	def handlePing(self):
		for line in self.recvData.splitlines():
			if line[0:5] == 'PING ':
				self.s.send('PONG ' + self.recvData.split(' ')[1][1:] + '\r\n')
				if self.config['settings']['printSend'] == 'True':
					print 'PONG ' + self.recvData.split(' ')[1][1:] + '\r\n'
		'''	I was thinking about making the bot run plugins from a 'PING' folder,
			but saw very little point, other than possible data logging?. Regardless,
			I left it out.	'''
	
bot = botApi()
bot.connect()
while 1:
	bot.do()
	

