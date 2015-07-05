#This file contains fuctions available for the plugin developers.
import socket
import sys
import re
import urllib2
import time
import os
import random
import json
import htmlentitydefs
import collections
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

def html_decode(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                if text[1:-1] == "apos":
                    text = u"'"
                else:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def textbetween(str1,str2,text):# returns the text between str1 and str2 in text. This is useful for parsing data.
        posstr1 = text.find(str1)
        posstr2 = text.find(str2)
        between = text[posstr1 + len(str1):posstr2]
        return between

def command(command,recv): #finds the argument for a command.
        if command in recv and command != '':
            num = recv.find(command)
            message = recv[num + len(command) + 1:]
            if message == '':
                return None
            else:
                return message
        else:
            return None

def argv(com,recv):# returns a named, multidimensional array of on recv
    # info [nick, user, channel, [argv[0], argv[1], etc..]] (Args are in
    # a separate array)
    m = re.match(
        "^:([^!]*)!~?([^@]*)@([^\s]*)\s(PRIVMSG|privmsg)\s(#?[^\s]*)\s:(.*)",
        recv
    )
    if m is not None:
        nick = m.group(1)
        user = nick
        ident = m.group(2)
        host = m.group(3)
        channel = m.group(5)
        message = m.group(6)
    else:
        return {'nick': 'Unknown', 'user': 'Unknown', 'channel': 'Unknown'}
    argc = command(com, message)
    argv = [com,]
    if argc is not None:
        argv += argc.split()
    return {'nick' : nick, 'user' : user,'channel' : channel, 'argv' : argv,
            'ident': ident, 'hostname': host, 'message': message}

def gettitle(url):#get the page title of an URL
    try:
        soup = BeautifulSoup(urllib2.urlopen(url).read(1024 * 1024))
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

def dictUpdate(d, u):
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = dictUpdate(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d

def dictUnicodeToByte(input):# recurively change unicode values of a dict to byte
    if isinstance(input, dict):
        return {dictUnicodeToByte(key):dictUnicodeToByte(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [dictUnicodeToByte(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
