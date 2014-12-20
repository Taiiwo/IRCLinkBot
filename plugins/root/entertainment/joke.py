def main(data):
        if '!joke' in data['recv']:
                args = argv('!joke',data['recv'])
		url = 'http://www.sickipedia.org/random/'
		while 1:
			html = urllib2.urlopen(url).read()
			joke = textbetween('<section class="jokeText" itemprop="text">', '</section>\n\t\t\t\t<aside class="jokeSocialButtons">',html).strip()
			joke = joke.replace('<br />',' ')
			joke = joke.replace('\n',' ')
			joke = joke.replace('\r',' ')
			joke = joke.replace('\t',' ')
			"""
			# Load the string into BeautifulSoup for parsing.
			soup = BeautifulSoup(html)
			for tag in soup.findAll(True):
				if tag.name != 'section':
					tag.hidden = True
                        joke = soup.find('section', attrs={'class':'jokeText'}).string #div -> section. It works.
			"""
                        #   joke = unicode(joke) 1 problem I've found - jokes are not nearly as funny as they used to be
                        if len(joke) <= 500:
                                joke = joke.decode("utf-8")
                                joke = html_decode(joke.encode("ascii","ignore"))
                                return 'privmsg ' + args['channel'] + ' :' + joke + '\r\n'
