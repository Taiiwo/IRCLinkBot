from BeautifulSoup import BeautifulSoup
def main(data):
	if '!wa ' in data['recv']:
		args = argv('!wa',data['recv'])
		query = '%20'.join(args['argv'][1:])
		response = urllib2.urlopen('http://api.wolframalpha.com/v2/query?input=' + query + '&appid=QPEPAR-TKWEJ3W7VA').read()
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
			return say(args['channel'], "Information not available.")
