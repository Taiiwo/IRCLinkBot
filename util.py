#util.py
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
	f = open('linkbot.conf','w')
	f.write(json.dumps(config, sort_keys=True, indent=4, separators=(',', ': ')))
	f.close()
def say(channel, message):# A quick way to make the bot say something. Use return say(argv['channel'],message)
	return 'PRIVMSG ' + channel + ' :' + message + '\r\n'# (You need to define argv with the argv() function

def html_strip(s):
	tags = ['p','b','ul','ln','div']
	for tag in tags:
		s.remove('<'+tag+'>')
		s.remove('</'+tag+'>')

def html_decode(s):# Replaces some HTML codes with normal text ones.
        htmlCodes = (("'", '&#39;'),('"', '&quot;'),('>', '&gt;'),('<', '&lt;'),('&', '&amp;'))
        for code in htmlCodes:
                s = s.replace(code[1], code[0])
        return s
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
	argc = gcommand.split()
	argv = []
	argv.append(com)
	for i in argc:
		argv.append(i)
	return {'nick' : nick, 'user' : user,'channel' : channel, 'argv' : argv}
def gettitle(url):#get the page title of an URL
        soup = BeautifulSoup(urllib2.urlopen(url))
        return soup.title.string
def geturl(recv):#parse an URL from a string
        return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', recv)
def maketiny(url):# make a tinyurl from a string
        html = urllib2.urlopen("http://tinyurl.com/api-create.php?url=" + url)
        tiny = str(html.read())
        return tiny
