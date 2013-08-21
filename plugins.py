from util import *
class plugins:
	def love(data):
		message = command("!love")
        	if str(message) != 'None':
        	        data['s'].send('privmsg ' + channel + ' :I love ' + str(message) + '\r\n')
        def say(data):
		message = command("!say")
	        if str(message) != 'None':
	                data['s'].send('privmsg ' + channel + ' :' + str(message) + '\r\n')
        def rfl(data):
		message = command("!rfl")
        	if str(message) != 'None':
        	        data['s'].send('privmsg ' + channel + ' :I really fucking love ' + str(message) + '\r\n')
        def fact(data):
		message = command("!fact")
	        if str(message) != 'None':
	                data['s'].send('privmsg ' + channel + ' :' + textbetween("<strong>","</strong>", urllib2.urlopen("http://randomfunfacts.com").read())[3:-4] + '\r\n')
        def joke(data):
		message = command("!joke")
        	if str(message) != 'None':
        	        data['s'].send('privmsg ' + channel + ' :' + textbetween('<td style="color: #000000">','<td align="right width="95px">', urllib2.urlopen('http://www.sickipedia.org/joke/view/' + str(randomnum(61,1300))).read()[:-5]) + '\r\n')
	def pong(data):#respond to ping req in a string --Not perfect, but works
	        if "ping" in data['recv'] or "PING" in data['recv']:
	                url = str(geturl(str(data['recv'])))
	                if url != "":
	                        data['s'].send("PONG " + url + "\n\r")

        def wyr(data):
		if "!wyr" in data['recv']:
        	        error = 1
        	        while error == 1:
        	                try:
        	                        data['s'].send('PRIVMSG '+ channel +' :' + gettitle('http://www.rrrather.com/view/' + str(random.randint(0,40000)))+ '\r\n') 
        	                        error = 0
        	                except:
        	                        print '[Server Error (Not my fault)]'
        	                        error = 1
        def roll(data):
		message = command('!roll')
        	if str(message) != 'None':
        	        try:
        	                int(message)
        	                error = 0
        	        except:
        	                error = 1
        	        if error != 1 and len(message) <= 6 and int(message) >= 1:
        	                data['s'].send('PRIVMSG '+ channel +' :' + str(random.randint(1,int(message))) + '\r\n')
	def linkbot(data):
		urlsfound = True
	        try:#look for urls in recv
	                link2 = link#make a backup of last url
	                link = geturl(recv)
	                print link
	        except:
	                print "[-]No URLS found"
	                error = 1
	                urlsfound = False
	        if link2 != link:#This stops spamming links
	                try:#try to get the title of the url
	                        nlink = link[0]
	                        if nlink[-4:] == '.cgi' or nlink[-4:] == '.CGI':#don't process cgi links
	                                title = 'Get fucked'
				else:#only get one line of titles
                                	title = gettitle(nlink)
                                	title = title.splitlines()
                                	title = title[0]
                        	if len(title) >= 150:#cap the length of titles
                        	        title = title[:150]
                        	title = html_decode(title)
                        	print title
               		except:	
                	        print "[E]No valid title"
                	        error = 2
                	#post title to irc
                	if error == 0  and loop >= numr:
                	        if len(nlink) >= 40:
					 s.send('privmsg ' + channel + ' : ^ ' + str(title) + " " + maketiny(link[0]) + ' ^\n\r')
                        else:
                                data['s'].send('privmsg ' + channel + ' : ^ ' + str(title) + " ^\r\n")
               		if error == 2 and urlsfound == True and nlink != "" and loop >= numr and len(nlink) >= 40:
                        	data['s'].send('privmsg ' + channel + ' : ^ ' + maketiny(nlink) + ' ^\r\n')
