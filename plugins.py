#Each function in the plugins class will be passed data from IRC, and run.
#ANY string returned by a function WILL be said in IRC. That includes your function
#not returning. You must atleast return ''
#Information sent from IRC is sent as a named list.
#data[' x ']:
#  recv = lump of raw TCP data received from IRC
#  s = The main socket instance (This is depricated. Plugins can only send data)
#  loop = The number of messages the bot has processed so far (int)
#  numr = user specified value of how many links to ignore (int)
#  channel = user specified channel name (str)
from util import *
import urllib, json
from lxml import etree
class plugins(object):
	def __init__(self,data):
		from util import *
	def love(self,data):
		message = command("!love",data['recv'])
        	if str(message) != 'None':
			args = argv('!love', data['recv'])
        	        return say(args['channel'],'I love ' + str(message))# Example of 'say' function.
		else:
			return ''
        def say(self,data):
		message = argv("!say", data['recv'])
	        if message['argv'][0] == '!say' and message['user'] in data['admins']:
			say = ' '.join(message['argv'][2:])
	                return 'privmsg ' + message['argv'][1] + ' :' + say + '\r\n'
        def rfl(self,data):
		message = command("!rfl", data['recv'])
        	if str(message) != 'None':
			args = argv('!rfl', data['recv'])
        	        return 'privmsg ' + args['channel'] + ' :I really fucking love ' + str(message) + '\r\n'
		else:
			return ''
        def fact(self,data):
		message = command("!fact", data['recv'])
	        if str(message) != 'None':
			args = argv('!fact', data['recv'])
	                return 'privmsg ' + args['channel'] + ' :' + textbetween("<strong>","</strong>", urllib2.urlopen("http://randomfunfacts.com").read())[3:-4] + '\r\n'
		else:
			return ''
        def joke(self,data):
		if '!joke' in data['recv']:
			loop = 1
			args = argv('!joke',data['recv'])
			while loop == 1:
				html = urllib2.urlopen('http://www.sickipedia.org/getjokes/random').read()
				soup = BeautifulSoup(html)
				joke = soup.body.find('div', attrs={'class':'jokeText'}).text
				if len(joke) <= 300:
					loop = 0
			ujoke = joke.decode("utf-8")
			joke = html_decode(ujoke.encode("ascii","ignore"))
        	        return 'privmsg ' + args['channel'] + ' :' + joke + '\r\n'
		else:
			return ''
	def pong(self,data):#respond to ping req in a string --Not perfect, but works
	        if "ping" in data['recv'] or "PING" in data['recv']:
	                url = str(geturl(str(data['recv'])))
	                if url != "":
	                        return "PONG " + url + "\n\r"
			else:
				return ''
		else:
			return ''
        def wyr(self,data):
		if "!wyr" in data['recv']:
        	        error = 1
			args = argv('!wyr',data['recv'])
        	        while error == 1:
        	                try:
        	                        return 'PRIVMSG '+ args['channel'] +' :' + gettitle('http://www.rrrather.com/view/' + str(random.randint(0,40000)))+ '\r\n'
        	                        error = 0
        	                except:
        	                        print '[Server Error (Not my fault)]'
        	                        error = 1
        def roll(self,data):
		message = command('!r', data['recv'])
        	if str(message) != 'None':
			if 'd' in message or 'D' in message:
				args = argv('!r', data['recv'])
				message.replace('D','d')
				pos_of_d = re.search(r"[^a-zA-Z](d)[^a-zA-Z]", message).start(1)
				num_of_dice = message[:pos_of_d]
				print num_of_dice
				dice_value = message[pos_of_d + 1:]
				print dice_value
				try:
                                        num_of_dice = int(num_of_dice)
					dice_value = int(dice_value)
                                        num_valid = True 
                                except:
                                        num_valid = False
				if num_valid and num_of_dice >= 1 and len(str(num_of_dice)) <4 and len(str(dice_value)) < 10 and dice_value >= 1:
					i = num_of_dice
					total = 0
					while i > 0:
						total += random.randint(1,dice_value)
						i = i - 1
					return say(args['channel'],str(total))
				else:
					return ''
			else:
        	        	try:
        	        	        int(message)
        	        	        error = 0
        	        	except:
        	        	        error = 1
        	        	if error != 1 and len(message) < 10 and int(message) >= 1:
					args = argv('!r', data['recv'])
					print args['channel']
        	        	        return 'PRIVMSG '+ args['channel'] +' :' + str(random.randint(1,int(message))) + '\r\n'
	def linkbot(self,data):
		args = argv(' :',data['recv'])
		if not hasattr(self, "link"):# it doesn't exist yet, so initialize it
			self.link2 = ''
		self.nlink = ''
		self.link = ''
		urlsfound = True
	        try:#look for urls in recv
	                self.link2 = self.link#make a backup of last url
	                self.link = geturl(data['recv'])
	                print self.link
			error = 0
	        except Exception , err:
			print sys.exc_info()[1]
	                print "[-]No URLS found"
	                error = 1
	                urlsfound = False
	        if self.link2 != self.link:#This stops spamming links
	                try:#try to get the title of the url
	                        self.nlink = self.link[0]
				badext = ('.cgi','.CGI','.jpg','.png','.gif','.bmp')
	                        if self.nlink[-4:] in badext:# don't process images and stuff
	                                pass
				else:#only get one line of titles
                                	title = gettitle(self.nlink)
                                	title = title.splitlines()
                                	title = ''.join(title)
                        	if len(title) >= 150:#cap the length of titles
                        	        title = title[:150]
                        	title = html_decode(title)
				title = title.encode('ascii', 'ignore')
                        	print title
				error = 0
               		except:	
                	        print "[E]No valid title"
                	        error = 2
                	#post title to irc
                	if error == 0 and data['loop'] >= data['numr']:
				slink = self.nlink.decode("utf-8")
				self.nlink = slink.encode("ascii","ignore")
                	        if len(self.nlink) >= 53:
					return 'privmsg ' + args['channel'] + ' :^ ' + str(title) + " " + maketiny(self.nlink) + ' ^\r\n'
                        	else:
                                	return 'privmsg ' + args['channel'] + ' :^ ' + str(title) + " ^\r\n"
               		if error == 2 and urlsfound == True and self.nlink != "" and data['loop'] >= data['numr'] and len(self.nlink) >= 53:
                        	return 'privmsg ' + args['channel'] + ' : ^ ' + maketiny(self.nlink) + ' ^\r\n'
			else:
				return ''
		else:
			return ''
	def nmap(self,data):
		if '!nmap' in data['recv']:
			args = argv('!nmap',data['recv'])
			if args['user'] in data['admins']:
				host = args['argv'][len(args['argv']) - 1]
				arguments = args['argv'][0:len(args['argv']) - 1]
				error = 0
				for i in host:
					if i.islower() or i.isupper() or '.' in i or '/' in i or ':' in i:
						pass
					else:
						error = 1
				for argument in arguments:
					for c in argument:
						if c.islower() or c.isupper():
							pass
						else:
							error = 1
				if error == 0:
					command = []
					command.append('nmap')
					for i in arguments:
						command.append(i)
					out = subprocess.call(command)
					out = textbetween('VERSION', 'Service Info:', out)
					out = out.splitlines()
					fout = []
					for i in out:
						fout.append(say(i))
					fout = ''.join(fout)
					return say(args['channel'], fout)
			else:
				return say(args['channel'], 'You are not my daddy, ' + args['nick'] + '.')
	def join(self,data):
		try:
			message = argv('!join',data['recv'])
		except:
			message = ''
		if message != '' and message['user'] in data['admins']:
			return 'JOIN ' + message['argv'][1] + '\r\n'
	def leave(self,data):
                try:
                        message = argv('!leave',data['recv'])
                except:
                        message = ''
                if message != '' and message['user'] in data['admins']:
                        return 'PART ' + message['argv'][1] + '\r\n'
	def scoop(self, data):
		if '!scoop ' in data['recv']:
			args = argv('!scoop',data['recv'])
			if args['user'] in data['admins'] or args['argv'][1] == 'me':
				sum = urllib2.urlopen('http://thescoop.io/ots.php?to_sum=' + str(args['argv'][2]) + '&ratio=10').read()
				sum = " ".join(sum.split())
				#print 'http://thescoop.io/ots.php?tosum=' + urllib.quote_plus(args['argv'][2]) + '&ratio=10'
				sum = re.sub('<[^<]+?>', '', sum)# strip HTML tags
				sum = html_decode(sum)
				sum = sum.splitlines()
				sum = ''.join(sum)
				if args['user'] in data['admins'] and sum != '':
					if args['argv'][1] == "me":
						return say(args['nick'],sum)
					else:
						return say(args['argv'][1],sum)
				elif args['argv'][1] == 'me' and sum != '':
					return say(args['nick'],sum)
	def send(self, data):
		if '!send' in data['recv']:
			args = argv('!send',data['recv'])
			if args['user'] in data['admins']:
				return ' '.join(args['argv'][1:])+ '\r\n'

	def chansearch(self, data):
	    if '!4search' in data['recv']:
	        args = argv('!4search',data['recv'])
	        if args['argv'][1] == 'usage':
	            return say(args['channel'], '!4search b op/all Taiiwo Trollstrich TJ')
	        board = args['argv'][1]
	        arg = args['argv'][2]#Should be either all or op
            words = args['argv'][3:]
            #Doing stupid TJ's suggestion:
            for word in words:
                for letter in word:
                    if letter == '-':
                        letter = ' '
            results = []
            rawjson = urllib2.urlopen('http://api.4chan.org/' + board + '/catalog.json').read()
            time.sleep(1)
            parsedjson = json.loads(rawjson)
            count = 0
            pagecount = 0
            retme = []
            for page in parsedjson:
                print 'Searching page ' + str(count)
                count += 1
                threadcount = 0
                for thread in page['threads']:
                    if 'args' in locals():
                        if arg != 'op':
                            print 'On thread ' + str(threadcount)
                            threadcount += 1
                            #get thread number
                            num = thread['no']
                            try:
                                rawreplies = urllib2.urlopen('http://api.4chan.org/' + board + '/res/' + str(num) + '.json').read()
                            except:
                                print "Thread 404'd"
                                break
                            time.sleep(0.00001)
                            parsedreplies = json.loads(rawreplies)
                            for post in parsedreplies['posts']:
                                if 'com' in post:
                                    for string in words:
                                        if string in post['com']: # (Thinking of checking post['name']
                                            if num == post['no']:
                                                retme.append('http://boards.4chan.org/' + board + '/res/' + str(num))
                                                print 'http://boards.4chan.org/' + board + '/res/' + str(num)
                                            else:
                                                retme.append('http://boards.4chan.org/' + board + '/res/' + str(num) + '#p' + str(post['no']))
                                                print 'http://boards.4chan.org/' + board + '/res/' + str(num) + '#p' + str(post['no'])
                        else:
                            #print pagecount
                            pagecount += 1
                            if 'com' in thread:
                                for string in words:
                                    if string in thread['com']:
                                        retme.append('http://boards.4chan.org/' + board + '/res/' + str(thread['no']))
                                        print 'http://boards.4chan.org/' + board + '/res/' + str(thread['no'])
            if retme == []:
                return say(args['nick'], "No threads found")
            retmeforrealthistime = []
            lt = 15
            appendloop = 0
            for i in retme:
                if appendloop <= lt:
                    retmeforrealthistime.append(say(args['nick'], i))
                appendloop += 1
            return ''.join(retmeforrealthistime)
	def wa(self, data):
		if '!wa' in data['recv']:
			args = argv('!wa',data['recv'])
			query = '%20'.join(args['argv'][1:])
			response = urllib2.urlopen('http://api.wolframalpha.com/v2/query?input=' + query + '&appid=Y76J7A-WKLWTY7RKJ').read()
			tree = etree.XML(response)
			answer = tree.findall('pod')[1].find('subpod').find('plaintext').text
			answer = answer.split('\n')
			toret = []
			for i in answer:
				toret.append(say(args['channel'],i).encode('ascii', 'ignore'))
			return ''.join(toret)

	def whoisonjoin(self, data):
		#:Taiiwo!~Taiiwo@cpc3-nott16-2-0-cust414.12-2.cable.virginm.net JOIN ##426699k
		if ' JOIN ' in data['recv']:
			args = argv('JOIN',data['recv'])
			return 'WHOIS ' + args['nick'] + '\r\n'
	def autoop(self,data):
		if ':End of /WHOIS list.' in data['recv']:
			args = argv("", data['recv'])
			if ':is logged in as' in data['recv']:
				lastline = data['recv'].splitlines()[len(data['recv'].splitlines())-1]
				supposednick = textbetween(data['nick']+' ',' :End of /WHOIS list.',lastline)
				#debug
				print lastline
				print supposednick
				#/debug
				for user in data['channelops']:
					if supposednick == user['user']:
						return 'MODE ' + user['channel'] + ' +o ' + user['user'] + '\r\n'
