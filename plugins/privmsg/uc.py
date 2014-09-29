import urllib2, json
def main(data):
	if '!uc ' in data['recv']:
		args = argv('!uc', data['recv'])
		query = '%20'.join(args['argv'][1:])
		wikiajson = urllib2.urlopen('http://uncovering-cicada.wikia.com/api/v1/Search/List?query=' + query).read()
		wikiaobj = json.loads(wikiajson)
		title = wikiaobj['items'][0]['title']
		tiny = maketiny(wikiaobj['items'][0]['url'])
		return say(args['channel'], title + ' - ' + tiny)
