from BeautifulSoup import BeautifulSoup
def main(data):
	if '!wa ' in data['recv']:
		import urllib
		args = argv('!wa',data['recv'])
		query = ' '.join(args['argv'][1:])
		query = {'input': query, 'appid': 'QPEPAR-TKWEJ3W7VA'}
		query = urllib.urlencode(query)
		response = urllib2.urlopen('http://api.wolframalpha.com/v2/query?' + query).read()
		soup = BeautifulSoup(response)
		try:
			interp = soup.queryresult.findAll('pod')[0].subpod.plaintext.string
			answer = soup.queryresult.findAll('pod')[1].subpod.plaintext.string
			answer = answer.split('\n')
			toret = [say(args['channel'], interp + ' :').encode('ascii', 'ignore'),]
			for i in answer:
				toret.append(say(args['channel'],i).encode('ascii', 'ignore'))
			return ''.join(toret)
		except:
			global bot
			query = ' '.join(args['argv'][1:])
			query = query.replace('\n','')
	                query = query.replace('\r','')
	                query = query.replace(data['config']['settings']['botNick'] + ':','')
	                query = query.replace(data['config']['settings']['botNick'],'CleverBot')
	                answer = bot.think(query)
	                answer = answer.replace('CleverBot',data['config']['settings']['botNick'])
	                answer = answer.replace('Cleverbot',data['config']['settings']['botNick'])
	                answer = answer.replace('God','Taiiwo')
	                answer = answer.replace('god','Taiiwo')
	                answer = answer.replace('&ouml;', 'o')
			return say(args['channel'], args['nick'] + ": " + answer)
