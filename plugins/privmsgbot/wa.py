from lxml import etree
def main(data):
	if '!wa ' in data['recv']:
		args = argv('!wa',data['recv'])
		query = '%20'.join(args['argv'][1:])
		response = urllib2.urlopen('http://api.wolframalpha.com/v2/query?input=' + query + '&appid=Y76J7A-WKLWTY7RKJ').read()
		tree = etree.XML(response)
		answer = tree.findall('pod')[1].find('subpod').find('plaintext').text
		answer = answer.split('\n')
		toret = []
		for i in answer:
			toret.append(say(args['user'],i).encode('ascii', 'ignore'))
		return ''.join(toret)

