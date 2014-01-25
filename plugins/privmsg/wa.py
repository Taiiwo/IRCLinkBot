from BeautifulSoup import BeautifulSoup
def main(data):
	if '!wa ' in data['recv']:
		args = argv('!wa',data['recv'])
		query = '%20'.join(args['argv'][1:])
		response = urllib2.urlopen('http://api.wolframalpha.com/v2/query?input=' + query + '&appid=Y76J7A-WKLWTY7RKJ').read()
		soup = BeautifulSoup(response)
		answer = soup.queryresult.findAll('pod')[1].subpod.plaintext.text
		answer = answer.split('\n')
		toret = []
		for i in answer:
			toret.append(say(args['channel'],i).encode('ascii', 'ignore'))
		return ''.join(toret)