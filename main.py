import socket
import sys
import ssl
import json
import os
import thread
import re
import time
from util import *


class botApi:
    loop = 0
    sending = 0
    lastPingTime = time.time()
    defaultConfig = {
        "settings": {
            "authenticate": "False",
            "botIdent": "IRCLinkBot",
            "botName": "IRCLinkBot",
            "botNick": "IRCLinkBot",
            "botUser": "IRCLinkBot",
            "host": "irc.freenode.net",
            "port": "6667",
            "ssl": "yes",
            "hoursDiffGMT": "-4",
            "pingTimeout": "300",
            "joinChannels": [
                "#IRCLinkBot"
            ],
            "joinMessage": "LinkBot v5.3 - Welcome to TaiiwoCorp.",
            "maxLinkLen": "53",
            "messageTimeSpacing": "0.5",
            "pluginIgnoreChannels": {
                "#freenode": [
                    "link.py"
                ]
            },
            "printRecv": "True",
            "printSend": "True",
            "recvLen": "512",
            "userModes": [
                {
                    "channel": "#IRCLinkBot",
                    "isAuth": "True",
                    "modes": "gao",
                    "nick": "Taiiwo"
                }
            ]
        },
        "variables": {
            "numr": "20"
        }
    }

    def __init__(self):
        self.importConfig()

    def importConfig(self, submissive=False):
        fails = 0
        while 1:
            try:
                # Import settings file
                configFile = open('./linkbot.conf', 'rw')
                # Parse config file
                self.config = dictUpdate(
                    self.defaultConfig,
                    json.loads(configFile.read())
                )
                # Convert each value of the dict to a byte string. We will encode this later.
                self.config = dictUnicodeToByte(self.config)
                configFile.close()
                return self.config
                break
            except:
                if fails < 5:
                    print "[E] Failed to read config, trying again..."
                    fails += 1
                else:
                    error = "[E] Failed to read config 5 times. Check file \
                            exists, named linkbot.conf, and syntax is correct."
                    if submissive:
                        print error
                        return self.config
                    else:
                        raise Exception(error)
                        break

    def connect(self):
        print "[-]Connecting to server..."
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while 1:
            try:
               # connect to server
                if self.config['settings']['ssl'].lower() == 'yes':
                    self.s.connect((self.config['settings']['host'],
                                    int(self.config['settings']['port'])))
                    self.s = ssl.wrap_socket(self.s)
                else:
                    self.s.connect((self.config['settings']['host'],
                                    int(self.config['settings']['port'])))
                break
            except:
                print "[E]Could not connect to server, trying again..."
                print "Please check your host and port number if this error continues."
                time.sleep(5)
        time.sleep(0.2)
        # set nick
        self.s.send('nick %s\r\n' % (self.config['settings']['botNick']))
        time.sleep(0.2)
        # set user
        self.s.send("user %s * %s %s\r\n" % (
            self.config['settings']['botIdent'],
            self.config['settings']['botUser'],
            self.config['settings']['botName']
        ))
        # authenticate
        if self.config['settings']['authenticate'] == 'True':
            try:
                passFile = open('pass', 'r')
                password = passFile.read()
                self.say('nickserv', 'identify %s' % (password))
            except:
                print "[E] Password not found. Continuing without \
                        authentication."
        while 1:
            recvData = self.recv()
            if self.config['settings']['printRecv'] == 'True':
                print recvData
            if ":You are now identified for" in recvData \
                    or self.config['settings']['authenticate'] != 'True':
                break
        # Join all the channels
        for channel in self.config['settings']['joinChannels']:
            self.s.send('join %s\r\n' % (channel))
            time.sleep(0.5)
            self.say(channel, self.config['settings']['joinMessage'])

    def do(self):
        self.importConfig(submissive=True)  # Refresh the config file
        bot.recv()
        bot.runPlugins()
        bot.handlePing()

    def recv(self):
        bot.loop += 1
        recvLen = int(self.config['settings']['recvLen'])
        # make sure recv data is decoded into a bytestring
        self.recvData = self.s.recv(recvLen).decode('utf-8', 'ignore').encode('utf-8')
        #print type(self.recvData)
        if self.recvData == '' or not self.recvData:
            self.s.close()
            self.connect()
        if self.config['settings']['printRecv'] == 'True':
            print self.recvData
        return self.recvData

    def say(self, target, message):
        # send multiple messages by splitting with \n
        # It is this way to help stop IRC injection
        retme = ""
        if type(target) == unicode:
            target = target.encode('utf-8')
        for msg in message.split('\n'):
            if type(msg) == unicode:
                msg = msg.encode('utf-8')
            if msg and msg != '':
                if len(msg) > 430:
                    # split into a group of messages 430 chars long
                    msgs = [msg[i:i+430] for i in range(0, len(msg), 430)]
                    for msg in msgs:
                        retme += 'PRIVMSG %s :%s\r\n' % (target, msg)
                else:
                    retme += 'PRIVMSG %s :%s\r\n' % (target, msg)
        self.send(retme)
        # I don't know why you'd want this, but
        # better to return something than nothing.
        return retme

    def runPlugins(self):  # run all plugins in threads
        self.indexPlugins()
        # Format data to send to the plugins.
        data = {'recv': self.recvData,  # recv data from IRC
                'config': self.config,  # json object of config file
                'loop': self.loop,      # number of messages received
                'api': self}            # The bot object
        for pluginFolder in self.pluginList:
            thread.start_new_thread(
                self.pluginThread,
                (pluginFolder['nameList'], pluginFolder['path'], data)
            )

    def indexPlugins(self):
        self.pluginList = []
        path = './plugins/'
        # Get plugin filenames only from the plugins directory, This runs the
        # plugins no matter what.
        rootPlugins = os.listdir('./plugins/')
        # Run the root plugins in a new thread
        self.pluginList.append({"nameList": rootPlugins, "path": path})
        # Check if the recv is a privmsg from a channel
        if re.match('^:[^!]*!~?[^@]*@[^\s]*\s(PRIVMSG|privmsg)\s#[^:]*\s:.*',
                        self.recvData) is not None:
            # Run plugins from ./plugins/privmsg/*
            for root, subFolders, files in os.walk('./plugins/privmsg/',
                                                   followlinks=True):
                # Fetch plugins recursively. This means you can organize
                # plugins in sub folders however you'd like. eg. Have a folder
                # full of entertainment plugins that you can easily disable by
                # prepending '.' to the folder name.
                self.pluginList.append({"nameList": files, "path": root})
        # If recv is a private message to the bot
        elif not re.match('^:[^!]*!~?[^@]*@[^\s]*\s(PRIVMSG|privmsg)\s%s:.*'
                          % (self.config['settings']['botNick']),
                          self.recvData) == None:
            # Run plugins from ./plugins/privmsgbot/*
            for root, subFolders, files in os.walk('./plugins/privmsgbot/',
                                                   followlinks=True):
                self.pluginList.append({"nameList": files, "path": root})

        # run plugins from the directory named 'root'
        for root, subFolders, files in os.walk('./plugins/root/',
                                               followlinks=True):
            self.pluginList.append({"nameList": files, "path": root})

    def pluginThread(self, plugins, path, data):  # This function is for
        for plugin in plugins:                    # threading
            self.runPlugin(plugin, path, data)

    def runPlugin(self, plugin, path, data):  # runs a single plugin
        if plugin[-3:] == '.py' and plugin[0:3] != 'lib':
            pluginFile = open('%s/%s' % (path, plugin), 'r')
            exec(pluginFile)
            pluginFile.close()
            args = argv('', self.recvData)
            toSend = main(data)
            if args['channel'] in \
                    self.config['settings']['pluginIgnoreChannels']:
                if plugin in (self.config
                              ['settings']
                              ['pluginIgnoreChannels']
                              [args['channel']]):
                    toSend = None
            if toSend and toSend != '' and toSend is not None:
                sendStatus = self.send(toSend)
                if type(sendStatus) == str():
                    print '%s : %s' % (str(sendStatus), plugin)

    def send(self, message):
        while 1:
            # this is so the bot can only send 1 message at a time
            # (Since we're threading), so as not to get us kicked for
            # excess flood
            if self.sending < 1:
                self.sending += 1
                for send in message.split('\n'):
                    try:
                       self.s.send(send + '\n')
                       time.sleep(
                            float(
                                self.config['settings']
                                ['messageTimeSpacing']
                            )
                       )
                    except Exception:
                        self.sending -= 1
                        errormsg = sys.exc_info()[1]
                        if errormsg is not None:
                            return errormsg
                self.sending -= 1
                break
            else:
                continue
        if self.config['settings']['printSend'] == 'True':
            print message
        return True

    def handlePing(self):
        # I was thinking about making the bot run plugins from a 'PING'
        # folder, but saw very little point, other than possible data
        # logging?. Regardless, I left it out.
        for line in self.recvData.splitlines():
            if line[0:5] == 'PING ':
                self.lastPingTime = time.time()
                self.s.send('PONG %s\r\n' % (self.recvData.split(' ')[1][1:]))
                if self.config['settings']['printSend'] == 'True':
                    print 'PONG %s\r\n' % (self.recvData.split(' ')[1][1:])

bot = botApi()
bot.connect()
while 1:
    bot.do()
