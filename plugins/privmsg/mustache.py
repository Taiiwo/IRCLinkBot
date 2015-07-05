def main(data):
    if '!mustache' in data['recv']:
        import urllib
        args = argv('!mustache',data['recv'])
        target = ' '.join(args['argv'][1:])
        baseUrl = "http://ajax.googleapis.com/ajax/services/search/images?"
        query = {
            "v": "1.0",
            "q": target,
            "start": 0
        }
        query = urllib.urlencode(query)
        images = json.loads(urllib2.urlopen(baseUrl + query).read())
        n = random.randint(0, len(images['responseData']['results']) - 1)
        image = images['responseData']['results'][n]['url']
        baseUrl = "http://mustachify.me/?"
        query = {"src": image}
        query = urllib.urlencode(query)
        mustacheUrl = baseUrl + query
        data['api'].say(args['channel'], maketiny(mustacheUrl))
