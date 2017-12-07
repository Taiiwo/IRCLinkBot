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
import urllib, json
from util import *
from lxml import etree
from shodan import WebAPI
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
		args = argv("!say", data['recv'])
	        if args['argv'][0] == '!say' and args['nick'] in self.authnick:
			say = ' '.join(args['argv'][2:])
	                return 'privmsg ' + args['argv'][1] + ' :' + say + '\r\n'
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
	def pong(self,data):#respond to ping req in a string
	        if "ping" in data['recv'] or "PING" in data['recv']:
	                url = data['recv'].split(' ')[1]
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
		if '!r' in data['recv']:
			args = argv('!r', data['recv'])
			if 'd' in args['argv'][1] or 'D' in args['argv'][1]:
				args['argv'][1].replace('D','d')
				pos_of_d = re.search(r"[^a-zA-Z](d)[^a-zA-Z]", args['argv'][1]).start(1)
				num_of_dice = args['argv'][1][:pos_of_d]
				dice_value = args['argv'][1][pos_of_d + 1:]
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
        	        	        int(args['argv'][1])
        	        	        error = 0
        	        	except:
        	        	        error = 1
        	        	if error != 1 and len(args['argv'][1]) < 10 and int(args['argv'][1]) >= 1:
					print args['channel']
        	        	        return 'PRIVMSG '+ args['channel'] +' :' + str(random.randint(1,int(args['argv'][1]))) + '\r\n'
	def linkbot(self,data):
		args = argv('@',data['recv'])
		if not hasattr(self, "link"):# it doesn't exist yet, so initialize it
			self.link2 = ''
			self.nlink = ''
			self.link = ''
		urlsfound = True
	        try:#look for urls in recv
	                self.link2 = self.link#make a backup of last url
	                self.link = geturl(data['recv'])
			if self.link == '':
				raise Exception("No links found.")
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
				if not 'http' in data['recv']:
					urlsfound = False
                	        error = 2
                	#post title to irc
                	if error == 0 and data['loop'] >= data['numr']:
				slink = self.nlink.decode("utf-8")
				self.nlink = slink.encode("ascii","ignore")
                	        if len(self.nlink) >= 53:
					return 'privmsg ' + args['channel'] + ' :^ ' + str(title) + " " + maketiny(self.nlink) + ' ^\r\n'
                        	else:
                                	return 'privmsg ' + args['channel'] + ' :^ ' + str(title) + " ^\r\n"
               		if error == 2 and urlsfound and self.nlink != "" and data['loop'] >= data['numr'] and len(self.nlink) >= 53:
                        	return 'privmsg ' + args['channel'] + ' : ^ ' + maketiny(self.nlink) + ' ^\r\n'
			else:
				return ''
		else:
			return ''
	def nmap(self,data):
		if '!nmap' in data['recv']:
			args = argv('!nmap',data['recv'])
			if args['user'] in self.authnick:
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
		if '!join' in data['recv']:
			args = argv('!join',data['recv'])
			if args['nick'] in self.authnick:
				return 'JOIN ' + args['argv'][1] + '\r\n'
	def leave(self,data):
		if '!leave' in data['recv']:
			args = argv('!leave',data['recv'])
			if args['nick'] in self.authnick:
                        	return 'PART ' + args['argv'][1] + '\r\n'
	def scoop(self, data):
		if '!scoop ' in data['recv']:
			args = argv('!scoop',data['recv'])
			if args['user'] in self.authnick or args['argv'][1] == 'me':
				sum = urllib2.urlopen('http://thescoop.io/ots.php?to_sum=' + str(args['argv'][2]) + '&ratio=10').read()
				sum = " ".join(sum.split())
				#print 'http://thescoop.io/ots.php?tosum=' + urllib.quote_plus(args['argv'][2]) + '&ratio=10'
				sum = re.sub('<[^<]+?>', '', sum)# strip HTML tags
				sum = html_decode(sum)
				sum = sum.splitlines()
				sum = ''.join(sum)
				if args['user'] in self.authnick and sum != '':
					if args['argv'][1] == "me":
						return say(args['nick'],sum)
					else:
						return say(args['argv'][1],sum)
				elif args['argv'][1] == 'me' and sum != '':
					return say(args['nick'],sum)
	def spambot(self,data):
		# set root variables
		if not hasattr(self, 'lastmessage'):
			self.lastmessage = {'nick':None,'msg':None}
		if not hasattr(self, 'spamcount'):
			self.spamcount = 0
		# if the same message is posted twice
		args = argv('@', data['recv'])
		if data['recv'] == self.lastmessage['msg'] and args['nick'] == self.lastmessage['nick']:
			self.spamcount += 1
		else:
			self.spamcount = 0
		if self.spamcount >= data['maxspam']:
			self.spamcount = 0
			self.lastmessage = {'nick':args['nick'],'msg':data['recv']}
			return 'kick ' + args['channel'] + ' ' + args['nick'] + ' Spam\r\n'
		self.lastmessage = {'nick':args['nick'],'msg':data['recv']}

	def send(self, data):
		if '!send' in data['recv']:
			args = argv('!send',data['recv'])
			if args['nick'] in self.authnick:
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
		if '!wa ' in data['recv']:
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
						if not hasattr(self, 'authnick'):
							self.authnick = []
						if not user['user'] in self.authnick:
							self.authnick.append(user['user'])
							print 'nicklist: ' + str(self.authnick)
						return 'MODE ' + user['channel'] + ' +o ' + user['user'] + '\r\n'
			elif args['nick'] in self.authnick:
				self.authnick.remove(args['nick'])
	def authme(self, data):
		if '!authme' in data['recv']:
			args = argv('!authme',data['recv'])
			return 'WHOIS ' + args['nick'] + '\r\n'
	def locateip(self, data):
		if '!locateip' in data['recv']:
			args = argv('!locateip',data['recv'])
			api = WebAPI("KpYC07EoGBtGarTFXCpjsspMVQ0a5Aus")#don look
			query = args['argv'][1]
			try:
				socket.inet_aton(query)
			except socket.error:
				return None
			results = api.host(query)
			output = []
			output.append('OS: ' + str(results['os']))
			output.append('City: ' + str(results['city']) + '\tPostal code: ' + str(results['postal_code']))
			output.append('Area code: ' + str(results['area_code']) + '\t\tCountry code: ' + str(results['country_code']))
			output.append('Region name: ' + str(results['region_name']) + '\tCountry name: ' + str(results['country_name']))
			output.append('Latitude: ' + str(results['latitude']) + '\tLongitude: ' + str(results['longitude']))
			ports = []
			for data in results['data']:
				port = data['port']
				if not str(port) in ports:
					ports.append(str(port))
			output.append('Open ports: ' + ', '.join(ports))
			ircoutput = ''
			for line in output:
				ircoutput += say(args['channel'],line)
			return ircoutput
	def timeuntil(self,data):
		if not hasattr(self, "counttime"):
			self.counttime = time.time()
		if hasattr(self, "countdown") and (time.time() - self.counttime) > 20:
			self.counttime - time.time()			
			query = '%20'.join('Time Until ' + self.countdown['date'])
			response = urllib2.urlopen('http://api.wolframalpha.com/v2/query?input=' + query + '&appid=Y76J7A-WKLWTY7RKJ').read()
			tree = etree.XML(response)
			answer = tree.findall('pod')[1].find('subpod').find('plaintext').text
			answer = answer.split('\n')
			toret = []
			for i in answer:
				print i
				toret.append(say(self.countdown['channel'],i).encode('ascii', 'ignore'))
			return ''.join(toret)
	def setcountdown(self, data):
		if '!setcountdown' in data['recv']:
			args = argv('!setcountdown', data['recv'])
			if args['nick'] in self.authnick:
				if args['argv'][2] != 'none':
					self.countdown = {'channel':args['argv'][1],
							'date':' '.join(args['argv'][2:])}
				else:
					self.countdown = None
	def uc(self, data):
		if '!uc ' in data['recv']:
			args = argv('!uc', data['recv'])
			query = '%20'.join(args['argv'][1:])
			wikiajson = urllib2.urlopen('http://uncovering-cicada.wikia.com/api/v1/Search/List?query=' + query).read()
			wikiaobj = json.loads(wikiajson)
			title = wikiaobj['items'][0]['title']
			tiny = maketiny(wikiaobj['items'][0]['url'])
			return say(args['channel'], title + ' - ' + tiny)
	def inform(self, data):
		if '!inform ' in data['recv']:
			args = argv('!inform', data['recv'])
			if args['nick'] in self.authnick:
				toret = []
				f = open (args['channel'] + '.inform','r')
				toret.append('MODE ' + args['channel'] + ' +q ' + args['argv'][1] + '\r\n')
				toret.append('PRIVMSG ' + args['argv'][1] + ' :' + f.read() + '\r\n')
				if not hasattr(self, "informnick"):
					self.informnick = {}
				self.informnick[args['argv'][1]] = args['channel']
				return '\r\n'.join(toret)
		if 'I understand' in data['recv']:
			args = argv('@', data['recv'])
			if args['channel'] == data['nick']:
				if args['nick'] in self.informnick:
					toret = 'MODE ' + self.informnick[args['nick']] + ' -q ' + args['nick'] + '\r\n'
					return toret
