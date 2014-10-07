#This file contains fuctions available for the plugin developers.
import socket, sys, re, urllib2, time, os, random, json
from BeautifulSoup import BeautifulSoup

def modeCheck(mode, data):
        args = argv('@', data['recv'])
        for user in data['config']['settings']['userModes']:
                if args['nick'] == user['nick'] and mode in user['modes']:
                        if user['channel'] == args['channel'] or 'g' in user['modes']:
                                return True
        return False

def saveConfigChanges(config):
	try:
		f = open('linkbot.conf','w')
		f.write(json.dumps(config, sort_keys=True, indent=4, separators=(',', ': ')))
		f.close()
	except:
		print "[E] Could not save to config file"

def say(channel, message):# A quick way to make the bot say something. Use return say(argv['channel'],message)
	if len(message) > 430:
		messages = [message[i:i+430] for i in range(0, len(message), 430)]
		retme = []
		for message in messages:
			retme.append('PRIVMSG ' + channel + ' :' + message + '\r\n')
		return '\n'.join(retme)
	else:
		return "PRIVMSG " + channel + " :" + message + "\r\n"

def html_strip(s):
	return re.sub('<[^<]+?>', '', s)

def html_decode(s):# Replaces some HTML codes with normal text ones.
	s = s.replace("&amp;", "&")
	s = BeautifulSoup(s,convertEntities=BeautifulSoup.HTML_ENTITIES)
        return str(s)
def textbetween(str1,str2,text):# returns the text between str1 and str2 in text. This is usefull for parsing data.
        posstr1 = text.find(str1)
        posstr2 = text.find(str2)
        between = text[posstr1 + len(str1):posstr2]
        return between
def command(command,recv): #finds the argument for a command. (Depricated. Use argv())
        if command + " " in recv or command in recv:
                num = recv.find(command)
                message = recv[num + len(command):]
                if message == '':
                        return 'no word'
                else:
                        return str(message[1:])
        else:
                message = "None"
def argv(gcommand,recv):# returns a named, multidimentional array of on recv info [nick, user, channel, [argv[0], argv[1],
	com = gcommand # 							etc..]] (Args are in aseparate array)
	gcommand = command(gcommand,recv)
	if recv[0] == ':':
		nick = textbetween(':', '!', recv)
		user = textbetween('~', '@', recv)
		channel = textbetween('PRIVMSG ', ' :', recv)
	else:
		nick = 'Unknown'
		user = 'Unknown'
		channel = None
	argc = gcommand.split()
	argv = []
	argv.append(com)
	for i in argc:
		argv.append(i)
	return {'nick' : nick, 'user' : user,'channel' : channel, 'argv' : argv}
def gettitle(url):#get the page title of an URL
	try:
        	soup = BeautifulSoup(urllib2.urlopen(url))
        	return soup.title.string
	except:
		return False
def geturl(recv):#parse an URL from a string
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', recv)
	if url and url != '':
		return url
	else:
		return False
def maketiny(url):# make a tinyurl from a string
	try:
        	html = urllib2.urlopen("http://tinyurl.com/api-create.php?url=" + url)
        	tiny = str(html.read())
        	return tiny
	except:
		return False
