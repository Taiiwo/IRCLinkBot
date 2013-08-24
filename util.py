#util.py
#This file contains fuctions available for the plugin developers.
import socket, sys, re, urllib2, time, os, random
from plugins import *
from BeautifulSoup import BeautifulSoup

#start functions
def say(channel, message):
	return 'PRIVMSG ' + channel + ' :' + message + '\r\n'
	
def html_decode(s):
        htmlCodes = (("'", '&#39;'),('"', '&quot;'),('>', '&gt;'),('<', '&lt;'),('&', '&amp;'))
        for code in htmlCodes:
                s = s.replace(code[1], code[0])
        return s
def textbetween(str1,str2,text):
        posstr1 = re.search(r"[^a-zA-Z](" + str1 + ")[^a-zA-Z]", text).start(1)
        posstr2 = re.search(r"[^a-zA-Z](" + str2 + ")[^a-zA-Z]", text).start(1)
        between = text[posstr1 + len(str1):posstr2]
        return between
def command(command,recv): #finds the argument for a command.
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
def geturl(recv):#parse an URL from a string
        return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', recv)
def maketiny(url):
        html = urllib2.urlopen("http://tinyurl.com/api-create.php?url=" + url)
        tiny = str(html.read())
        return tiny
