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
class plugins(object):
	def __init__(self,data):
		from util import *
	def love(self,data):
		message = command("!love",data['recv'])
        	if str(message) != 'None':
        	        return say(data['channel'],'I love ' + str(message))# Example of 'say' function.
		else:
			return ''
        def say(self,data):
		message = command("!say", data['recv'])
	        if str(message) != 'None':
	                return 'privmsg ' + data['channel'] + ' :' + str(message) + '\r\n'
        def rfl(self,data):
		message = command("!rfl", data['recv'])
        	if str(message) != 'None':
        	        return 'privmsg ' + data['channel'] + ' :I really fucking love ' + str(message) + '\r\n'
		else:
			return ''
        def fact(self,data):
		message = command("!fact", data['recv'])
	        if str(message) != 'None':
	                return 'privmsg ' + data['channel'] + ' :' + textbetween("<strong>","</strong>", urllib2.urlopen("http://randomfunfacts.com").read())[3:-4] + '\r\n'
		else:
			return ''
        def joke(self,data):
		if '!joke' in data['recv']:
			loop = 1
			while loop == 1:
				html = urllib2.urlopen('http://www.sickipedia.org/getjokes/random').read()
				soup = BeautifulSoup(html)
				table = soup.body.findAll('table')[3]
				joke = table.findAll('td')[0].text
				if len(joke) <= 300:
					loop = 0
			ujoke = joke.decode("utf-8")
			joke = html_decode(ujoke.encode("ascii","ignore"))
        	        return 'privmsg ' + data['channel'] + ' :' + joke + '\r\n'
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
        	        while error == 1:
        	                try:
        	                        return 'PRIVMSG '+ data['channel'] +' :' + gettitle('http://www.rrrather.com/view/' + str(random.randint(0,40000)))+ '\r\n'
        	                        error = 0
        	                except:
        	                        print '[Server Error (Not my fault)]'
        	                        error = 1
        def roll(self,data):
		message = command('!r', data['recv'])
        	if str(message) != 'None':
			if 'd' in message or 'D' in message:
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
					return say(data['channel'],str(total))
				else:
					return ''
			else:
        	        	try:
        	        	        int(message)
        	        	        error = 0
        	        	except:
        	        	        error = 1
        	        	if error != 1 and len(message) < 10 and int(message) >= 1:
        	        	        return 'PRIVMSG '+ data['channel'] +' :' + str(random.randint(1,int(message))) + '\r\n'
	def linkbot(self,data):
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
	                        if self.nlink[-4:] == '.cgi' or self.nlink[-4:] == '.CGI':#don't process cgi links
	                                title = 'Get fucked'# You should probaly change this...
				else:#only get one line of titles
                                	title = gettitle(self.nlink)
                                	title = title.splitlines()
                                	title = title[0]
                        	if len(title) >= 150:#cap the length of titles
                        	        title = title[:150]
                        	title = html_decode(title)
                        	print title
				error = 0
               		except:	
                	        print "[E]No valid title"
                	        error = 2
                	#post title to irc
                	if error == 0 and data['loop'] >= data['numr']:
                	        if len(self.nlink) >= 40:
					return 'privmsg ' + data['channel'] + ' : ^ ' + str(title) + " " + maketiny(self.link[0]) + ' ^\n\r'
                        	else:
                                	return 'privmsg ' + data['channel'] + ' : ^ ' + str(title) + " ^\r\n"
               		if error == 2 and urlsfound == True and self.nlink != "" and data['loop'] >= data['numr'] and len(self.nlink) >= 40:
                        	return 'privmsg ' + data['channel'] + ' : ^ ' + maketiny(self.nlink) + ' ^\r\n'
			else:
				return ''
		else:
			return ''
