def main(data):
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
